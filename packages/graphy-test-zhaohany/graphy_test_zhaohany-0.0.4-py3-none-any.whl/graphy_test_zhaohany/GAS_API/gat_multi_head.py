import torch as th
from torch import nn

import sparse

# pylint: enable=W0235
class GATConv(nn.Module):
    def __init__(self,
                 in_feats,
                 out_feats,
                 num_heads,
                 feat_drop=0.,
                 attn_drop=0.,
                 negative_slope=0.2,
                 activation=None,
                 allow_zero_in_degree=False):
        super(GATConv, self).__init__()
        self._num_heads = num_heads
        self._in_feats_size = in_feats
        self._out_feats = out_feats
        self._allow_zero_in_degree = allow_zero_in_degree

        self.linear = nn.Linear(
            self._in_feats_size, out_feats * num_heads, bias=False)
        self.fc = nn.Linear(
            self._in_feats_size, out_feats * num_heads, bias=False)
        self.attn_l = nn.Parameter(th.FloatTensor(size=(1, num_heads, out_feats)))
        self.attn_r = nn.Parameter(th.FloatTensor(size=(1, num_heads, out_feats)))
        self.feat_drop = nn.Dropout(feat_drop)
        self.attn_drop = nn.Dropout(attn_drop)
        self.leaky_relu = nn.LeakyReLU(negative_slope)

        self.reset_parameters()
        self.activation = activation

    def reset_parameters(self):
        """
        Description
        -----------
        Reinitialize learnable parameters.
        Note
        ----
        The fc weights :math:`W^{(l)}` are initialized using Glorot uniform initialization.
        The attention weights are using xavier initialization method.
        """
        gain = nn.init.calculate_gain('relu')
        # re-initilize the parameter for linear layer
        nn.init.xavier_normal_(self.linear.weight, gain=gain)
        # re-initilize the parameter for attention layer
        nn.init.xavier_normal_(self.attn_l, gain=gain)
        nn.init.xavier_normal_(self.attn_r, gain=gain)
        # re-initilize the parameter for linear layer
        # if isinstance(self.res_fc, nn.Linear):
        #     nn.init.xavier_normal_(self.res_fc.weight, gain=gain)

    def set_allow_zero_in_degree(self, set_value):
        r"""
        Description
        -----------
        Set allow_zero_in_degree flag.
        Parameters
        ----------
        set_value : bool
            The value to be set to the flag.
        """
        self._allow_zero_in_degree = set_value

    def forward(self, graph, feat):
        #print(feat, " ------0000", feat.size(), self._num_heads, self._out_feats)
        self.fc_src, self.fc_dst = self.fc, self.fc
        feat_src = feat_dst = self.fc(feat).view(-1, self._num_heads, self._out_feats)
        #print(feat_src.size(), " 1111")
        #print(self.attn_l.size(), "2222")
        el = (feat_src * self.attn_l).sum(dim=-1).unsqueeze(-1)
        er = (feat_dst * self.attn_r).sum(dim=-1).unsqueeze(-1)
        #el = el.flatten(1)
        #er = er.flatten(1)
        #print(el.size(), " 3333")

        # map_input = self.linear(feat).view(-1, self._num_heads, self._out_feats)
        # print (map_input.size())
        # print(self.attn_l.size())
        # el = th.matmul(map_input, self.attn_l)
        # er = th.matmul(map_input,  self.attn_r)

        num_vcount = graph.get_vcount()
        # since the score is scalar
        # dim = feat_src.size(1)
        dim = self._out_feats
        #print('222')
        #print(dim)
        # apply_edge add the attention_score by vertex, el and er are 3D tensor
        edge_score = sparse.apply_edge_heads(graph, el, er)
        efficient_score = self.leaky_relu(edge_score)
        # edge_score_by_softmax is a 3D tensor
        edge_score_by_softmax = sparse.edge_softmax_heads(graph, efficient_score, num_vcount, dim)
        #     // std::cout << "nani6" << std::endl;
        # torch::Tensor
        rst = sparse.run_gspmv_op_heads(graph, feat_src, edge_score_by_softmax, num_vcount, dim)
        #print (rst.size(), " 4444")

        # activation
        if self.activation:
            rst = self.activation(rst)
        return rst


class GAT(nn.Module):
    def __init__(self,
                 graph,
                 num_layers,
                 in_dim,
                 num_hidden,
                 num_classes,
                 heads,
                 activation = None,
                 feat_drop = 0.,
                 attn_drop = 0.,
                 negative_slope =0.2,
                 residual = False):
        super(GAT, self).__init__()
        self.graph = graph
        self.num_layers = num_layers
        self.gat_layers = nn.ModuleList()
        self.activation = activation
        # input projection (no residual)
        self.gat_layers.append(GATConv(
            in_dim, num_hidden, heads[0],
            feat_drop, attn_drop, negative_slope, False, self.activation))
        # hidden layers
        for l in range(1, num_layers):
            # due to multi-head, the in_dim = num_hidden * num_heads
            self.gat_layers.append(GATConv(
                num_hidden * heads[l-1], num_hidden, heads[l],
                feat_drop, attn_drop, negative_slope, residual, self.activation))
        # output projection
        self.gat_layers.append(GATConv(
            num_hidden * heads[-2], num_classes, heads[-1],
            feat_drop, attn_drop, negative_slope, residual, None))

    def forward(self, inputs):
        h = inputs
        for l in range(self.num_layers):
            h = self.gat_layers[l](self.graph, h).flatten(1)
        #print('111')
        #print(h.size())
        # output projection
        logits = self.gat_layers[-1](self.graph, h).mean(1)
        #print('debug')
        #print(logits.size())
        return logits

