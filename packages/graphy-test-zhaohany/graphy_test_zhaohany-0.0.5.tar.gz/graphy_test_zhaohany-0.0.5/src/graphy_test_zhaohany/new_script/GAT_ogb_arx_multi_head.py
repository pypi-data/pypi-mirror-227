import torch
import torch.nn as nn
import itertools
import torch.nn.functional as F
import datetime

import pygraph as gone
import gat_multi_head as gatconv 
import pubmed_util
import create_graph as cg
import argparse
import kernel

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='pick CPU or GPU to perform the graph deep learning ')
    parser.add_argument('--device', type=str, default= 'CPU', help='pick CPU or GPU')
    args = parser.parse_args()

    # Select Device
    use_cuda = args.device == 'GPU' and torch.cuda.is_available()
    device = torch.device('cuda' if use_cuda else 'cpu')
    if use_cuda:
        print("Using CUDA!")
    else:
        print('Not using CUDA!!!')

    
    file_dir = "/home/ygong07/data/test2/ogb-arx/"
    ifile = file_dir + "graph_structure/"
    feature = pubmed_util.read_feature_info(file_dir + "feature/feature.txt")
    train_id = pubmed_util.read_index_info(file_dir + "index/train_index.txt")
    test_id = pubmed_util.read_index_info(file_dir + "index/test_index.txt")
    test_y_label =  pubmed_util.read_label_info(file_dir + "label/test_y_label.txt")
    train_y_label =  pubmed_util.read_label_info(file_dir + "label/train_y_label.txt")
    

    #num_vcount = 232965
    #ingestion_flag = gone.enumGraph.eDdir | gone.enumGraph.eDoubleEdge | gone.enumGraph.eCreateEID
    #G = cg.create_csr_graph(ifile, num_vcount, ingestion_flag)

    ofile = ifile + "../saved_graph/"
    G = kernel.load_graph(ofile)
    num_vcount = G.get_vcount()
    print("finish creating the graph")
    input_feature_dim = 128
    num_heads = 1
    num_layers = 3
    heads_array = ([num_heads] * num_layers) + [1]
    net = gatconv.GAT(G, num_layers, input_feature_dim, 16, 40, heads_array, device, activation = F.elu, feat_drop = 0., attn_drop = 0., negative_slope =0.2, residual = None)
    
    feature = torch.tensor(feature)
    train_id = torch.tensor(train_id)
    test_id = torch.tensor(test_id)
    train_y_label = torch.tensor(train_y_label)
    test_y_label = torch.tensor(test_y_label)

    feature = feature.to(device)
    train_id = train_id.to(device)
    test_id = test_id.to(device)
    train_y_label = train_y_label.to(device)
    test_y_label = test_y_label.to(device)

    
    # train the network
    optimizer = torch.optim.Adam(itertools.chain(net.parameters()), lr=0.01, weight_decay=5e-4)
    all_logits = []
    start = datetime.datetime.now()
    for epoch in range(200):
        logits = net(feature)
        #print(logits)
        #print(logits.size())
        logp = F.log_softmax(logits, 1)
        #print("prediction",logp[train_id])
        #print('loss_size', logp[train_id].size(), train_y_label.size())
        loss = F.nll_loss(logp[train_id], train_y_label)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        print('Epoch %d | Train_Loss: %.4f' % (epoch, loss.item()))

        # check the accuracy for test data
        #logits_test = net.forward(feature)
        #logp_test = F.log_softmax(logits_test, 1)

        #acc_val = pubmed_util.accuracy(logp[test_id], test_y_label)
        #print('Epoch %d | Test_accuracy: %.4f' % (epoch, acc_val))

    end = datetime.datetime.now()
    difference = end - start
    print("the time of graphpy is:", difference)
    logits_test = net.forward(feature)
    logp_test = F.log_softmax(logits_test, 1)
    acc_val = pubmed_util.accuracy(logp_test[test_id], test_y_label)
    print('Epoch %d | Test_accuracy: %.4f' % (epoch, acc_val))
