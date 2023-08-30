import torch
import torch.nn as nn
import gat_multi_head as gatconv 
import util
import itertools
import torch.nn.functional as F
import pygraph as gone
import kernel
import numpy as np
import datetime
import create_graph as cg

def memoryview_to_np(memview, nebr_dt):
    arr = np.array(memview, copy=False)
    #a = arr.view(nebr_dt).reshape(nebr_reader.get_degree())
    a = arr.view(nebr_dt)
    return a;

if __name__ == "__main__":
    ingestion_flag = gone.enumGraph.eUdir | gone.enumGraph.eDoubleEdge| gone.enumGraph.eSNB
    ifile = "/home/datalab/data/test3/cora"
    num_vcount = 2708
    num_sources = 1
    num_thread = 4
    # manager = gone.pgraph_manager_tW(ifile, "", ingestion_flag, num_node)
    # snap_t = manager.create_static_view(gone.enumView.eStale)

    G = cg.create_snb_graph(ifile, num_vcount, ingestion_flag)

    input_feature_dim = 1433
    num_heads = 3
    num_layers = 3
    heads_array = ([num_heads] * num_layers) + [1]
    net = gatconv.GAT(G, num_layers, input_feature_dim, 16, 7, heads_array, 
            activation = F.elu, feat_drop = 0., attn_drop = 0., negative_slope =0.2, residual = None)

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
    # train the network
    optimizer = torch.optim.Adam(itertools.chain(net.parameters()), lr=0.01, weight_decay=5e-4)
    start = datetime.datetime.now()
    for epoch in range(200):
        logits = net(input_X)
        #print ('check result')
        #print(logits)
        #print(logits.size())
        logp = F.log_softmax(logits, 1)
        #print("prediction",logp[labeled_nodes_train])
        #print('loss_size', logp[labeled_nodes_train].size(), labels[labeled_nodes_train].size())
        #print(labels[labeled_nodes_train])
        loss = F.nll_loss(logp[labeled_nodes_train], labels[labeled_nodes_train])

        #print('Epoch %d | Train_Loss: %.4f' % (epoch, loss.item()))
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        #print('Epoch %d | Train_Loss: %.4f' % (epoch, loss.item()))

        # check the accuracy for test data
        logits_test = net.forward(input_X)
        logp_test = F.log_softmax(logits_test, 1)

        acc_val = util.accuracy(logp_test[labeled_nodes_test], labels[labeled_nodes_test])
        #print('Epoch %d | Test_accuracy: %.4f' % (epoch, acc_val))

    end = datetime.datetime.now()
    difference = end - start
    print("the time of graphpy is:", difference)
    print('Epoch %d | Test_accuracy: %.4f' % (epoch, acc_val))


#



