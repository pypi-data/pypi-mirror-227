import torch
import datetime

import pygraph as gone
import kernel
import argparse
import time
import gp_apis

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='pick CPU or GPU to perform the graph deep learning ')
    parser.add_argument('--device', type=str, default= 'GPU', help='pick CPU or GPU')
    parser.add_argument('--gdir',   type=str, help='pick saved graph dir')
    parser.add_argument('--feat', type=int, default= 16, help='feature size')

    args = parser.parse_args()
    
    # Select Device
    use_cuda = args.device == 'GPU' and torch.cuda.is_available()
    device = torch.device('cuda' if use_cuda else 'cpu')
    if use_cuda:
        print("Using CUDA!")
    else:
        print('Not using CUDA!!!')

    ofile = args.gdir

    G = kernel.load_graph(ofile);

    num_vcount = G.get_vcount()
    num_ecount = G.get_edge_count()
    print("num_vcount, num_ecount are:", num_vcount, num_ecount)
    torch.set_printoptions(edgeitems=2)

    
    num_heads = 1
    hidden_feature = args.feat
    
    print(num_vcount, num_ecount)
    print("begin test kernel(3d)")
    reverse = 0
            
    # gspmmw_op2d
    dim0 = num_vcount
    dim1 = num_heads
    dim2 = hidden_feature
    X = torch.ones(num_vcount, num_heads, hidden_feature)
    #torch.save(X, 'pubmed/spmmw_op2d_X.pt')
    #X = torch.load('/home/ygong07/GraphPy_2d_partition/build/pubmed/spmmw_op2d_X.pt')
    #print("X is", X.size())
    X = X.to(device)
    Y = torch.ones(num_ecount, num_heads)
    #torch.save(Y, 'pubmed/spmmw_op2d_Y.pt')
    #Y = torch.load('/home/ygong07/GraphPy_2d_partition/build/pubmed/spmmw_op2d_Y.pt')
    Y = Y.to(device)
    g_start = datetime.datetime.now()
    res = gp_apis.gp_gspmmw_op2d(G, X, Y, dim0, dim1, dim2, gone.enumOP.eSUM, reverse, device)
    torch.cuda.synchronize()
    g_end = datetime.datetime.now()
    diff = g_end - g_start
    print(res);
    print ('spmmw_op2d time is:', diff)
    #print("the num_heads is ",num_heads)
    #torch.save(res, 'spmmw_op_res.pt')
    #torch.save(res, 'pubmed/spmmw_op2d_result_new.pt')
    
    #time.sleep(3)
    g_start = datetime.datetime.now()
    res = gp_apis.gp_gspmmw_op2d(G, X, Y, dim0, dim1, dim2, gone.enumOP.eSUM, reverse, device)
    torch.cuda.synchronize()
    g_end = datetime.datetime.now()
    diff = g_end - g_start
    print(res)
    print ('spmmw_op2d time is:', diff)

    g_start = datetime.datetime.now()
    res = gp_apis.gp_gspmmw_op2d(G, X, Y, dim0, dim1, dim2, gone.enumOP.eSUM, reverse, device)
    torch.cuda.synchronize()
    g_end = datetime.datetime.now()
    diff = g_end - g_start
    print(res)
    print ('spmmw_op2d time is:', diff)
