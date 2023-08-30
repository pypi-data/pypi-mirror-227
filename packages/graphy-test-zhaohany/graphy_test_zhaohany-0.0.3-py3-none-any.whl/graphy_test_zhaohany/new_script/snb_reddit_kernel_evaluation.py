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

if __name__ == "__main__":
    ingestion_flag = gone.enumGraph.eUdir | gone.enumGraph.eDoubleEdge | gone.enumGraph.eSNB
    ifile = "/home/datalab/data/test2/reddit/graph_structure/"
    num_vcount = 232965
    #ifile = "/home/datalab/data/test2/cora/graph_structure"
    #num_vcount = 2708
    #ifile = "/home/datalab/data/test2/pubmed/graph_structure"
    #num_vcount = 19717
    # ifile = "/home/datalab/data/test3/amazon"
    # num_vcount = 400727

    G = cg.create_snb_graph(ifile, num_vcount, ingestion_flag)

    input_feature_dim = 602
    


    num_ecount = G.get_edge_count()
    hidden_feature = 16
    print("ha?", num_ecount)
    # gspmmw_op
    dim0 = num_vcount
    dim1 = hidden_feature
    X = torch.rand(num_vcount, hidden_feature)
    X_dl = torch.utils.dlpack.to_dlpack(X)
    Y = torch.rand(num_ecount, 1)
    Y_dl = torch.utils.dlpack.to_dlpack(Y)

    res = torch.zeros(dim0, dim1)
    res_dl = torch.utils.dlpack.to_dlpack(res)
    g_start = datetime.datetime.now()
    gpk.gspmmw_op(G, X_dl, Y_dl, res_dl, gone.enumOP.eSUM, 1)
    g_end = datetime.datetime.now()
    diff = g_end - g_start
    print ('spmmw_op time is:', diff)

    #spmmw
    dim0 = num_vcount
    dim1 = 1
    X = torch.rand(num_ecount, 1)
    X_dl = torch.utils.dlpack.to_dlpack(X)
    res = torch.zeros(dim0, dim1)
    res_dl = torch.utils.dlpack.to_dlpack(res)
    g_start = datetime.datetime.now()
    gpk.gspmmw(G, X_dl, res_dl, gone.enumOP.eMAX, 1)
    g_end = datetime.datetime.now()
    diff = g_end - g_start
    print ('spmmw time is:', diff)

    # sddmme
    dim0 = num_ecount
    dim1 = 1
    X = torch.rand(num_vcount, 1)
    X_dl = torch.utils.dlpack.to_dlpack(X)
    Y = torch.rand(num_vcount, 1)
    Y_dl = torch.utils.dlpack.to_dlpack(Y)

    res = torch.zeros(dim0, dim1)
    res_dl = torch.utils.dlpack.to_dlpack(res)
    g_start = datetime.datetime.now()
    gpk.gsddmme(G, X_dl, Y_dl, res_dl, gone.enumOP.eSUM, 1)
    g_end = datetime.datetime.now()
    diff = g_end - g_start
    print ('sddmme time is:', diff)

    # sddmm
    dim0 = num_ecount
    dim1 = 1
    X = torch.rand(num_vcount, 1)
    X_dl = torch.utils.dlpack.to_dlpack(X)
    Y = torch.rand(num_ecount, 1)
    Y_dl = torch.utils.dlpack.to_dlpack(Y)

    res = torch.zeros(dim0, dim1)
    res_dl = torch.utils.dlpack.to_dlpack(res)
    g_start = datetime.datetime.now()
    gpk.gsddmm(G, X_dl, Y_dl, res_dl, gone.enumOP.eSUB, 1)
    g_end = datetime.datetime.now()
    diff = g_end - g_start
    print ('sddmm time is:', diff)




    
