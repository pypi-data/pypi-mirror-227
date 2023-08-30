import torch as th
from torch import nn
import sparse
from utils import Identity


# pylint: enable=W0235
class GATConv(nn.Module):
    def __init__(self,
                 in_feats,
                 out_feats,
                 num_heads,
                 device,
                 feat_drop=0.,
                 attn_drop=0.,
                 negative_slope=0.2,
                 residual=False,
                 activation=None,
                 allow_zero_in_degree=False,
                 bias=True):
        super(GATConv, self).__init__()
        self._num_heads = num_heads
        self._in_feats_size = in_feats
        self._out_feats = out_feats
        self._allow_zero_in_degree = allow_zero_in_degree
        self.device = device

        #self.linear = nn.Linear(
        #    self._in_feats_size, out_feats * num_heads, bias=False)
        self.fc = nn.Linear(
            self._in_feats_size, out_feats * num_heads, bias=False)
        self.attn_l = nn.Parameter(th.FloatTensor(size=(1, num_heads, out_feats)))
        self.attn_r = nn.Parameter(th.FloatTensor(size=(1, num_heads, out_feats)))
        self.feat_drop = nn.Dropout(feat_drop)
        self.attn_drop = nn.Dropout(attn_drop)
        self.leaky_relu = nn.LeakyReLU(negative_slope)
        if residual:
            if self._in_dst_feats != out_feats:
                self.res_fc = nn.Linear(
                    self._in_dst_feats, out_feats, bias=False)
            else:
                self.res_fc = Identity()
        else:
            self.register_buffer('res_fc', None)
        if bias:
            self.bias = nn.Parameter(th.FloatTensor(size=(num_heads*out_feats,)))
        else:
            self.register_buffer('bias', None)

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
        # re-initilize the parameter for fc layer
        nn.init.xavier_normal_(self.fc.weight, gain=gain)
        # re-initilize the parameter for attention layer
        nn.init.xavier_normal_(self.attn_l, gain=gain)
        nn.init.xavier_normal_(self.attn_r, gain=gain)
        if self.bias is not None:
            nn.init.constant_(self.bias, 0)
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
        h_src = h_dst = self.feat_drop(feat)
        feat_src = self.fc(h_src).view(-1, self._num_heads, self._out_feats)
        feat_dst = self.fc(h_dst).view(-1, self._num_heads, self._out_feats)
        #print(feat_src.size(), " 1111")
        #print(self.attn_l.size(), "2222")
        el = (feat_src * self.attn_l).sum(dim=-1).unsqueeze(-1)
        er = (feat_dst * self.attn_r).sum(dim=-1).unsqueeze(-1)


        num_vcount = graph.get_vcount()
        # since the score is scalar
        # dim = feat_src.size(1)
        dim = self._out_feats
        #print('222', dim)
        # apply_edge add the attention_score by vertex, el and er are 3D tensor
        edge_score = sparse.apply_edge_heads(graph, el, er, self.device)
        efficient_score = self.leaky_relu(edge_score)
        # edge_score_by_softmax is a 3D tensor
        edge_score_by_softmax = self.attn_drop(sparse.edge_softmax_heads(graph, efficient_score, num_vcount, dim, self.device))
        #print ("softmax edge_score", edge_score_by_softmax)
        rst = sparse.run_gspmv_op_heads(graph, feat_src, edge_score_by_softmax, num_vcount, dim, self.device)
        #print ("rst",rst.size())

        # residual
        if self.res_fc is not None:
            resval = self.res_fc(h_dst).view(h_dst.shape[0], self._out_feats)
            rst = rst + resval

        src_prefix_shape = dst_prefix_shape = feat.shape[:-1]
        # bias
        if self.bias is not None:
            rst = rst + self.bias.view(
                    *((1,) * len(dst_prefix_shape)), self._num_heads, self._out_feats)
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
                 device, 
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
        self.device = device
        # input projection (no residual)
        self.gat_layers.append(GATConv(
            in_dim, num_hidden, heads[0], self.device,
            feat_drop, attn_drop, negative_slope, False, self.activation))
        # hidden layers
        for l in range(1, num_layers):
            # due to multi-head, the in_dim = num_hidden * num_heads
            self.gat_layers.append(GATConv(
                num_hidden * heads[l-1], num_hidden, heads[l], self.device,
                feat_drop, attn_drop, negative_slope, residual, self.activation))
        # output projection
        self.gat_layers.append(GATConv(
            num_hidden * heads[-2], num_classes, heads[-1], self.device,
            feat_drop, attn_drop, negative_slope, residual, None))

    def forward(self, inputs):
        h = inputs
        for l in range(self.num_layers):
            h = self.gat_layers[l](self.graph, h).flatten(1)
        #print(h.size())
        # output projection
        logits = self.gat_layers[-1](self.graph, h).mean(1)
        #print('debug')
        #print(logits.size())
        return logits
