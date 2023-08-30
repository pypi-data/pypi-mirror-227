
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

    G = kernel.load_graph(ofile);

    num_vcount = G.get_vcount()
    num_ecount = G.get_edge_count()
    print("num_vcount, num_ecount are:", num_vcount, num_ecount)
    torch.set_printoptions(edgeitems=10)

    hidden_feature = args.feat
    print(num_vcount, num_ecount)
    reverse = 0
        
    dim0 = num_ecount
    dim1 = 1
    X = torch.rand(num_vcount, 1)
    #torch.save(X, 'sddmmve_X.pt')
    #X = torch.load('sddmmve_X.pt')
    X = X.to(device)
    
    Y = torch.rand(num_ecount, 1)
    #torch.save(Y, 'sddmmve_Y.pt')
    #Y = torch.load('sddmmve_Y.pt')
    Y = Y.to(device)
    
    g_start = datetime.datetime.now()
    #gpk.gsddmm(G, X_dl, Y_dl, res_dl, gone.enumOP.eSUB, reverse, device)
    rst = gp_apis.gp_gsddmm(G, X, Y, num_ecount, dim1, gone.enumOP.eMUL, reverse, device)
    torch.cuda.synchronize()
    g_end = datetime.datetime.now()
    diff = g_end - g_start

    print ('sddmm time is:', diff)
    print(rst)

    g_start = datetime.datetime.now()
    #gpk.gsddmm(G, X_dl, Y_dl, res_dl, gone.enumOP.eSUB, reverse, device)
    rst = gp_apis.gp_gsddmm(G, X, Y, num_ecount, dim1, gone.enumOP.eMUL, reverse, device)
    torch.cuda.synchronize()
    g_end = datetime.datetime.now()
    diff = g_end - g_start

    print ('sddmm time is:', diff)
    
    g_start = datetime.datetime.now()
    #gpk.gsddmm(G, X_dl, Y_dl, res_dl, gone.enumOP.eSUB, reverse, device)
    rst = gp_apis.gp_gsddmm(G, X, Y, num_ecount, dim1, gone.enumOP.eMUL, reverse, device)
    torch.cuda.synchronize()
    g_end = datetime.datetime.now()
    diff = g_end - g_start

    print ('sddmm time is:', diff)

    """
    if (reverse == 0):
        saved_rst = torch.load('sddmmve_rst_MUL.pt')
    #else:
        #saved_rst = torch.load('sddmmve_rst_1.pt')
    same = torch.all(rst.eq(saved_rst))
    print("whterh the compare result are the same", same)
    
    #torch.save(rst, 'sddmmve_rst_DIV.pt')
    """

