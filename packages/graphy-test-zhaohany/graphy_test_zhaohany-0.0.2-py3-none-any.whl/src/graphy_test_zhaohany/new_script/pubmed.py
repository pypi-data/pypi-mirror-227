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
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='pick CPU or GPU to perform the graph deep learning ')
    parser.add_argument('--device', type=str, default= 'CPU', help='pick CPU or GPU')
    parser.add_argument('--kernel', type=str, default= 'GAT', help='pick GCN or GAT')
    parser.add_argument('--random', type=str, default= 'no', help='pick random or ones')
    parser.add_argument('--save', type=str, default= 'no', help='pick save file or not save output')
    args = parser.parse_args()
    
    #check gcn kernel
    test_gcn = args.kernel == 'GCN'
    
    # Select Device
    use_cuda = args.device == 'GPU' and torch.cuda.is_available()
    device = torch.device('cuda' if use_cuda else 'cpu')
    random = args.device == 'random'
    save_file = args.save == 'save'
    reverse = 1
    
    if use_cuda:
        print("Using CUDA!")
    else:
        print('Not using CUDA!!!')
    
    if random:
        print("use random as init value")
    else:
        print("not use random init value ")
    
    if save_file:
        print("kernel output is saved")
    else:
        print("kernel output is not saved")

    ofile = "/home/ygong07/data/test2/pubmed/saved_graph/"
    if test_gcn:
        G = kernel.load_graph_noeid(ofile);
    else:
        G = kernel.load_graph(ofile);
    
    num_vcount = G.get_vcount();
    print("load graph successfully")
    torch.set_printoptions(edgeitems=20)

    num_ecount = G.get_edge_count()
    #hidden_feature = 3
    
    num_heads_list = [1]
    hidden_feature = 3 
    
    print(num_vcount, num_ecount)
    print("begin test kernel(3d)")
    for num_heads in num_heads_list:
        if test_gcn:
            dim0 = num_vcount
            dim1 = hidden_feature
            X = torch.ones(dim0, dim1)
            #torch.save(X, 'data_save/X_file.pt')
            X = X.to(device)
            X_dl = torch.utils.dlpack.to_dlpack(X)
            res = torch.zeros(dim0, dim1)
            res = res.to(device)
            res_dl = torch.utils.dlpack.to_dlpack(res)
            
            g_start = datetime.datetime.now()
            norm = 1
            gpk.spmm(G, X_dl, res_dl, reverse, norm)  # do not specify the reduce operation
            torch.cuda.synchronize();
            g_end = datetime.datetime.now()
            diff = g_end - g_start
            print ('spmm time is:', diff)
            #print("res is", res)
            #res = res.to("cpu")
            torch.save(res, 'data_save/res1.pt')

        else: 
            # gspmmw_op2d
            dim0 = num_vcount
            dim1 = num_heads
            dim2 = hidden_feature
            #num_vcount = 232965
            #hidden_feature = 16
            #num_ecount = 229231784
            if random:
                X = torch.rand(num_vcount, num_heads, hidden_feature)
            else:
                X = torch.ones(num_vcount, num_heads, hidden_feature)
            #torch.save(X, 'pubmed/spmmw_op2d_X.pt')
            #X = torch.load('/home/ygong07/GraphPy_2d_partition/build/pubmed/spmmw_op2d_X.pt')
            #print("X is", X.size())
            X = X.to(device)
            X_dl = torch.utils.dlpack.to_dlpack(X)
            if random:
                Y = torch.rand(num_ecount, num_heads)
            else:
                Y = torch.ones(num_ecount, num_heads)
            #torch.save(Y, 'pubmed/spmmw_op2d_Y.pt')
            #Y = torch.load('/home/ygong07/GraphPy_2d_partition/build/pubmed/spmmw_op2d_Y.pt')
            Y = Y.to(device)
            Y_dl = torch.utils.dlpack.to_dlpack(Y)
            res = torch.zeros(dim0, num_heads, hidden_feature)
            res = res.to(device)
            res_dl = torch.utils.dlpack.to_dlpack(res)
            g_start = datetime.datetime.now()
            #gpk.spmmw_op2d(G, X_dl, Y_dl, res_dl, gone.enumOP.eSUM, reverse)
            gpk.gspmmw_op(G, X_dl, Y_dl, res_dl, gone.enumOP.eSUM, reverse)
            g_end = datetime.datetime.now()
            diff = g_end - g_start
            print ('spmmw_op2d time is:', diff)
            print("result", res)
            #print("the num_heads is ",num_heads)
            torch.save(res, 'test/spmmw_op2d_res.pt')
            #print("res is", res)
            #torch.save(res, 'pubmed/spmmw_op2d_result_new.pt')

        
         
            #spmmw2d
            dim0 = num_vcount
            dim1 = 1
            dim2 = 1
            if random:
                X = torch.rand(num_ecount, num_heads)
            else:   
                X = torch.ones(num_ecount, num_heads)
            #X = torch.load('/home/ygong07/GraphPy_2d_partition/build/reddit/spmmw2d_X.pt')
            X = X.to(device)
            #torch.save(X, 'pubmed/spmmw2d_X.pt')
            X_dl = torch.utils.dlpack.to_dlpack(X)
            res = torch.zeros(dim0, num_heads, dim2)
            res = res.to(device)
            res_dl = torch.utils.dlpack.to_dlpack(res)
            g_start = datetime.datetime.now()
            gpk.spmmw2d(G, X_dl, res_dl, gone.enumOP.eSUM, reverse)
            g_end = datetime.datetime.now()
            diff = g_end - g_start
            print ('spmmw2d time is:', diff)
            #print("the num_heads is ",num_heads)
            #print("result", res)
            torch.save(res, 'test/spmmw2d_result.pt')

        
            # sddmme2d
            dim0 = num_ecount
            dim1 = 1
            if random:
                X = torch.rand(num_vcount, num_heads, 1)
            else:
                X = torch.ones(num_vcount, num_heads, 1)
            #torch.save(X, 'pubmed/sddmme2d_X.pt')
            #X = torch.load('/home/ygong07/GraphPy_2d_partition/build/reddit/sddmme2d_X.pt')
            #print("X is", X)
            X = X.to(device)
            X_dl = torch.utils.dlpack.to_dlpack(X)
            if random:
                Y = torch.rand(num_vcount, num_heads, 1)
            else: 
                Y = torch.ones(num_vcount, num_heads, 1)
            #torch.save(Y, 'pubmed/sddmme2d_Y.pt')
            #Y = torch.load('/home/ygong07/GraphPy_2d_partition/build/reddit/sddmme2d_Y.pt')
            #print("Y is", Y)
            Y = Y.to(device)
            Y_dl = torch.utils.dlpack.to_dlpack(Y)
            res = torch.zeros(dim0, num_heads)
            res = res.to(device)
            res_dl = torch.utils.dlpack.to_dlpack(res)
            g_start = datetime.datetime.now()
            gpk.gsddmme2d(G, X_dl, Y_dl, res_dl, gone.enumOP.eSUM, reverse)
            g_end = datetime.datetime.now()
            diff = g_end - g_start
            print ('sddmme2d time is:', diff)
            #print("the num_heads is ",num_heads)
            #print("result", res)
            torch.save(res, 'test/sddmme2d_result.pt')

            # sddmm2d
            dim0 = num_ecount
            dim1 = 1
            if random:
                X = torch.rand(num_vcount, num_heads, 1)
            else:   
                X = torch.ones(num_vcount, num_heads, 1)
            #torch.save(X, 'pubmed/sddmm2d_X.pt')
            #X = torch.load('/home/ygong07/GraphPy_2d_partition/build/reddit/sddmm2d_X.pt')
            X = X.to(device)
            X_dl = torch.utils.dlpack.to_dlpack(X)
            if random:
                Y = torch.rand(num_ecount, num_heads)
            else:
                Y = torch.ones(num_ecount, num_heads)
            #torch.save(Y, 'pubmed/sddmm2d_Y.pt')
            #Y = torch.load('/home/ygong07/GraphPy_2d_partition/build/reddit/sddmm2d_Y.pt')
            Y = Y.to(device)
            Y_dl = torch.utils.dlpack.to_dlpack(Y)
            res = torch.zeros(dim0, num_heads)
            res = res.to(device)
            res_dl = torch.utils.dlpack.to_dlpack(res)
            g_start = datetime.datetime.now()
            gpk.sddmm2d(G, X_dl, Y_dl, res_dl, gone.enumOP.eSUB, reverse)
            g_end = datetime.datetime.now()
            diff = g_end - g_start
            print ('sddmm2d time is:', diff)
            #print("the num_heads is ",num_heads)
            #print("res",res)
            torch.save(res, 'test/sddmm2d_result.pt')
