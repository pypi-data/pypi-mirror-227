# -*- coding: utf-8 -*-
import argparse
import os
import time
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
from torchvision import datasets, transforms
from tqdm import tqdm
import itertools
from net.models import LeNet
from net.quantization import apply_weight_sharing
import util
import kernel
import datetime
import numpy as np

from scipy import sparse

import model_conv as conv
import sys
import queue
import numpy as np
import collections
import pygraph as gone


def create_csr_graph(pgraph, dd):
    #num_sources = 1
    #num_thread = 4

    #edge_dt = np.dtype([('src', np.int32), ('dst', np.int32), ('edgeid', np.int32)])
    csr_dt = np.dtype([('dst', np.int32), ('edgeid', np.int32)])
    offset_dt = np.dtype([('offset', np.int32)])

    #outdir = ""
    # graph = gone.init(1, 1, outdir, num_sources, num_thread)  # Indicate one pgraph, and one vertex type
    #tid0 = graph.init_vertex_type(num_vcount, True, "gtype") # initiate the vertex type
    #pgraph = graph.create_schema(ingestion_flag, tid0, "friend", edge_dt) # initiate the pgraph

    # creating graph directly from file requires some efforts. Hope to fix that later
    #manager = graph.get_pgraph_managerW(0) # This assumes single weighted graph, edgeid is the weight
    pgraph.add_edges(dd)  # ifile has no weights, edgeid will be generated
    pgraph.wait()  # You can't call add_edges() after wait(). The need of it will be removed in future.
    #snap_t = gone.create_static_view(pgraph, gone.enumView.eStale)
    
    offset_csr1, offset_csc1, nebrs_csr1, nebrs_csc1 = gone.create_csr_view(pgraph) 
    offset_csr = memoryview_to_np(offset_csr1, offset_dt) 
    offset_csc = memoryview_to_np(offset_csc1, offset_dt) 
    nebrs_csr = memoryview_to_np(nebrs_csr1, csr_dt) 
    nebrs_csc = memoryview_to_np(nebrs_csc1, csr_dt) 
    
    kernel_graph_flag = 0; #eADJ graph
    csr_graph = kernel.init_graph(offset_csr, nebrs_csr, offset_csc, nebrs_csc, kernel_graph_flag) 

    return csr_graph;

def memoryview_to_np(memview, nebr_dt):
    arr = np.array(memview, copy=False)
    #a = arr.view(nebr_dt).reshape(nebr_reader.get_degree())
    a = arr.view(nebr_dt)
    return a

