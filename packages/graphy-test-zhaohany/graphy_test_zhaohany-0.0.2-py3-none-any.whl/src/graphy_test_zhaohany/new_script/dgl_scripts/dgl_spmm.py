import sys
import dgl
from dgl import sparse
from dgl.data.utils import load_graphs
import torch 
from dgl import function as fn
import argparse
import datetime
from dgl.sparse import _gspmm,  _gsddmm
import time
#from dgl.sparse import _gspmm, _gspmm_hetero, _gsddmm, _gsddmm_hetero, _segment_reduce, _bwd_segment_cmp, _edge_softmax_forward, _edge_softmax_backward
#from dgl.sparse import _csrmm, _csrsum, _csrmask, _scatter_add, _update_grad_minmax_hetero

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='pick CPU or GPU to perform the graph deep learning ')
    parser.add_argument('--device', type=str, default= 'GPU', help='pick CPU or GPU')
    parser.add_argument('--reverse', type=str, default= 'no_reverse', help='pick reverse graph or not')
    parser.add_argument('--gdir', type=str,  help='pick the file name of saved dgl graph')
    args = parser.parse_args()

    # Select Device
    use_cuda = args.device == 'GPU' and torch.cuda.is_available()
    device = torch.device('cuda' if use_cuda else 'cpu')
    reverse = args.reverse == "reverse"
    if use_cuda:
        print("Using CUDA!")
    else:
        print('Not using CUDA!!!')


    ofile = args.gdir
    list_graph, label_dict_none = load_graphs(ofile) #"./_reddit_dgl.bin")
    graph = list_graph[0]

    
    if reverse:
        graph = dgl.reverse(graph, copy_edata=True)
        print("load reverse graph")
    
    graph = graph.to(device)
    num_vcount = graph.number_of_nodes() #232965

    print("edge loading done")
    print("graph edge:", graph.number_of_edges())
    print("graph edge:", num_vcount)

     
    num_heads = 1
    hidden_feature = 16
    # check DGL kernel spmm 
    score = torch.ones(num_vcount, hidden_feature)
    score = score.to(device)
    
    g_start = datetime.datetime.now()
    #score_max = _gspmm(graph._graph, 'copy_rhs', 'max', None, score)[0]
    score_max = _gspmm(graph._graph, 'copy_lhs', 'sum', score, None)[0]
    torch.cuda.synchronize()
    g_end = datetime.datetime.now()
    
    diff = g_end - g_start
    print ('spmm time is:', diff)
    #print("spmm done", score_max, score_max.size())
    
    ###########
    #time.sleep(3)
    g_start = datetime.datetime.now()
    score_max = _gspmm(graph._graph, 'copy_lhs', 'sum', score, None)[0]
    torch.cuda.synchronize()
    g_end = datetime.datetime.now()
    
    diff = g_end - g_start
    print ('spmm time is:', diff)
    print("spmm done", score_max, score_max.size())
    
    #res_load = torch.load('/home/ygong07/Graphy_workload_compare/GraphPy_workflow/new_script/test/spmmw2d_result.pt')
    #print("res_load", res_load, res_load.size())
    #print("score_max", score_max, score_max.size())
    #print("spmmw2d results are the same", torch.all(res_load.eq(score_max)))
    #print("rst", rst)

