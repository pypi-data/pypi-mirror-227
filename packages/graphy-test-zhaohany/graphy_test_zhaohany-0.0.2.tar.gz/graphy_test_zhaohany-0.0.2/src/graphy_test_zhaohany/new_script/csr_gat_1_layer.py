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
import sys

if __name__ == "__main__":
    #ingestion_flag = gone.enumGraph.eDdir | gone.enumGraph.eDoubleEdge | gone.enumGraph.eCreateEID | gone.enumGraph.eBinarySource
    ifile = "/mnt/huge_26TB/data/test2/reddit/binary_graph/"
    #num_vcount = 232965
    #ifile = "/home/datalab/data/test2/cora/graph_structure/"
    #num_vcount = 2708
    #ifile = "/home/ygong07/data/test2/pubmed/graph_structure/"
    #ifile = "/home/ygong07/data/test2/pubmed/graph_structure/"
  
    #num_vcount = 19717
    #G = cg.create_csr_graph(ifile, num_vcount, ingestion_flag)
 
    ofile = ifile + "../saved_graph/"
    G = gpk.load_graph(ofile);
    num_vcount = G.get_vcount();
    #input_feature_dim = 602
    torch.set_printoptions(edgeitems=20)
 

    num_ecount = G.get_edge_count()
    hidden_feature = 1
    num_heads = 1

    # sddmme
    dim0 = num_ecount
    dim1 = 1
    #X = torch.rand(num_vcount, 1)
    X = torch.load('/home/ygong07/GraphPy_workflow/new_script/reddit/sddmme2d_X.pt')
    #X = torch.load('/home/ygong07/GraphPy_2d_partition_CPU/new_script/pubmed/sddmme2d_X.pt')
    #print("X", X)
    X_dl = torch.utils.dlpack.to_dlpack(X)
    #Y = torch.rand(num_vcount, 1)
    Y = torch.load('/home/ygong07/GraphPy_workflow/new_script/reddit/sddmme2d_Y.pt')
    #Y = torch.load('/home/ygong07/GraphPy_2d_partition_CPU/new_script/pubmed/sddmme2d_Y.pt')
    #print("Y",Y)
    Y_dl = torch.utils.dlpack.to_dlpack(Y)
  
    res = torch.zeros(dim0, num_heads)
    res_dl = torch.utils.dlpack.to_dlpack(res)
    g_start = datetime.datetime.now()
    gpk.gsddmme2d(G, X_dl, Y_dl, res_dl, gone.enumOP.eSUM, 0)
    g_end = datetime.datetime.now()
    diff = g_end - g_start
    print ('sddmme time is:', diff) 
    #values, indices = torch.sort(res, dim= 0)
    #print("sddmme", values)
    #sys.exit()


    #spmmw
    dim0 = num_vcount
    dim1 = 1
    #X = torch.rand(num_ecount, 1)
    #X = torch.load('/home/ygong07/GraphPy_2d_partition_CPU/new_script/reddit/spmmw2d_X.pt')
    X = res

    X_dl = torch.utils.dlpack.to_dlpack(X)

    res1 = torch.zeros(dim0, num_heads, dim1)
    res_dl = torch.utils.dlpack.to_dlpack(res1)
    g_start = datetime.datetime.now()
    gpk.spmmw2d(G, X_dl, res_dl, gone.enumOP.eMAX, 0)
    g_end = datetime.datetime.now()
    diff = g_end - g_start
    print ('spmmw time is:', diff) 
    #res_load = torch.load('/home/ygong07/GraphPy_2d_partition_CPU/new_script/reddit/spmmw2d_result.pt')
    #values, indices = torch.sort(res1, dim= 0)
    #print("spmmw", values)
    #print("spmmw", res1)
    #res_load = torch.load('/home/ygong07/GraphPy_workflow/new_script/reddit/spmmw_res.pt')
    #print("spmmw results are the same", torch.all(res_load.eq(values)))



    #sys.exit()

    # sddmm
    dim0 = num_ecount
    dim1 = 1
    #X = torch.rand(num_vcount, 1)
    #X = torch.load('/home/ygong07/GraphPy_2d_partition_CPU/new_script/reddit/sddmm2d_X.pt')
    #X = torch.load('/home/ygong07/GraphPy_2d_partition_CPU/new_script/pubmed/sddmm2d_X.pt')
    #print("X", X)
    X = res1
    X_dl = torch.utils.dlpack.to_dlpack(X)
    #Y = torch.rand(num_ecount, 1)
    #Y = torch.load('/home/ygong07/GraphPy_2d_partition_CPU/new_script/reddit/sddmm2d_Y.pt')
    #Y = torch.load('/home/ygong07/GraphPy_2d_partition_CPU/new_script/pubmed/sddmm2d_Y.pt')
    #print("Y", Y)
    Y = res
    Y_dl = torch.utils.dlpack.to_dlpack(Y)
    res = torch.zeros(dim0, num_heads)
    res_dl = torch.utils.dlpack.to_dlpack(res)
    g_start = datetime.datetime.now()
    gpk.sddmm2d(G, X_dl, Y_dl, res_dl, gone.enumOP.eSUB, 0)
    """ 
    temp = res.tolist()
    print ("start")
    for each in temp:
        #print(len(each))
        if each[0] < 0:
            print(each)
    print("end")
    """
    if (torch.any(res > 0)):
        print("csr has eSUB problem")
    g_end = datetime.datetime.now()
    diff = g_end - g_start
    #print ('sddmm time is:', diff)
    #values, indices = torch.sort(res, dim= 0)

    # print('sddmm values', values)
    #res_load = torch.load('/home/ygong07/GraphPy_2d_partition_CPU/new_script/reddit/sddmm2d_result.pt')
    #values, indices = torch.sort(res, dim= 0)
    #print("sddmm res", values)
    #print("spmmw", res1)
    #res_load = torch.load('/home/ygong07/GraphPy_workflow/new_script/reddit/sddmm_res.pt')
    #print("spmmw results are the same", torch.all(res_load.eq(values)))

    #sys.exit()





    score_exp = torch.exp(res)
    #spmmw
    dim0 = num_vcount
    dim1 = 1
    #X = torch.rand(num_ecount, 1)
    #X = torch.load('/home/ygong07/GraphPy_2d_partition_CPU/new_script/reddit/spmmw2d_X.pt')
    X = score_exp

    X_dl = torch.utils.dlpack.to_dlpack(X)

    res2 = torch.zeros(dim0, num_heads, dim1)
    res_dl = torch.utils.dlpack.to_dlpack(res2)
    g_start = datetime.datetime.now()
    gpk.spmmw2d(G, X_dl, res_dl, gone.enumOP.eSUM, 0)
    g_end = datetime.datetime.now()
    diff = g_end - g_start
    #print ('spmmw time is:', diff) 


    # sddmm
    dim0 = num_ecount
    dim1 = 1
    #X = torch.rand(num_vcount, 1)
    #X = torch.load('/home/ygong07/GraphPy_2d_partition_CPU/new_script/reddit/sddmm2d_X.pt')
    #X = torch.load('/home/ygong07/GraphPy_2d_partition_CPU/new_script/pubmed/sddmm2d_X.pt')
    #print("X", X)
    X = res2
    X_dl = torch.utils.dlpack.to_dlpack(X)
    #Y = torch.rand(num_ecount, 1)
    #Y = torch.load('/home/ygong07/GraphPy_2d_partition_CPU/new_script/reddit/sddmm2d_Y.pt')
    #Y = torch.load('/home/ygong07/GraphPy_2d_partition_CPU/new_script/pubmed/sddmm2d_Y.pt')
    #print("Y", Y)
    Y = score_exp
    Y_dl = torch.utils.dlpack.to_dlpack(Y)
    res_fin = torch.zeros(dim0, num_heads)
    res_dl = torch.utils.dlpack.to_dlpack(res_fin)
    g_start = datetime.datetime.now()
    gpk.sddmm2d(G, X_dl, Y_dl, res_dl, gone.enumOP.eDIV, 0)
    g_end = datetime.datetime.now()
    diff = g_end - g_start
    #print ('sddmm time is:', diff)

    #print('sddmm values', values)
    #res_load = torch.load('/home/ygong07/GraphPy_2d_partition_CPU/new_script/reddit/sddmm2d_result.pt')
    #values, indices = torch.sort(res, dim= 0)
    #print(values)
    # torch.save(res, 'pubmed/spmmw_op2d_result_new.pt')
    #res_load = torch.load('/home/ygong07/GraphPy_workflow/new_script/reddit/sddmm_res.pt')
    #print("sddmm results are the same", torch.all(res_load.eq(values)))

    #sys.exit()



   
    # gspmmw_op2d
    dim0 = num_vcount
    dim1 = num_heads
    dim2 = hidden_feature
    #num_vcount = 232965
    #hidden_feature = 16
    #num_ecount = 229231784
    X = torch.ones(num_vcount, num_heads, hidden_feature)
    #torch.save(X, 'reddit/spmmw_op2d_X.pt')
        #X = torch.load('/home/ygong07/GraphPy_2d_partition/build/pubmed/spmmw_op2d_X.pt')
    #print("X is", X.size())
    #X = X.to(cuda)
    X_dl = torch.utils.dlpack.to_dlpack(X)
    Y = res_fin
    #Y = 0.5 * Y
    #torch.save(Y, 'reddit/spmmw_op2d_Y.pt')
    # torch.save(Y, 'pubmed/spmmw_op2d_Y.pt')
    #Y = torch.load('/home/ygong07/GraphPy_2d_partition/build/pubmed/spmmw_op2d_Y.pt')
    #Y = Y.to(cuda)
    Y_dl = torch.utils.dlpack.to_dlpack(Y)
    res = torch.zeros(dim0, num_heads, hidden_feature)
    res_dl = torch.utils.dlpack.to_dlpack(res)
    g_start = datetime.datetime.now()
    gpk.spmmw_op2d(G, X_dl, Y_dl, res_dl, gone.enumOP.eSUM, 0)
    g_end = datetime.datetime.now()
    diff = g_end - g_start
    print ('spmmw_op time is:', diff)
    #print("the num_heads is ",num_heads)
    #torch.save(res, 'pubmed/spmmw_op_res.pt')
    #print("res is", res.isnan().any())
    values, indices = torch.sort(res, dim= 0)
    #print(values)
    # torch.save(res, 'pubmed/spmmw_op2d_result_new.pt')
    res_load = torch.load('/home/ygong07/GraphPy_workflow/new_script/reddit/spmmw_op2d_result_new.pt')
    values_load, indices_load = torch.sort(res_load, dim= 0)
    #print("spmmw_op2d results are the same", torch.all(res_load.eq(values)))
    c = values - values_load
    values1, indices = torch.sort(c, dim= 0)

    print("values1", values1)



