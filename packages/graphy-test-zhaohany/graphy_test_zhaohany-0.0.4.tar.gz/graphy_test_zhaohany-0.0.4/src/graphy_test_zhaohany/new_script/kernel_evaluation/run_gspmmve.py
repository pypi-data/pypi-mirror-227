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
    parser.add_argument('--feat', type=int, default= 32, help='feature size')

    args = parser.parse_args()
    
    # Select Device
    use_cuda = args.device == 'GPU' and torch.cuda.is_available()
    device = torch.device('cuda' if use_cuda else 'cpu')
    if use_cuda:
        print("Using CUDA!")
    else:
        print('Not using CUDA!!!')

    ofile = args.gdir

    #G = kernel.load_graph_noeid(ofile);
    G = kernel.load_graph(ofile);

    num_vcount = G.get_vcount()
    num_ecount = G.get_edge_count()
    print("num_vcount, num_ecount are:", num_vcount, num_ecount)
    torch.set_printoptions(edgeitems=10)

    
    #num_heads = 1
    hidden_feature = args.feat
    
    print(num_vcount, num_ecount)
    print("begin test kernel(1d)")
    reverse = 0
            
    # gspmmw_op2d
    dim0 = num_vcount
    #dim1 = num_heads
    dim2 = hidden_feature
    X = torch.rand(num_vcount, hidden_feature)
    #torch.save(X, 'spmmve_X.pt')
    #X = torch.load('spmmve_X.pt')
    #print("X is", X.size())
    X = X.to(device)
    X1 = torch.rand(num_vcount, 9)
    X1 = X1.to(device)
    Y = torch.ones(num_ecount, 1)
    #torch.save(Y, 'spmmve_Y.pt')
    #Y = torch.load('spmmve_Y.pt')
    #Y = torch.load('/home/ygong07/GraphPy_2d_partition/build/pubmed/spmmw_op2d_Y.pt')
    Y = Y.to(device)
    Y1 = torch.ones(num_ecount, 1)
    Y1 = Y1.to(device)
    g_start = datetime.datetime.now()
    res = gp_apis.gp_gspmmw_op(G, X, Y, dim0, dim2, gone.enumOP.eSUM, reverse, device)
    res1 = gp_apis.gp_gspmmw_op(G, X1, Y1, dim0, 9, gone.enumOP.eSUM, reverse, device)
    torch.cuda.synchronize()
    g_end = datetime.datetime.now()
    diff = g_end - g_start
    print ('spmmw_op 1nd time is:', diff)
    #print(res);
    #print("the num_heads is ",num_heads)
    #torch.save(res, 'spmmve_rst_0.pt')
    #torch.save(res, 'pubmed/spmmw_op2d_result_new.pt')


    # gspmmw_op2d
    dim0 = num_vcount
    #dim1 = num_heads
    dim2 = hidden_feature
    X = torch.rand(num_vcount, hidden_feature)
    #torch.save(X, 'spmmve_X.pt')
    #X = torch.load('spmmve_X.pt')
    #print("X is", X.size())
    X = X.to(device)
    X1 = torch.rand(num_vcount, 9)
    X1 = X1.to(device)
    Y = torch.ones(num_ecount, 1)
    Y1 = torch.ones(num_ecount, 1)
    Y1 = Y1.to(device)
    #torch.save(Y, 'spmmve_Y.pt')
    #Y = torch.load('spmmve_Y.pt')
    #Y = torch.load('/home/ygong07/GraphPy_2d_partition/build/pubmed/spmmw_op2d_Y.pt')
    Y = Y.to(device)
    g_start = datetime.datetime.now()
    res = gp_apis.gp_gspmmw_op(G, X, Y, dim0, dim2, gone.enumOP.eSUM, reverse, device)
    res1 = gp_apis.gp_gspmmw_op(G, X1, Y1, dim0, 9, gone.enumOP.eSUM, reverse, device)
    torch.cuda.synchronize()
    g_end = datetime.datetime.now()
    diff = g_end - g_start
    print ('spmmw_op 2nd time is:', diff)
    #print(res);
    #print("the num_heads is ",num_heads)

    # gspmmw_op2d
    dim0 = num_vcount
    #dim1 = num_heads
    dim2 = hidden_feature
    X = torch.rand(num_vcount, hidden_feature)
    #torch.save(X, 'spmmve_X.pt')
    #X = torch.load('spmmve_X.pt')
    #print("X is", X.size())
    X = X.to(device)
    X1 = torch.rand(num_vcount, 9)
    X1 = X1.to(device)
    Y = torch.ones(num_ecount, 1)
    #torch.save(Y, 'spmmve_Y.pt')
    #Y = torch.load('spmmve_Y.pt')
    #Y = torch.load('/home/ygong07/GraphPy_2d_partition/build/pubmed/spmmw_op2d_Y.pt')
    Y = Y.to(device)
    Y1 = torch.ones(num_ecount, 1)
    Y1 = Y1.to(device)
    g_start = datetime.datetime.now()
    res = gp_apis.gp_gspmmw_op(G, X, Y, dim0, dim2, gone.enumOP.eSUM, reverse, device)
    res1 = gp_apis.gp_gspmmw_op(G, X1, Y1, dim0, 9, gone.enumOP.eSUM, reverse, device)
    torch.cuda.synchronize()
    g_end = datetime.datetime.now()
    diff = g_end - g_start
    print ('spmmw_op 1nd time is:', diff)
    #print(res);
    #print("the num_heads is ",num_heads)
    
    """
    if (reverse == 0):
        saved_rst = torch.load('spmmve_rst_0.pt')
    else:
        saved_rst = torch.load('spmmve_rst_1.pt')
    same = torch.all(res.eq(saved_rst))
    print("whterh the compare result are the same", same)

    loc_array = res.eq(saved_rst)
    print(loc_array)
    rst_flat = torch.flatten(res).tolist()
    saved_rst_flat = torch.flatten(saved_rst).tolist()
    different_list = []
    for i in range(len(rst_flat)):
        #if rst_flat[i] != saved_rst_flat[i]:
        different_list.append((rst_flat[i] - saved_rst_flat[i]))
    #print("diff list", different_list)
    print("max diff", max(different_list))  
    max_i = different_list.index(max(different_list))
    print("index is", max_i)
    print("node value for index", rst_flat[max_i], saved_rst_flat[max_i])
    """
