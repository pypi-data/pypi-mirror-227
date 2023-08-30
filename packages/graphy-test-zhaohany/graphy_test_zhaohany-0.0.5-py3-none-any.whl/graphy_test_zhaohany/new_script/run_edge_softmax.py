
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
    parser.add_argument('--feat', type=int, default= 1, help='feature size')

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

    G = kernel.load_graph(ofile)

    num_vcount = G.get_vcount()
    num_ecount = G.get_edge_count()
    print("num_vcount, num_ecount are:", num_vcount, num_ecount)
    torch.set_printoptions(edgeitems=10)

    hidden_feature = args.feat
    print(num_vcount, num_ecount)
    reverse = 0
        
    dim0 = num_ecount
    dim1 = hidden_feature
    # X = torch.rand(num_vcount, dim0)
    # torch.save(X, 'X_file.pt')
    X = torch.load('X_file.pt')
    X = X.to(device)
    # Y = torch.rand(num_vcount, dim0)
    # torch.save(X, 'Y_file.pt')
    Y = torch.load('Y_file.pt')
    Y = Y.to(device)
    
    
    g_start = datetime.datetime.now()
    rst = gp_apis.gp_edge_softmax_forward(G, X, dim0, dim1, reverse, device)
    torch.cuda.synchronize()
    g_end = datetime.datetime.now()
    diff = g_end - g_start
    print ('forward time is:', diff)
    print(rst)
    print("size", rst.size())
   
    g_start = datetime.datetime.now()
    rst = gp_apis.gp_edge_softmax_backward(G, X, Y, dim0, dim1, reverse, device)
    torch.cuda.synchronize()
    g_end = datetime.datetime.now()
    diff = g_end - g_start
    print ('backward time is:', diff)
    print(rst)
    print("size", rst.size())

    """
    if (reverse == 0):
        saved_rst = torch.load('sddmmvv_rst_MUL.pt')
    same = torch.all(rst.eq(saved_rst))
    print("whterh the compare result are the same", same)
    """
    # torch.save(rst, 'X.pt')

