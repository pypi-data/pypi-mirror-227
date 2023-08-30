import torch
import torch.nn as nn
import itertools
import torch.nn.functional as F
import datetime

import pygraph as gone
import util
import gcnconv 
import create_graph as cg


if __name__ == "__main__":
    ingestion_flag = gone.enumGraph.eUdir | gone.enumGraph.eDoubleEdge | gone.enumGraph.eSNB
    ifile = "/home/datalab/data/test3/cora"
    num_vcount = 2708

    G = cg.create_snb_graph(ifile, num_vcount, ingestion_flag)


    labels, node_id, input_X = util.read_data()
    train_idx, val_idx, test_idx = util.limit_data(labels)
    input_train, input_test, output_train, output_test = util.get_train_test_data(train_idx, test_idx, input_X, labels)

    label_set = set(labels)
    class_label_list = []
    for each in label_set:
        class_label_list.append(each)
    labeled_nodes_train = torch.tensor(train_idx)  # only the instructor and the president nodes are labeled
    # labels_train = torch.tensor(output_train_label_encoded )  # their labels are different
    labeled_nodes_test = torch.tensor(test_idx)  # only the instructor and the president nodes are labeled
    # labels_test = torch.tensor(output_test_label_encoded)  # their labels are different
    
    # build and train the network
    input_feature_dim = 1433
    net = gcnconv.GCN(G, input_feature_dim, 16, 7)
    optimizer = torch.optim.Adam(itertools.chain(net.parameters()), lr=0.01, weight_decay=5e-4)
    #print(input_X)
    print("-------------------")
    start = datetime.datetime.now()
    for epoch in range(200):
        logits = net(input_X)
        logp = F.log_softmax(logits, 1)
        loss = F.nll_loss(logp[labeled_nodes_train], labels[labeled_nodes_train])
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        print('Epoch %d | Train_Loss: %.4f' % (epoch, loss.item()))

        # check the accuracy for test data
        logits_test = net.forward(input_X)
        logp_test = F.log_softmax(logits_test, 1)

        acc_val = util.accuracy(logp_test[labeled_nodes_test], labels[labeled_nodes_test])
        print('Epoch %d | Test_accuracy: %.4f' % (epoch, acc_val))
    end = datetime.datetime.now()
    difference = end - start
    print ('time is:', difference)
    print('Epoch %d | Test_accuracy: %.4f' % (epoch, acc_val))




