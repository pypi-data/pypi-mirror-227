import torch
import torch.nn as nn
import pubmed_util
import itertools
import torch.nn.functional as F
import pygraph as gone
import kernel 
import numpy as np
import gcnconv 
import datetime
import create_graph as cg


if __name__ == "__main__":
    ingestion_flag = gone.enumGraph.eUdir | gone.enumGraph.eDoubleEdge | gone.enumGraph.eSNB
    ifile = "/home/datalab/data/test2/citeseer/graph_structure"
    num_vcount = 3327
    
    G = cg.create_snb_graph(ifile, num_vcount, ingestion_flag);

    feature = pubmed_util.read_feature_info("/home/datalab/data/test2/citeseer/feature/citeseer_feature.txt")
    train_id = pubmed_util.read_index_info("/home/datalab/data/test2/citeseer/index/citeseer_train_index.txt")
    test_id = pubmed_util.read_index_info("/home/datalab/data/test2/citeseer/index/citeseer_test_index.txt")
    test_y_label =  pubmed_util.read_label_info("/home/datalab/data/test2/citeseer/label/citeseer_test_y_label.txt")
    train_y_label =  pubmed_util.read_label_info("/home/datalab/data/test2/citeseer/label/citeseer_y_label.txt")
    
    feature = torch.tensor(feature)
    train_id = torch.tensor(train_id)
    test_id = torch.tensor(test_id)
    train_y_label = torch.tensor(train_y_label)
    test_y_label = torch.tensor(test_y_label)
    
    # train the network
    input_feature_dim = 3703
    net = gcnconv.GCN(G, input_feature_dim, 16, 6, 3, 1)
    optimizer = torch.optim.Adam(itertools.chain(net.parameters()), lr=0.01, weight_decay=5e-4)
    #print(input_X)
    #print("-------------------")
    start = datetime.datetime.now()
    for epoch in range(200):
        logits = net(feature)
        #print ('check result')
        #print(logits)
        #print(logits.size())
        logp = F.log_softmax(logits, 1)
        #print("prediction",logp[train_id])
    
        #print('loss_size', logp[train_id].size(), train_y_label.size())
        loss = F.nll_loss(logp[train_id], train_y_label)

        #print('Epoch %d | Train_Loss: %.4f' % (epoch, loss.item()))
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        #print('Epoch %d | Train_Loss: %.4f' % (epoch, loss.item()))

        # check the accuracy for test data
        logits_test = net.forward(feature)
        logp_test = F.log_softmax(logits_test, 1)

        acc_val = pubmed_util.accuracy(logp_test[test_id], test_y_label)
        #print('Epoch %d | Test_accuracy: %.4f' % (epoch, acc_val))

    end = datetime.datetime.now()
    difference = end - start
    print("the time of graphpy is:", difference)
    print('Epoch %d | Test_accuracy: %.4f' % (epoch, acc_val))


