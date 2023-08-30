import torch
import datetime

import pygraph as gone
import kernel_big as gpk
import argparse
import gp_apis_big as gp_apis

if __name__ == "__main__":
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
    ofile = ifile + "../save_big_graph/"
    
    #ifile = "/home/ygong07/data/test2/pubmed/"
    #ofile = ifile + "saved_graph/"

    #ifile = "/home/ygong07/data/test2/cora/"
    #ofile = ifile + "saved_graph/"
    
    #ifile = "/home/ygong07/data/test2/citeseer/graph_structure"
    #num_vcount = 3327

    if test_gcn:
        G = gpk.load_graph_noeid(ofile);
    else:
        G = gpk.load_graph(ofile);

    num_vcount = G.get_vcount()
    num_ecount = G.get_edge_count()
    print("num_vcount, num_ecount are:", num_vcount, num_ecount)
    print("load graph successfully")
    torch.set_printoptions(edgeitems=5)

    print("graph is success")
    
    num_heads_list = [1]
    hidden_feature = 16
    
    print("begin test kernel(3d)")
    reverse = 0
    for num_heads in num_heads_list:
        if test_gcn:
        
            dim0 = num_vcount
            dim1 = hidden_feature
            X = torch.load('data_save/spmm_X.pt')
            X = X.to(device)
            norm = 1
            g_start = datetime.datetime.now()
            res = gp_apis.gp_gspmm(G, X, dim0, dim1, reverse, norm, device)
            torch.cuda.synchronize()
            g_end = datetime.datetime.now()
            diff = g_end - g_start
            print ('spmm time is:', diff)
            print("res is", res)
            res_old = torch.load('data_save/spmm_res.pt')
            comp = torch.sub(res - res_old.to(device));
            print(comp.all());

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
            """
            # gspmmw_op2d
            dim0 = num_vcount
            dim1 = num_heads
            dim2 = hidden_feature
            X = torch.load('data_save/spmmw_op2d_X.pt')
            #print("X is", X.size())
            X = X.to(device)
            Y = torch.load('data_save/spmmw_op2d_Y.pt')
            Y = Y.to(device)
            g_start = datetime.datetime.now()
            res = gp_apis.gp_gspmmw_op2d(G, X, Y, dim0, dim1, dim2, gone.enumOP.eSUM, reverse, device)
            torch.cuda.synchronize()
            g_end = datetime.datetime.now()
            diff = g_end - g_start
            print ('spmmw_op2d time is:', diff)
            print("res is", res)
            res_old = torch.load('data_save/spmmw_op2d_res.pt')
            comp = torch.sub(res - res_old.to(device));
            print(comp.all());
            
            # sddmm2d
            dim0 = num_ecount
            dim1 = 1
            X = torch.load('data_save/sddmm2d_X.pt')
            X = X.to(device)
            Y = torch.load('data_save/sddmm2d_Y.pt')
            Y = Y.to(device)
            g_start = datetime.datetime.now()
            res = gp_apis.gp_gsddmm2d(G, X, Y, dim0, dim1, gone.enumOP.eSUB, reverse, device)
            torch.cuda.synchronize()
            g_end = datetime.datetime.now()
            diff = g_end - g_start
            print ('sddmm2d SUB time is:', diff)
            res_old = torch.load('data_save/sddmm2d_res.pt')
            comp = torch.sub(res - res_old.to(device));
            print(comp.all());

            # sddmme2d
            dim0 = num_ecount
            dim1 = 1
            X = torch.load('data_save/sddmme2d_X.pt')
            X = X.to(device)
            Y = torch.load('data_save/sddmme2d_Y.pt')
            Y = Y.to(device)
            g_start = datetime.datetime.now()
            res = gp_apis.gp_gsddmme2d(G, X, Y, dim0, dim1, gone.enumOP.eSUM, reverse, device)
            torch.cuda.synchronize()
            g_end = datetime.datetime.now()
            diff = g_end - g_start
            print ('sddmme2d SUM time is:', diff)
            #print("result", res)
            res_old = torch.load('data_save/sddmme2d_res.pt')
            sort_res_old, index_old = torch.sort(res_old, 0)
            sort_res, index = torch.sort(res, 0)
            print(sort_res)
            print(sort_res_old)
            comp = torch.sub(sort_res, sort_res_old.to(device));
            print(comp);
            print(torch.max(comp));
            print(torch.min(comp));
            #print(False != comp.all());
            """
         
            #spmmw2d
            dim0 = num_vcount
            dim1 = 1
            dim2 = 1
            X = torch.load('data_save/spmmw2d_X.pt')
            X = X.to(device)
            g_start = datetime.datetime.now()
            res = gp_apis.gp_gspmmw2d(G, X, dim0, dim1, gone.enumOP.eMAX, reverse, device)
            torch.cuda.synchronize()
            g_end = datetime.datetime.now()
            diff = g_end - g_start
            print ('spmmw2d time is:', diff)
            
            print("result", res.size(), res)
            #res_old = torch.load('data_save/spmmw2d_res.pt')
            #comp = torch.sub(res.to('cpu'), res_old);
            #print(comp)
            #print(comp.all());

