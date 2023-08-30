from dgl.data.utils import load_graphs
import torch 
from torch import nn
import dgl
import argparse
import datetime
from dgl.sparse import _gspmm,  _gsddmm
import time
import create_graph_dgl as cg
from dgl import function as fn
#from dgl.sparse import _gspmm, _gspmm_hetero, _gsddmm, _gsddmm_hetero, _segment_reduce, _bwd_segment_cmp, _edge_softmax_forward, _edge_softmax_backward
#from dgl.sparse import _csrmm, _csrsum, _csrmask, _scatter_add, _update_grad_minmax_hetero

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='pick CPU or GPU to perform the graph deep learning ')
    parser.add_argument('--device', type=str, default= 'GPU', help='pick CPU or GPU')
    parser.add_argument('--gdir', type=str,  help='pick the file name of saved dgl graph')
    parser.add_argument('--dim', type=str, default= 32, help='pick CPU or GPU')
    parser.add_argument('--graph', type=str, default= 'text', help='pick text or binary')
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
    graph_dir = args.gdir #"/mnt/huge_26TB/data/test2/cora/"
    if args.graph == 'text':
        graph_data_path = graph_dir + "graph_structure/graph.txt"
        line_needed_to_skip = 0
        src, dst, comment = cg.read_graph_data(graph_data_path, line_needed_to_skip)
        graph = cg.build_dgl_graph(src, dst)
    else:
        graph_data_path = graph_dir + "dgl_graph/graph.dgl"
        list_graph, label_dict_none = load_graphs(graph_data_path)
        graph = list_graph[0]


    #torch.set_printoptions(edgeitems=75)
    num_vcount = graph.number_of_nodes()
    num_ecount = graph.number_of_edges()
    print("number of node", num_vcount)
    print("number of edges", num_ecount)
    
    if reverse:
        graph = dgl.reverse(graph, copy_edata=True)
        print("load reverse graph")

    graph = graph.to(device)
    
    num_heads = 1
    hidden_feature = int(args.dim)

    dim0 = num_vcount
    dim1 = num_heads
    dim2 = hidden_feature
    num_ecount = graph.number_of_edges()
    #feat = torch.load('/home/ygong07/Graphy_workload_compare/GraphPy_workflow/new_script/test_save/gat_feat_X.pt')
    feat = torch.ones(dim0, dim2) 
    el = feat.to(device)
    
    feat1 = torch.ones(dim0, dim2) 
    er = feat1.to(device)
    
    graph.srcdata.update({'el': el})
    graph.dstdata.update({'er': er})
     
    #check DGL kernel sddmm
    g_start = datetime.datetime.now()
    graph.apply_edges(fn.u_add_v('el', 'er', 'e'))
    torch.cuda.synchronize()
    g_end = datetime.datetime.now()
    diff = g_end - g_start
    print ('sddmmvv time is:', diff) 
    rst = graph.edata.pop('e')
    print("rst", rst.size(), rst)
    
    g_start = datetime.datetime.now()
    graph.apply_edges(fn.u_add_v('el', 'er', 'e'))
    torch.cuda.synchronize()
    g_end = datetime.datetime.now()
    diff = g_end - g_start
    print ('sddmmvv time is:', diff) 
    
    #print("sddmm done ", score)
    #print("sddmm results are the same", torch.all(res_load.eq(score)))
    #print("rst", rst)
    
