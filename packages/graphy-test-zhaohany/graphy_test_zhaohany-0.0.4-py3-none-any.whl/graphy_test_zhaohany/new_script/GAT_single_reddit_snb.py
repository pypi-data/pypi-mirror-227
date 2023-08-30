import torch
import torch.nn as nn
import itertools
import torch.nn.functional as F
import datetime

import pygraph as gone
import gatconv 
import pubmed_util
import create_graph as cg



def memoryview_to_np(memview, nebr_dt):
    arr = np.array(memview, copy=False)
    #a = arr.view(nebr_dt).reshape(nebr_reader.get_degree())
    a = arr.view(nebr_dt)
    return a


if __name__ == "__main__":
    ingestion_flag = gone.enumGraph.eUdir | gone.enumGraph.eDoubleEdge | gone.enumGraph.eSNB
    ifile = "/home/datalab/data/test2/reddit/graph_structure"
    num_vcount = 232965

    num_sources = 1
    num_thread = 4
    # manager = gone.pgraph_manager_tW(ifile, "", ingestion_flag, num_node)
    # snap_t = manager.create_static_view(gone.enumView.eStale)

    G = cg.create_snb_graph(ifile, num_vcount, ingestion_flag)
    print("finish creating graph")
    input_feature_dim = 602
    num_layers = 3
    net = gatconv.GAT(G, num_layers, input_feature_dim, 16, 41, 
            activation = F.elu, feat_drop = 0., attn_drop = 0., negative_slope =0.2, residual = None)


    feature = pubmed_util.read_feature_info("/home/datalab/data/test2/reddit/feature/reddit_feature.txt")
    train_id = pubmed_util.read_index_info("/home/datalab/data/test2/reddit/index/reddit_train_index.txt")
    test_id = pubmed_util.read_index_info("/home/datalab/data/test2/reddit/index/reddit_test_index.txt")
    test_y_label =  pubmed_util.read_label_info("/home/datalab/data/test2/reddit/label/reddit_test_y_label.txt")
    train_y_label =  pubmed_util.read_label_info("/home/datalab/data/test2/reddit/label/reddit_y_label.txt")
    


    feature = torch.tensor(feature)
    train_id = torch.tensor(train_id)
    test_id = torch.tensor(test_id)
    train_y_label = torch.tensor(train_y_label)
    test_y_label = torch.tensor(test_y_label)


    # label_set = set(labels)
    # class_label_list = []
    # for each in label_set:
    #     class_label_list.append(each)
    # labeled_nodes_train = torch.tensor(train_idx)  # only the instructor and the president nodes are labeled
    # # labels_train = torch.tensor(output_train_label_encoded )  # their labels are different
    # labeled_nodes_test = torch.tensor(test_idx)  # only the instructor and the president nodes are labeled
    # # labels_test = torch.tensor(output_test_label_encoded)  # their labels are different
    # train the network
    optimizer = torch.optim.Adam(itertools.chain(net.parameters()), lr=0.01, weight_decay=5e-4)
    start = datetime.datetime.now()
    for epoch in range(1):
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
        #logits_test = net.forward(feature)
        #logp_test = F.log_softmax(logits_test, 1)

        #acc_val = pubmed_util.accuracy(logp_test[test_id], test_y_label)
        #print('Epoch %d | Test_accuracy: %.4f' % (epoch, acc_val))

    end = datetime.datetime.now()
    difference = end - start
    print("the time of graphpy is:", difference)
    logits_test = net.forward(feature)
    logp_test = F.log_softmax(logits_test, 1)
    acc_val = pubmed_util.accuracy(logp_test[test_id], test_y_label)
    print('Epoch %d | Test_accuracy: %.4f' % (epoch, acc_val))
