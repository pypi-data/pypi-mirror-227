
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
    #check gcn kernel
    
    # Select Device
    use_cuda = args.device == 'GPU' and torch.cuda.is_available()
    device = torch.device('cuda' if use_cuda else 'cpu')
    if use_cuda:
        print("Using CUDA!")
    else:
        print('Not using CUDA!!!')

    ofile = args.gdir

    G = kernel.load_graph_noeid(ofile);

    num_vcount = G.get_vcount()
    num_ecount = G.get_edge_count()
    print("num_vcount, num_ecount are:", num_vcount, num_ecount)
    torch.set_printoptions(edgeitems=2)

    hidden_feature = args.feat
    print(num_vcount, num_ecount)
    print("begin test kernel(3d)")
    reverse = 0
        
    dim0 = num_vcount
    dim1 = hidden_feature
    X = torch.ones(dim0, dim1)
    #torch.save(X, 'data_save/X_file.pt')
    X = X.to(device)
    norm = 0
    g_start = datetime.datetime.now()
    res = gp_apis.gp_gspmm(G, X, dim0, dim1, reverse, norm, device)
    torch.cuda.synchronize()
    g_end = datetime.datetime.now()
    diff = g_end - g_start
    print ('spmm time is:', diff)
    print("res is", res)

    g_start = datetime.datetime.now()
    res = gp_apis.gp_gspmm(G, X, dim0, dim1, reverse, norm, device)
    torch.cuda.synchronize()
    g_end = datetime.datetime.now()
    diff = g_end - g_start
    print ('spmm time is:', diff)

    print("res is", res)
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