if __name__=="__main__":
        num_sources = 1 
        num_thread = 4
        outdir = ""
        model = torch.load("/home/datalab/graphpy-workflow/model_compression/Deep-Compression-PyTorch/saves/model_after_retraining.ptmodel")
        graph = gone.init(3, 3, outdir, num_sources, num_thread)
        managers = []
        dim_list = []
        output_dim_list = []
        ingestion_flag = gone.enumGraph.eDdir
        bias_list = []

        #graph  = gone.init(2,1, outdir)
        for name, param in model.named_parameters():
            if 'weight' in name:
                tensor = param.data.cpu().numpy()
                dim_list.append(len(tensor[0]))
                output_dim_list.append(len(tensor))
                print("check num", len(tensor[0]), len(tensor))
                num_vcount = max(len(tensor[0]), len(tensor))
                #tid0 = graph.init_vertex_type(num_vcount, True, "gtype") # initiate the vertex type
                dt = np.dtype([('src', np.int32), ('dst', np.int32), ('edgeid', np.int32)])
                tid0 = graph.init_vertex_type(num_vcount, True, "gtype");
                graph_name = "friend" + str(tid0);
                pgraph = graph.create_schema(ingestion_flag, tid0, graph_name, dt);
                #pgraph2 = graph.create_schema(ingestion_flag, tid0, "friend2", dt2);
                #pgraph3 = graph.create_schema(ingestion_flag, tid0, "friend2", dt2);
                managers.append(pgraph)

            elif 'bias' in name:
                tensor = param.data.cpu().numpy()
                #print(type(tensor))
                #print(tensor.shape)
                bias = tensor.tolist()
                #print(bias[0])
                bias_list.append(bias)


        csrgraphs = []
        weight_list = []
        weight_list_leaf = []
        names = []
        #ingestion_flag = gone.enumGraph.eDdir;
        #dim_list = []
        index = 0
        for name, param in model.named_parameters():
            if 'weight' in name:
                print("name: ", name)
                names.append(name)
                dict_tensor = {}
                tensor = param.data.cpu().numpy()
                #dim_list.append(len(tensor[0]))
                #print("check num", len(tensor[0]), len(tensor))
                #num_vcount = max(len(tensor[0]), len(tensor))
                #print("num", num_vcount)
                sparse_tensor = sparse.coo_matrix(tensor)
                #index = np.row_stack((sparse_tensor.row, sparse_tensor.col))
                dt = np.dtype([('src', np.int32), ('dst', np.int32), ('weight', np.int32)])
                dd = np.zeros(len(sparse_tensor.row), dt); 
                #print("sparse_rows",sparse_tensor.row)
                edge_count = 0
                #print("111")
                for i in range(len(sparse_tensor.row)): 
                    dd[edge_count] = (sparse_tensor.row[i], sparse_tensor.col[i], edge_count)
                    edge_count += 1
                #print("edge_count", edge_count)
                pgraph = create_csr_graph(managers[index], dd)
                index = index + 1
                csrgraphs.append(pgraph)
                #print("weight type", type(sparse_tensor.data))
                #weight1 = sparse_tensor.data.tolist()
                #weight2 = np.array(weight1)
                weight = torch.tensor(sparse_tensor.data, requires_grad=True)
                #print("whether have gradient:")
                #print(weight.requires_grad)
                #print("is leaf?")
                #print(weight.is_leaf)
                #weight = torch.Tensor(weight1, requires_grad=True)
                weight = weight.reshape(len(sparse_tensor.data), 1)
                #print("weight size", weight.size())
                #print("is leaf?11")
                #print(weight1.is_leaf)
                #print(weight.is_leaf)

                weight_list.append(weight)

                #weight_list_leaf.append(weight)
            #else:
                #print(param)
                #dict[name] = param
        dict_weight = {}
        #print("333")
        #sys.exit()
        for i in range(len(csrgraphs)):

            #gview = managers[i].create_static_view(gone.enumView.eStale)

            #test_bfs(csrgraph[i], 1)
            #managers[i].run_bfs(1)
            dict_weight['data'] = weight_list[i]
            #dict_weight['gview'] = gview
        parser = argparse.ArgumentParser(description='PyTorch MNIST pruning from deep compression paper')
        parser.add_argument('--batch-size', type=int, default=50, metavar='N', help='input batch size for training (default: 50)')
        parser.add_argument('--test-batch-size', type=int, default=1000, metavar='N',
                    help='input batch size for testing (default: 1000)')
        args = parser.parse_args()
        use_cuda = 0
        kwargs = {} if use_cuda else {}
        train_loader = torch.utils.data.DataLoader(
	datasets.MNIST('data', train=True, download=True,
	       transform=transforms.Compose([transforms.ToTensor(),transforms.Normalize((0.1307,), (0.3081,))])), batch_size = args.batch_size, shuffle=True, **kwargs)

        test_loader = torch.utils.data.DataLoader(datasets.MNIST('data', train=False, transform=transforms.Compose([ transforms.ToTensor(), transforms.Normalize((0.1307,), (0.3081,))])), batch_size=args.test_batch_size, shuffle=False, **kwargs)
    # feature = torch.tensor(feature)
    # train_id = torch.tensor(train_id)
    # test_id = torch.tensor(test_id)
    # train_y_label = torch.tensor(train_y_label)
    # test_y_label = torch.tensor(test_y_label)
    
        #print("dim_list", dim_list)
        #print("output_dim_list", output_dim_list)

	# train the network
        input_feature_dim = dim_list[0]
        hidden_layer1 = dim_list[1]
        hidden_layer2 = dim_list[2]
        num_class = output_dim_list[2]
        num_layers = len(managers)
        #print("len_of_graph", len(managers))
        net = conv.Compressed_Model(csrgraphs, input_feature_dim, hidden_layer1, hidden_layer2, num_class, num_layers, weight_list, bias_list)
        #print("whether the weight is the leaf")
        #print(weight_list[0].is_leaf)
        #print(net.weight_list[0].is_leaf)
        optimizer = torch.optim.Adam(itertools.chain(net.parameters()), lr=0.01, weight_decay=5e-4)
        #optimizer = torch.optim.Adam(lr=0.01, weight_decay=5e-4)

        #print(input_X)
        #print("-------------------")
        start = datetime.datetime.now()
        for epoch in range(10):
            pbar = tqdm(enumerate(train_loader), total=len(train_loader))
            for batch_idx, (data, target) in pbar:
                #data, target = data.to(device), target.to(device)
                optimizer.zero_grad()
                #print("77777")
                #print(data.size())
                data = data.view(-1, 784)
                #print("77777")
                #print(data.size())
                print("data tensor", data)
                print("is data contains NAN?", torch.isnan(data).any())
                #sys.exit()

                logits = net.forward(data)
                #print("begin back")
                #print("output", output)
                #sys.exit()
                output = F.log_softmax(logits, 1)
                loss = F.nll_loss(output, target)
                #print("output_size", output.size())
                #print("target:", target.size())
                #print("output", output)
                #sys.exit()
                print("Epoch" + str(epoch))
                print("loss is:", loss)
                #sys.exit()
                optimizer.zero_grad()
                loss.backward()
                optimizer.step()
                if batch_idx % 10 == 0:
                    done = batch_idx * len(data)
                    percentage = 100. * batch_idx / len(train_loader)
                    pbar.set_description(f'Train Epoch: {epoch} [{done:5}/{len(train_loader.dataset)} ({percentage:3.0f}%)]  Loss: {loss.item():.6f}')




        #print('Epoch %d | Train_Loss: %.4f' % (epoch, loss.item()))

        # # check the accuracy for test data
        # logits_test = net.forward(feature)
        # logp_test = F.log_softmax(logits_test, 1)

        # acc_val = pubmed_util.accuracy(logp_test[test_id], test_y_label)
        #print('Epoch %d | Test_accuracy: %.4f' % (epoch, acc_val))

    # end = datetime.datetime.now()
    # difference = end - start
    # print("the time of graphpy is:", difference)
    # print('Epoch %d | Test_accuracy: %.4f' % (epoch, acc_val))




