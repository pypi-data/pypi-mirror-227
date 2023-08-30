import torch 
from torch import nn
import numpy as np
import dgl
from dgl.data.utils import load_graphs
import argparse
import datetime
import time
import dgl.sparse as dglsp
import create_graph_dgl as cg
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
    parser.add_argument('--reverse', type=bool, required=False, help='pick graph directory')
    parser.add_argument('--gdir', type=str, required=True, help='pick graph directory')
    parser.add_argument('--device', type=str, default= 'GPU', help='pick CPU or GPU')
    parser.add_argument('--graph', type=str, default= 'text', help='pick text or binary')
    parser.add_argument('--dim', type=int, default= 41, help='intermediate feature length')


    args = parser.parse_args()

    # Select Device
    use_cuda = args.device == 'GPU' and torch.cuda.is_available()
    device = torch.device('cuda' if use_cuda else 'cpu')
    reverse = args.reverse == "reverse"
    if use_cuda:
        print("Using CUDA!")
    else:
        print('Not using CUDA!!!')

    graph_dir = args.gdir #"/mnt/huge_26TB/data/test2/cora/"
    if args.graph == 'text':
        graph_data_path = graph_dir + "graph_structure/graph.txt"
        line_needed_to_skip = 4
        src, dst, comment = cg.read_graph_data(graph_data_path, line_needed_to_skip)
        graph = cg.build_dgl_graph(src, dst)
    else:
        graph_data_path = graph_dir + "dgl_graph/graph.dgl"
        list_graph, label_dict_none = load_graphs(graph_data_path)
        graph = list_graph[0]


    num_vcount = graph.number_of_nodes()
    num_heads = 1
    #torch.set_printoptions(edgeitems=75)
    #cuda = torch.device('cuda')
    line_needed_to_skip = 0

    if reverse:
        graph = dgl.reverse(graph, copy_edata=True)
        print("load reverse graph")
    graph = graph.to(device)
    print("edge loading done")
    print("graph edge:", graph.number_of_edges())
    #graph=graph.to(cuda)
    dim0 = num_vcount
    dim1 = num_heads
    dim2 = args.dim
    num_ecount = graph.number_of_edges()
    #feat = torch.load('/home/ygong07/Graphy_workload_compare/GraphPy_workflow/new_script/test_save/gat_feat_X.pt')
    #feat = torch.ones(dim0, dim1) 
    feat = torch.ones(dim0, dim1, dim2) 
    feat_src = feat.to(device)
    
    feat1 = torch.ones(dim0, dim1, dim2) 
    feat_dst = feat1.to(device)
    
    #feat = feat.to(cuda)
    #feat_drop = nn.Dropout(p = 0.0)

    #feat_src = feat_drop(feat)
    #feat_dst = feat_drop(feat)

    
    #ndices = torch.tensor([[1, 1, 2], [2, 3, 3]])
    #val = torch.arange(1, 4).float()
    #A = dglsp.spmatrix(indices, val, (3, 4))
    #X1 = torch.randn(3, 5)
    #X2 = torch.randn(5, 4)
    #dglsp.sddmm(A, X1, X2)

    # check DGL kernel sddmme
    g_start = datetime.datetime.now()
    rst = dglsp._gsddmm(graph._graph, 'dot', feat_src, feat_dst, 'u', 'v')
    torch.cuda.synchronize()
    g_end = datetime.datetime.now()
    diff = g_end - g_start
    print ('sddmme time is:', diff)
    print("rst", rst, rst.size())
    
    g_start = datetime.datetime.now()
    rst = dglsp._gsddmm(graph._graph, 'dot', feat_src, feat_dst, 'u', 'v')
    torch.cuda.synchronize()
    g_end = datetime.datetime.now()
    diff = g_end - g_start
    print ('sddmme time is:', diff)
    print("rst", rst, rst.size())

    #res_load = torch.load('/home/ygong07/Graphy_workload_compare/GraphPy_workflow/new_script/test/sddmme2d_result.pt')
    #res_load = torch.flatten(res_load)
    #print("res_load", res_load, res_load.size())
    #print("sddmme results are the same", torch.all(res_load.eq(rst)))
    #print("rst", rst)
    
    
