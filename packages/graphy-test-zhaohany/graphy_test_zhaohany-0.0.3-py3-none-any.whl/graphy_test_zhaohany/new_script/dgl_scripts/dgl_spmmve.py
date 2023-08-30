import sys
import dgl
from dgl import sparse
import dgl.utils.internal as interu
from dgl.data.utils import load_graphs
import torch 
from torch import nn
from torch.nn import init
import numpy as np
from dgl import function as fn
from dgl.base import DGLError
from dgl.utils import expand_as_pair
import argparse
import datetime

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='pick CPU or GPU to perform the graph deep learning ')
    parser.add_argument('--device', type=str, default= 'GPU', help='pick CPU or GPU')
    parser.add_argument('--gdir', type=str,  help='pick the file name of saved dgl graph')
    parser.add_argument('--dim', type=str, default= 16, help='pick CPU or GPU')
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
    ofile = args.gdir
    list_graph, label_dict_none = load_graphs(ofile) #"./_reddit_dgl.bin")
    graph = list_graph[0]

    #torch.set_printoptions(edgeitems=75)
    #line_needed_to_skip = 0
    #src, dst, comment = read_graph_data(graph_data_path, line_needed_to_skip)
    #graph = build_dgl_graph(src, dst)
    
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
    print("the dim is:", hidden_feature)
    dim0 = num_vcount
    dim1 = num_heads
    dim2 = hidden_feature
    
    feat = torch.ones(dim0, dim1, dim2) 
    feat = feat.to(device)

    graph.srcdata['ft'] = feat
    graph.edata['a'] = torch.ones(num_ecount).to(device)

    start = datetime.datetime.now()
    graph.update_all(fn.u_mul_e('ft', 'a', 'm'),
                     fn.sum('m', 'o'))
    torch.cuda.synchronize()
    end = datetime.datetime.now()
    difference = end - start
    print("the 1nd time of dgl is:", difference)
    rst = graph.dstdata['o']
    print("rst", rst)

    start = datetime.datetime.now()
    graph.update_all(fn.u_mul_e('ft', 'a', 'm'),
                     fn.sum('m', 'o'))
    torch.cuda.synchronize()
    end = datetime.datetime.now()
    difference = end - start
    print("the 2nd time of dgl is:", difference)
    
    start = datetime.datetime.now()
    graph.update_all(fn.u_mul_e('ft', 'a', 'm'),
                     fn.sum('m', 'o'))
    torch.cuda.synchronize()
    end = datetime.datetime.now()
    difference = end - start
    print("the 3nd time of dgl is:", difference)
    rst = graph.dstdata['o']
    print("rst", rst)
