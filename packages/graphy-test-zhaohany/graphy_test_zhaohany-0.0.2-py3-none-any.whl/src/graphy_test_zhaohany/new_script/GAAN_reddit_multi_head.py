import torch
import torch.nn as nn
import itertools
import torch.nn.functional as F
import datetime
import kernel
import gat_multi_head as gatconv 
import gaanconv as gaan
import pubmed_util
import create_graph as cg
import argparse

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

    
    file_dir = "/mnt/huge_26TB/data/"
    ifile = file_dir + "test2/reddit/binary_graph/"


    feature = torch.load(file_dir + "test2/reddit/feature/reddit_feature.pt")
    train_id = pubmed_util.read_index_info(file_dir + "test2/reddit/index/reddit_train_index.txt")
    test_id = pubmed_util.read_index_info(file_dir + "test2/reddit/index/reddit_test_index.txt")
    test_y_label =  pubmed_util.read_label_info(file_dir + "test2/reddit/label/reddit_test_y_label.txt")
    train_y_label =  pubmed_util.read_label_info(file_dir + "test2/reddit/label/reddit_y_label.txt")

    #num_vcount = 19717
    
    ofile = ifile + "../saved_graph/"
    G = kernel.load_graph(ofile);
    num_vcount = G.get_vcount();

    input_feature_dim = 602
    num_heads = 1
    num_layers = 3
    map_feats = 64
    heads_array = ([num_heads] * num_layers) + [1]
    net = gaan.GatedGAT(input_feature_dim, 41, map_feats, num_heads, device)
    net.to(device)

    train_id = torch.tensor(train_id)
    test_id = torch.tensor(test_id)
    train_y_label = torch.tensor(train_y_label)
    test_y_label = torch.tensor(test_y_label)

    feature = feature.to(device)
    train_id = train_id.to(device)
    test_id = test_id.to(device)
    train_y_label = train_y_label.to(device)
    test_y_label = test_y_label.to(device)


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
    #print("start_training")
    start = datetime.datetime.now()
    for epoch in range(200):
        logits = net(G, feature)
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
    print("the time of graphpy for GAT3 pubmed is:", difference)
    # check the accuracy for test data
    logits_test = net.forward(G, feature)
    logp_test = F.log_softmax(logits_test, 1)
    acc_val = pubmed_util.accuracy(logp_test[test_id], test_y_label)
    print('Epoch %d | Test_accuracy: %.4f' % (epoch, acc_val))
