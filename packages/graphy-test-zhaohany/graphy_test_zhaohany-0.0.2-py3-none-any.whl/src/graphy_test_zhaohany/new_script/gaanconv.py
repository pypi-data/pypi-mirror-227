import numpy as np
import gat_multi_head as gat
import torch as th
from torch import nn
import sparse
from utils import Identity
import copy



class GatedGAT(nn.Module):
    """Gated Graph Attention module, it is a general purpose
    graph attention module proposed in paper GaAN. The paper use
    it for traffic prediction task
    Parameter
    ==========
    in_feats : int
        number of input feature
    out_feats : int
        number of output feature
    map_feats : int
        intermediate feature size for gate computation
    num_heads : int
        number of head for multihead attention
    """

    def __init__(self, in_feats, out_feats, map_feats, num_heads, device):
        super(GatedGAT, self).__init__()
        self.in_feats = in_feats
        self.out_feats = out_feats
        self.map_feats = map_feats
        self.num_heads = num_heads
        self.device = device
        self.gatlayer = gat.GATConv(
            self.in_feats, self.out_feats, self.num_heads, self.device
        )
        self.gate_fn = nn.Linear(
            2 * self.in_feats + self.map_feats, self.num_heads
        )

        self.gate_m = nn.Linear(self.in_feats, self.map_feats)
        self.merger_layer = nn.Linear(
            self.in_feats + self.out_feats, self.out_feats
        )

    def forward(self, g, x):
        linear_z = self.gate_m(x)
        copy_x = copy.deepcopy(x)
        #copy_linear_z = copy.deepcopy(linear_z)
        #g.update_all(fn.copy_u("x", "x"), fn.mean("x", "mean_z"))
        #g.update_all(fn.copy_u("z", "z"), fn.max("z", "max_z"))
        dim0 = x.size(1)
        dim1 = linear_z.size(1)
        node_num = g.get_vcount()
        # need the max and mean operator
        mean_z = sparse.run_gspmm(g, copy_x, 1, node_num, dim0, self.device)
        max_z = sparse.run_gspmm_max(g, linear_z, 0, node_num, dim1, self.device)
        nft = th.cat(
            [x, max_z, mean_z], dim=1
        )
        gate = self.gate_fn(nft).sigmoid()
        attn_out = self.gatlayer(g, x)
        print("attn_out", attn_out)
        gated_out = (
            (gate.view(-1) * attn_out.view(-1, self.out_feats).T).T
        ).view(node_num, self.num_heads, self.out_feats)
        gated_out = gated_out.mean(1)
        merge = self.merger_layer(th.cat([x, gated_out], dim=1))
        return merge
