import torch
import torch.nn as nn
import itertools
import torch.nn.functional as F
import datetime
import torch.utils.dlpack
import pygraph as gone
import pubmed_util
import create_graph as cg
import kernel as gpk

if __name__ == "__main__":
    ingestion_flag = gone.enumGraph.eUdir | gone.enumGraph.eBinarySource

    file_dir = "/mnt/huge_26TB/data/test2/reddit/"    
    ifile = file_dir + "binary_graph/"
    #num_vcount = 3327
    
    #ofile = ifile + "../saved_graph/"
    #G = gpk.load_graph(ofile);
    #num_vcount = G.get_vcount();

    #ifile = "/home/ygong07/data/test2/cora/graph_structure/"
    #num_vcount = 2708
    #cuda = torch.device('cuda')
    #torch.set_printoptions(edgeitems=19717)
    #ifile = "/home/datalab/data/test2/cora/graph_structure"
    #num_vcount = 2708
    #ifile = "/home/datalab/data/test2/pubmed/graph_structure"
    #num_vcount = 19717
    # ifile = "/home/datalab/data/test3/amazon"
    num_vcount = 232965
    G = cg.create_csr_graph_noeid(ifile, num_vcount, ingestion_flag)

    num_ecount = G.get_edge_count()
    dim0 = num_vcount
    dim1 = 1
    inverse = 0 
    norm = True
    #print("ha?", num_ecount)

    # gspmmw_o
    #X = torch.rand(dim0, dim1)
    X = torch.ones(dim0, dim1)
    X = X*0.3
    torch.save(X, 'test_save/gcn_X.pt')
    #X = torch.load('/home/ygong07/GraphPy_SNB_github/GraphPy_snb/build/snb_test/spmmw_op_X.pt')
    #print("X is", X)
    #print("X is", X)
    #X = X.to(cuda)
    X_dl = torch.utils.dlpack.to_dlpack(X)
    res = torch.zeros(dim0, dim1)
    res_dl = torch.utils.dlpack.to_dlpack(res)
    g_start = datetime.datetime.now()
    gpk.spmm(G, X_dl, res_dl, inverse, norm)
    g_end = datetime.datetime.now()
    diff = g_end - g_start
    #print ('spmmw_op time is:', diff)
    print ('spmmw_op result is:', res[3565])
    torch.save(res,'test_save/res.pt')

