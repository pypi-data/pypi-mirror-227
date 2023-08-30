import numpy as np
import gat_multi_head as gat
import dgl
import dgl.function as fn
import dgl.nn as dglnn
from dgl.base import DGLError
from dgl.nn.functional import edge_softmax
import torch.nn as nn



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

    def __init__(self, in_feats, out_feats, map_feats, num_heads):
        super(GatedGAT, self).__init__()
        self.in_feats = in_feats
        self.out_feats = out_feats
        self.map_feats = map_feats
        self.num_heads = num_heads
        self.gatlayer = gat.GATConv(
            self.in_feats, self.out_feats, self.num_heads
        )
        self.gate_fn = nn.Linear(
            2 * self.in_feats + self.map_feats, self.num_heads
        )
        self.gate_m = nn.Linear(self.in_feats, self.map_feats)
        self.merger_layer = nn.Linear(
            self.in_feats + self.out_feats, self.out_feats
        )

    def forward(self, g, x):
        with g.local_scope():
            g.ndata["x"] = x
            g.ndata["z"] = self.gate_m(x)
            g.update_all(fn.copy_u("x", "x"), fn.mean("x", "mean_z"))
            g.update_all(fn.copy_u("z", "z"), fn.max("z", "max_z"))
            nft = th.cat(
                [g.ndata["x"], g.ndata["max_z"], g.ndata["mean_z"]], dim=1
            )
            gate = self.gate_fn(nft).sigmoid()
            attn_out = self.gatlayer(g, x)
            node_num = g.num_nodes()
            gated_out = (
                (gate.view(-1) * attn_out.view(-1, self.out_feats).T).T
            ).view(node_num, self.num_heads, self.out_feats)
            gated_out = gated_out.mean(1)
            merge = self.merger_layer(th.cat([x, gated_out], dim=1))
            return merge
