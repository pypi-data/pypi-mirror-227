import torch
import torch.nn as nn
import itertools
import torch.nn.functional as F
import datetime

import pygraph as gone
import gatconv 
import pubmed_util
import create_graph as cg
import kernel as gpk
import kernel
import sparse
import argparse
import time
import gp_apis

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='pick CPU or GPU to perform the graph deep learning ')
    parser.add_argument('--device', type=str, default= 'CPU', help='pick CPU or GPU')

    args = parser.parse_args()
    #check gcn kernel
    
    # Select Device
    use_cuda = args.device == 'GPU' and torch.cuda.is_available()
    device = torch.device('cuda' if use_cuda else 'cpu')
    if use_cuda:
        print("Using CUDA!")
    else:
        print('Not using CUDA!!!')

    ifile = "/mnt/huge_26TB/data/test2/reddit/binary_graph/"
    
    ofile = ifile + "../saved_graph/"

    graph = kernel.load_graph(ofile);

    num_vcount = graph.get_vcount()
    num_ecount = graph.get_edge_count()
    print("num_vcount, num_ecount are:", num_vcount, num_ecount)
    print("load graph successfully")
    torch.set_printoptions(edgeitems=20)
    
    heads = 1
    reverse = 0

    # sddmme2d
    dim0 = num_ecount
    dim1 = 1
    X = torch.load('data_save/sddmme2d_X.pt')
    X = X.to(device)
    Y = torch.load('data_save/sddmme2d_Y.pt')
    Y = Y.to(device)
    efficient_score = gp_apis.gp_gsddmme2d(graph, X, Y, dim0, dim1, gone.enumOP.eSUM, reverse, device)
    
    score_max = gp_apis.gp_gspmmw2d(graph, efficient_score, num_vcount, heads, gone.enumOP.eMAX, 0, device)
    score = gp_apis.gp_gsddmm2d(graph, score_max, efficient_score, num_ecount, heads, gone.enumOP.eSUB, 0, device)
    
    score_exp = torch.exp(score)
    
    score_sum = gp_apis.gp_gspmmw2d(graph, score_exp, num_vcount, heads, gone.enumOP.eSUM, 0, device)
    #out = gp_apis.gp_gsddmm2d(graph, score_sum, score_exp, num_ecount, heads, gone.enumOP.eDIV, 0, device)
    torch.cuda.synchronize()
    
    res = score_sum
    print("res is", res)
    torch.save(res.to("cpu"), 'data_save/out.pt')
    
