
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
    reverse = 1
        

    #spmmw
    dim0 = num_vcount
    dim1 = hidden_feature
    #X = torch.rand(num_ecount, hidden_feature)
    #torch.save(X, 'sppmme_X.pt')
    X = torch.load('sppmme_X.pt')
    X = X.to(device)
    #X_dl = torch.utils.dlpack.to_dlpack(X)
    #res = torch.zeros(dim0, dim1)
    #res_dl = torch.utils.dlpack.to_dlpack(res)
    g_start = datetime.datetime.now()
    #gpk.gspmmw(G, X_dl, res_dl, gone.enumOP.eMAX, reverse, device)
    rst = gp_apis.gp_gspmmw(G, X, num_vcount, dim1, gone.enumOP.eSUM, reverse, device)
    torch.cuda.synchronize()
    g_end = datetime.datetime.now()
    diff = g_end - g_start
    print ('spmmw time is:', diff)
    print(rst)
    print("size", rst.size())
    
    if (reverse == 0):
        saved_rst = torch.load('spmme_rst_SUM_0.pt')
    else:
        saved_rst = torch.load('spmme_rst_SUM_1.pt')
    same = torch.all(rst.eq(saved_rst))
    print("whterh the compare result are the same", same)

    loc_array = rst.eq(saved_rst)
    print(loc_array)
    rst_flat = torch.flatten(rst).tolist()
    saved_rst_flat = torch.flatten(saved_rst).tolist()
    different_list = []
    for i in range(len(rst_flat)):
        #if rst_flat[i] != saved_rst_flat[i]:
        different_list.append(abs(rst_flat[i] - saved_rst_flat[i]))
    #print("diff list", different_list)
    print("max diff", max(different_list))   
    max_i = different_list.index(max(different_list))
    print("index is", max_i)
    print("node index is", rst_flat[max_i], saved_rst_flat[max_i])
    
    #torch.save(rst, 'spmme_rst_SUM_1.pt')
