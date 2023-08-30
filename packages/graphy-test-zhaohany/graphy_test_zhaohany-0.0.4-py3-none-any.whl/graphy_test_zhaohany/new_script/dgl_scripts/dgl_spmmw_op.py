import sys
from dgl import sparse
import dgl.utils.internal as interu
import torch 
from torch import nn
from torch.nn import init
import numpy as np
from dgl import function as fn
from dgl.base import DGLError
from dgl.utils import expand_as_pair
import dgl
from dgl.nn.pytorch import edge_softmax
import argparse
import datetime
from dgl.sparse import _gspmm,  _gsddmm
import time
#from dgl.sparse import _gspmm, _gspmm_hetero, _gsddmm, _gsddmm_hetero, _segment_reduce, _bwd_segment_cmp, _edge_softmax_forward, _edge_softmax_backward
#from dgl.sparse import _csrmm, _csrsum, _csrmask, _scatter_add, _update_grad_minmax_hetero

def read_graph_data(file_path, line_needed_to_skip):
    crs = open(file_path, "r")
    print ("Output of Read function is ")
    # print (crs.read())
    a = [line.split() for line in crs]
    comment = a[0:line_needed_to_skip]
    array = a[line_needed_to_skip:]
    # convert the edge to src and dst
    src = []
    dst = []
    for each_edge in array:
        src.append(int(each_edge[0]))
        dst.append(int(each_edge[1]))
    return src, dst, comment

def build_dgl_graph(src, dst):
    # while the other for destination endpoints.
    src = np.array(src)
    dst = np.array(dst)
    # Edges are directional in DGL; Make them bi-directional.
    u = np.concatenate([src, dst])
    v = np.concatenate([dst, src])
    # Construct a DGLGraph
    return dgl.DGLGraph((u, v))


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='pick CPU or GPU to perform the graph deep learning ')
    parser.add_argument('--device', type=str, default= 'CPU', help='pick CPU or GPU')
    parser.add_argument('--reverse', type=str, default= 'no_reverse', help='pick reverse graph or not')
    args = parser.parse_args()

    # Select Device
    use_cuda = args.device == 'GPU' and torch.cuda.is_available()
    device = torch.device('cuda' if use_cuda else 'cpu')
    reverse = args.reverse == "reverse"
    if use_cuda:
        print("Using CUDA!")
    else:
        print('Not using CUDA!!!')

    graph_data_path = "/mnt/huge_26TB/data/test2/reddit/graph_structure/reddit_graph_undirect.txt"
    num_vcount = 232965
    num_heads = 1
    hidden_feature = 16
    #torch.set_printoptions(edgeitems=75)
    #cuda = torch.device('cuda')
    line_needed_to_skip = 0

    src, dst, comment = read_graph_data(graph_data_path, line_needed_to_skip)
    graph = build_dgl_graph(src, dst)
    if reverse:
        graph = dgl.reverse(graph, copy_edata=True)
        print("load reverse graph")
    graph = graph.to(device)
    print("edge loading done")
    print("graph edge:", graph.number_of_edges())
    #graph=graph.to(cuda)
    dim0 = num_vcount
    dim1 = num_heads
    dim2 = hidden_feature
    num_ecount = graph.number_of_edges()
    #feat = torch.load('/home/ygong07/Graphy_workload_compare/GraphPy_workflow/new_script/test_save/gat_feat_X.pt')
    feat = torch.ones(dim0, dim1, dim2) 
    feat = feat.to(device)
    #feat = feat.to(cuda)
    feat_drop = nn.Dropout(p = 0.0)
    attn_drop = nn.Dropout(p = 0.0)

    feat_src = feat_drop(feat)
    feat_dst = feat_drop(feat)

    el = (feat_src ).sum(dim=-1).unsqueeze(-1)
    er = (feat_dst ).sum(dim=-1).unsqueeze(-1)
    graph.srcdata.update({'ft': feat_src, 'el': el})
    graph.dstdata.update({'er': er})
    # compute edge attention, el and er are a_l Wh_i and a_r Wh_j respectively.
     
    time.sleep(1)
    # check DGL kernel spmmw_op
    edge_score = torch.ones(num_ecount, num_heads)
    edge_score = edge_score.to(device)
    graph.edata['a'] = edge_score
    start = datetime.datetime.now()
    graph.update_all(fn.u_mul_e('ft', 'a', 'm'),
                     fn.sum('m', 'ft'))
    rst = graph.dstdata['ft']
    end = datetime.datetime.now()
    difference = end - start
    print("the time of spmmw_op is:", difference)
    res_load = torch.load('/home/ygong07/Graphy_workload_compare/GraphPy_workflow/new_script/test/spmmw_op2d_result.pt')
    print("spmmw_op2d results are the same", torch.all(res_load.eq(rst)))
    print("rst", rst)
