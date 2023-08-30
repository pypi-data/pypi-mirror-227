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
    offset_file = ofile + '_csr_noeid.offset'
    nebrs_file = ofile + "_csr_noeid.nebrs"
    offset = np.fromfile(offset_file, dtype='int32')
    nebrs  = np.fromfile(nebrs_file, dtype='int32')
    rowptr = torch.from_numpy(offset)
    colind = torch.from_numpy(nebrs)
    graph = dgl.graph(('csr', (rowptr, colind, [])))
    graph = graph.to(device)

    num_vcount = rowptr.shape[0] - 1
    print("edge loading done")
    print("graph edge:", graph.number_of_edges())


    
    if reverse:
        graph = dgl.reverse(graph, copy_edata=True)
        print("load reverse graph")
    
    graph = graph.to(device)
    num_heads = 1
    #hidden_feature = 16
    hidden_feature = int(args.dim)
    print("the dim is:", hidden_feature)

    dim0 = num_vcount
    dim1 = hidden_feature
    
    feat = torch.ones(dim0, dim1) 
    feat = feat.to(device)

    graph.srcdata['ft'] = feat

    start = datetime.datetime.now()
    graph.update_all(fn.copy_src('ft', 'm'),
                     fn.sum('m', 'o'))
    torch.cuda.synchronize()
    end = datetime.datetime.now()
    difference = end - start
    print("the time of dgl is:", difference)
    rst = graph.dstdata['o']
    print("rst", rst)
    
    #"""
    start = datetime.datetime.now()
    degs = graph.out_degrees().float().clamp(min=1)
    #norm = torch.pow(degs, -0.5)
    norm = 1.0/degs #torch.pow(degs, -0.5)
    shp = norm.shape + (1,) * (rst.dim() - 1)
    norm = torch.reshape(norm, shp)
    rst1 =rst * norm
    torch.cuda.synchronize()
    end = datetime.datetime.now()
    difference = end - start
    print("the norm time of dgl norm:", difference)
    print("rst", rst1)
    #"""

    start = datetime.datetime.now()
    graph.update_all(fn.copy_src('ft', 'm'),
                     fn.sum('m', 'o'))
    torch.cuda.synchronize()
    end = datetime.datetime.now()
    difference = end - start
    print("the 1nd time of dgl is:", difference)
    
    start = datetime.datetime.now()
    graph.update_all(fn.copy_src('ft', 'm'),
                     fn.sum('m', 'o'))
    torch.cuda.synchronize()
    end = datetime.datetime.now()
    difference = end - start
    print("the 2nd time of dgl is:", difference)
    rst = graph.dstdata['o']
    #print("rst", rst)
    
    
    start = datetime.datetime.now()
    degs1 = graph.out_degrees().float().clamp(min=1)
    norm1 = 1.0/degs1 #torch.pow(degs, -0.5)
    shp1 = norm1.shape + (1,) * (rst.dim() - 1)
    norm1 = torch.reshape(norm1, shp1)
    rst1 = feat * norm1
    torch.cuda.synchronize()
    end = datetime.datetime.now()
    difference = end - start
    print("the 3nd norm time of dgl norm:", difference)
    print("rst", rst1)
    
