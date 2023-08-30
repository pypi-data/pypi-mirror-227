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
    
    #ingestion_flag = gone.enumGraph.eUdir | gone.enumGraph.eBinarySource
    #ingestion_flag = gone.enumGraph.eUdir 
    #ifile = "/home/ygong07/data/test2/pubmed/graph_structure/"
    #num_vcount = 19717
    #cuda = torch.device('cuda')
    #ifile = "/home/datalab/data/test2/cora/graph_structure"
    #num_vcount = 2708

    #ifile = "/mnt/huge_26TB/data/test2/reddit/graph_structure"
    #ifile = "/mnt/huge_26TB/data/test2/reddit/binary_graph"
    #num_vcount = 232965
    parser = argparse.ArgumentParser(description='pick CPU or GPU to perform the graph deep learning ')
    parser.add_argument('--device', type=str, default= 'CPU', help='pick CPU or GPU')
    parser.add_argument('--kernel', type=str, default= 'GAT', help='pick GCN or GAT')

    args = parser.parse_args()
    #check gcn kernel
    test_gcn = args.kernel == 'GCN'
    # Select Device
    use_cuda = args.device == 'GPU' and torch.cuda.is_available()
    device = torch.device('cuda' if use_cuda else 'cpu')
    if use_cuda:
        print("Using CUDA!")
    else:
        print('Not using CUDA!!!')

    ifile = "/mnt/huge_26TB/data/test2/reddit/binary_graph/"
    ofile = ifile + "../saved_graph/"
    
    #ifile = "/home/ygong07/data/test2/pubmed/"
    #ofile = ifile + "saved_graph/"

    #ifile = "/home/ygong07/data/test2/cora/"
    #ofile = ifile + "saved_graph/"
    
    #ifile = "/home/ygong07/data/test2/citeseer/"
    #ofile = ifile + "saved_graph/"

    if test_gcn:
        G = kernel.load_graph_noeid(ofile);
    else:

        G = kernel.load_graph(ofile);
    num_vcount = G.get_vcount()
    num_ecount = G.get_edge_count()
    print("num_vcount, num_ecount are:", num_vcount, num_ecount)
    print("load graph successfully")
    #input_feature_dim = 602
    torch.set_printoptions(edgeitems=20)

    #ifile = "/home/ygong07/data/test2/citeseer/graph_structure"
    #num_vcount = 3327
    #input_feature_dim = 3703

    #G = cg.create_2d_partition_graph(ifile, num_vcount, ingestion_flag)
    print("graph is success")
    #input_feature_dim = 500
    


    num_ecount = G.get_edge_count()
    #hidden_feature = 3
    
    num_heads_list = [1]
    hidden_feature = 16
    
    print(num_vcount, num_ecount)
    print("begin test kernel(3d)")
    reverse = 0
    for num_heads in num_heads_list:
        if test_gcn:
        
            dim0 = num_vcount
            dim1 = hidden_feature
            #num_vcount = 232965
            #hidden_feature = 16
            #num_ecount = 229231784i
            X = torch.ones(dim0, dim1)
            X = X.to(device)
            norm = 1
            g_start = datetime.datetime.now()
            gp_apis.gp_gspmm(G, X, dim0, dim1, reverse, norm, device)
            #torch.save(X, 'data_save/X_file.pt')
            #X_dl = torch.utils.dlpack.to_dlpack(X)
            #res = torch.zeros(dim0, dim1)
            #res = res.to(device)
            #res_dl = torch.utils.dlpack.to_dlpack(res)
            #g_start = datetime.datetime.now()
            #gpk.spmm(G, X_dl, res_dl, reverse, norm)  # do not specify the reduce operation
            torch.cuda.synchronize()
            g_end = datetime.datetime.now()
            diff = g_end - g_start
            print ('spmm time is:', diff)

            time.sleep(1)
            X = torch.ones(dim0, dim1)
            X = X.to(device)
            norm = 1
            g_start = datetime.datetime.now()
            gp_apis.gp_gspmm(G, X, dim0, dim1, reverse, norm, device)
            torch.cuda.synchronize()
            g_end = datetime.datetime.now()
            diff = g_end - g_start
            print ('spmm time is:', diff)

            time.sleep(1)
            X = torch.ones(dim0, dim1)
            X = X.to(device)
            norm = 1
            g_start = datetime.datetime.now()
            gp_apis.gp_gspmm(G, X, dim0, dim1, reverse, norm, device)
            torch.cuda.synchronize()
            g_end = datetime.datetime.now()
            diff = g_end - g_start
            print ('spmm time is:', diff)




            #print("res is", res)
            
            #res1 = torch.flatten(res)
            #print(res)
            """
            cal = 0
            b = res1.tolist()
            for each in b:
                if each != 1.00:
                    cal = cal + 1
            print("num is", cal)
            """
             
            #res = res.to("cpu")
            #torch.save(res, 'data_save/res_file.pt')

        else: 
            
            # gspmmw_op2d
            dim0 = num_vcount
            dim1 = num_heads
            dim2 = hidden_feature
            X = torch.rand(num_vcount, num_heads, hidden_feature)
            #torch.save(X, 'pubmed/spmmw_op2d_X.pt')
            #X = torch.load('/home/ygong07/GraphPy_2d_partition/build/pubmed/spmmw_op2d_X.pt')
            #print("X is", X.size())
            X = X.to(device)
            Y = torch.ones(num_ecount, num_heads)
            #torch.save(Y, 'pubmed/spmmw_op2d_Y.pt')
            #Y = torch.load('/home/ygong07/GraphPy_2d_partition/build/pubmed/spmmw_op2d_Y.pt')
            Y = Y.to(device)
            res = torch.zeros(dim0, num_heads, hidden_feature)
            res = res.to(device)
            g_start = datetime.datetime.now()
            #gpk.spmmw_op2d(G, X_dl, Y_dl, res_dl, gone.enumOP.eSUM, reverse)
            #gp_apis.gp_gspmmw2d(G, X, dim0, dim1, gone.enumOP.eSUM, reverse, device)
            gp_apis.gp_gspmmw_op2d(G, X, Y, dim0, dim1, dim2, gone.enumOP.eSUM, reverse, device)
            torch.cuda.synchronize()
            g_end = datetime.datetime.now()
            diff = g_end - g_start
            print ('spmmw_op2d time is:', diff)
            time.sleep(3)
            g_start = datetime.datetime.now()
            #gpk.spmmw_op2d(G, X_dl, Y_dl, res_dl, gone.enumOP.eSUM, reverse)
            res = gp_apis.gp_gspmmw_op2d(G, X, Y, dim0, dim1, dim2, gone.enumOP.eSUM, reverse, device)
            torch.cuda.synchronize()
            g_end = datetime.datetime.now()
            diff = g_end - g_start
            print ('spmmw_op2d time is:', diff)
            #print("the num_heads is ",num_heads)
            #torch.save(res, 'spmmw_op_res.pt')
            print("res is", res)
            #torch.save(res, 'pubmed/spmmw_op2d_result_new.pt')

        
         
            #spmmw2d
            dim0 = num_vcount
            dim1 = 1
            dim2 = 1
            X = torch.rand(num_ecount, num_heads)
            #X = torch.load('/home/ygong07/GraphPy_2d_partition/build/reddit/spmmw2d_X.pt')
            X = X.to(device)
            #torch.save(X, 'pubmed/spmmw2d_X.pt')
            res = torch.zeros(dim0, num_heads, dim2)
            res = res.to(device)
            g_start = datetime.datetime.now()
            #gpk.spmmw2d(G, X_dl, res_dl, gone.enumOP.eSUM, reverse)
            gp_apis.gp_gspmmw2d(G, X, dim0, dim1, gone.enumOP.eSUM, reverse, device)
            torch.cuda.synchronize()
            g_end = datetime.datetime.now()
            diff = g_end - g_start
            print ('spmmw2d time is:', diff)
            time.sleep(3)
            g_start = datetime.datetime.now()
            #gpk.spmmw2d(G, X_dl, res_dl, gone.enumOP.eSUM, reverse)
            res = gp_apis.gp_gspmmw2d(G, X, dim0, dim1, gone.enumOP.eSUM, reverse, device)
            torch.cuda.synchronize()
            g_end = datetime.datetime.now()
            diff = g_end - g_start
            print ('spmmw2d time is:', diff)
            #print("the num_heads is ",num_heads)
            print("result", res)
            #torch.save(res, 'pubmed/spmmw2d_result.pt')

        
            # sddmme2d
            dim0 = num_ecount
            dim1 = 1
            X = torch.rand(num_vcount, num_heads, 1)
            #torch.save(X, 'pubmed/sddmme2d_X.pt')
            #X = torch.load('/home/ygong07/GraphPy_2d_partition/build/reddit/sddmme2d_X.pt')
            #print("X is", X)
            X = X.to(device)
            #X_dl = torch.utils.dlpack.to_dlpack(X)
            Y = torch.rand(num_vcount, num_heads, 1)
            #torch.save(Y, 'pubmed/sddmme2d_Y.pt')
            #Y = torch.load('/home/ygong07/GraphPy_2d_partition/build/reddit/sddmme2d_Y.pt')
            #print("Y is", Y)
            Y = Y.to(device)
            #Y_dl = torch.utils.dlpack.to_dlpack(Y)
            res = torch.zeros(dim0, num_heads)
            res = res.to(device)
            #res_dl = torch.utils.dlpack.to_dlpack(res)
            g_start = datetime.datetime.now()
            #gpk.gsddmme2d(G, X_dl, Y_dl, res_dl, gone.enumOP.eSUM, reverse)
            gp_apis.gp_gsddmme2d(G, X, Y, dim0, dim1, gone.enumOP.eSUM, reverse, device)
            torch.cuda.synchronize()
            g_end = datetime.datetime.now()
            diff = g_end - g_start
            print ('sddmme2d SUM time is:', diff)
            time.sleep(3)
            g_start = datetime.datetime.now()
            #gpk.gsddmme2d(G, X_dl, Y_dl, res_dl, gone.enumOP.eSUM, reverse)
            res = gp_apis.gp_gsddmme2d(G, X, Y, dim0, dim1, gone.enumOP.eSUM, reverse, device)
            torch.cuda.synchronize()
            g_end = datetime.datetime.now()
            diff = g_end - g_start
            print ('sddmme2d SUM time is:', diff)
            #print("the num_heads is ",num_heads)
            print("result", res)
            #torch.save(res, 'pubmed/sddmme2d_result.pt')

            
            # sddmm2d
            dim0 = num_ecount
            dim1 = 1
            X = torch.rand(num_vcount, num_heads, 1)
            #torch.save(X, 'pubmed/sddmm2d_X.pt')
            #X = torch.load('/home/ygong07/GraphPy_2d_partition/build/reddit/sddmm2d_X.pt')
            X = X.to(device)
            #X_dl = torch.utils.dlpack.to_dlpack(X)
            Y = torch.ones(num_ecount, num_heads)
            #torch.save(Y, 'pubmed/sddmm2d_Y.pt')
            #Y = torch.load('/home/ygong07/GraphPy_2d_partition/build/reddit/sddmm2d_Y.pt')
            Y = Y.to(device)
            #Y_dl = torch.utils.dlpack.to_dlpack(Y)
            res = torch.zeros(dim0, num_heads)
            res = res.to(device)
            #res_dl = torch.utils.dlpack.to_dlpack(res)
            g_start = datetime.datetime.now()
            #gpk.sddmm2d(G, X_dl, Y_dl, res_dl, gone.enumOP.eSUB, reverse)
            res = gp_apis.gp_gsddmm2d(G, X, Y, dim0, dim1, gone.enumOP.eSUB, reverse, device)
            torch.cuda.synchronize()
            g_end = datetime.datetime.now()
            diff = g_end - g_start
            print ('sddmm2d SUB time is:', diff)
            time.sleep(3)
            g_start = datetime.datetime.now()
            #gpk.sddmm2d(G, X_dl, Y_dl, res_dl, gone.enumOP.eSUB, reverse)
            gp_apis.gp_gsddmm2d(G, X, Y, dim0, dim1, gone.enumOP.eSUB, reverse, device)
            torch.cuda.synchronize()
            g_end = datetime.datetime.now()
            diff = g_end - g_start
            print ('sddmm2d SUB time is:', diff)
            #print("the num_heads is ",num_heads)
            print("res",res)
            #torch.save(res, 'pubmed/sddmm2d_result.pt')

