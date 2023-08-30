import os
from random import shuffle
import numpy as np
from sklearn.preprocessing import LabelEncoder
import torch
from sklearn.preprocessing import OneHotEncoder
from sklearn import preprocessing
import keras
import itertools
import torch.nn.functional as F
import torch.nn as nn
import scipy.sparse as sp
import dgl
import datetime
import torch
import torch.nn as nn
import dgl.function as fn
from dgl.nn.pytorch import edge_softmax, GATConv
import util
import pubmed_util
import argparse



def read_graph_data(file_path, line_needed_to_skip):
    crs = open(file_path, "r")
    print ("Output of Read function is ")
    # print (crs.read())
    a = [line.split() for line in crs]
    comment = a[0:line_needed_to_skip]
    array = a[line_needed_to_skip:]
    # convert the edge to src and dst
    src = []
    dst = []
    for each_edge in array:
        src.append(int(each_edge[0]))
        dst.append(int(each_edge[1]))
    return src, dst, comment


def build_dgl_graph(src, dst):
    # while the other for destination endpoints.
    src = np.array(src)
    dst = np.array(dst)
    # Edges are directional in DGL; Make them bi-directional.
    u = np.concatenate([src, dst])
    v = np.concatenate([dst, src])
    # Construct a DGLGraph
    return dgl.DGLGraph((u, v))

class GatedGAT(nn.Module):
    """Gated Graph Attention module, it is a general purpose
    graph attention module proposed in paper GaAN. The paper use
    it for traffic prediction task
    Parameter
    ==========
    in_feats : int
        number of input feature
    out_feats : int
        number of output feature
    map_feats : int
        intermediate feature size for gate computation
    num_heads : int
        number of head for multihead attention
    """

    def __init__(self, in_feats, out_feats, map_feats, num_heads):
        super(GatedGAT, self).__init__()
        self.in_feats = in_feats
        self.out_feats = out_feats
        self.map_feats = map_feats
        self.num_heads = num_heads
        self.gatlayer = GATConv(
            self.in_feats, self.out_feats, self.num_heads, allow_zero_in_degree = True
        )
        self.gate_fn = nn.Linear(
            2 * self.in_feats + self.map_feats, self.num_heads
        )
        self.gate_m = nn.Linear(self.in_feats, self.map_feats)
        self.merger_layer = nn.Linear(
            self.in_feats + self.out_feats, self.out_feats
        )

    def forward(self, g, x):
        with g.local_scope():
            g.ndata["x"] = x
            g.ndata["z"] = self.gate_m(x)
            g.update_all(fn.copy_u("x", "x"), fn.mean("x", "mean_z"))
            g.update_all(fn.copy_u("z", "z"), fn.max("z", "max_z"))
            nft = torch.cat(
                [g.ndata["x"], g.ndata["max_z"], g.ndata["mean_z"]], dim=1
            )
            gate = self.gate_fn(nft).sigmoid()
            attn_out = self.gatlayer(g, x)
            #print("out", attn_out)
            node_num = g.num_nodes()
            gated_out = (
                (gate.view(-1) * attn_out.view(-1, self.out_feats).T).T
            ).view(node_num, self.num_heads, self.out_feats)
            gated_out = gated_out.mean(1)
            merge = self.merger_layer(torch.cat([x, gated_out], dim=1))
            return merge




if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='pick CPU or GPU to perform the graph deep learning ')
    parser.add_argument('--device', type=str, default= 'CPU', help='pick CPU or GPU')
    args = parser.parse_args()
    #torch.set_printoptions(edgeitems=2000)
    # Select Device
    use_cuda = args.device == 'GPU' and torch.cuda.is_available()
    device = torch.device('cuda' if use_cuda else 'cpu')
    if use_cuda:
        print("Using CUDA!")
    else:
        print('Not using CUDA!!!')
    graph_data_path = "/home/ygong07/data/test2/citeseer/graph_structure/citeseer_graph_undirect.txt"
    # the number of node in the graph
    num_node = 3327
    input_feature_dim =  3703
    # the features have 5 dimensions
    # net = GCN(input_feature_dim, 16, 7)

    #head = ([3] * 3) + [1]
    head = 1
    #head = ([1] * 3) + [1]
    line_needed_to_skip = 4
    map_feat = 64
    src, dst, comment = read_graph_data(graph_data_path, line_needed_to_skip)
    graph = build_dgl_graph(src, dst)
    graph = graph.to(device)
    net = GatedGAT(input_feature_dim, 6, map_feat, head)
    net.to(device)
    feature = pubmed_util.read_feature_info("/home/ygong07/data/test2/citeseer/feature/citeseer_feature.txt")
    train_id = pubmed_util.read_index_info("/home/ygong07/data/test2/citeseer/index/citeseer_train_index.txt")
    test_id = pubmed_util.read_index_info("/home/ygong07/data/test2/citeseer/index/citeseer_test_index.txt")
    test_y_label =  pubmed_util.read_label_info("/home/ygong07/data/test2/citeseer/label/citeseer_test_y_label.txt")
    train_y_label =  pubmed_util.read_label_info("/home/ygong07/data/test2/citeseer/label/citeseer_y_label.txt")


    feature = torch.tensor(feature)
    train_id = torch.tensor(train_id)
    test_id = torch.tensor(test_id)
    train_y_label = torch.tensor(train_y_label)
    test_y_label = torch.tensor(test_y_label)
    # define the test for the remaining node
    feature=feature.to(device)
    train_id=train_id.to(device)
    test_id=test_id.to(device)
    train_y_label=train_y_label.to(device)
    test_y_label=test_y_label.to(device)
    

    # train the network
    optimizer = torch.optim.Adam(itertools.chain(net.parameters()), lr=0.01, weight_decay=5e-4)
    start = datetime.datetime.now()
    for epoch in range(200):
        logits = net(graph, feature)
        # print ('check result')
        # #print(logits)
        # print (logits.size())
        # print("details")
        # print(logits)
        logp = F.log_softmax(logits, 1)
        #print("ha?", train_y_label)
        loss = F.nll_loss(logp[train_id], train_y_label)
        #print('Epoch %d | Train_Loss1: %.4f' % (epoch, loss.item()))
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        #print('Epoch %d | Train_Loss: %.4f' % (epoch, loss.item()))

        # check the accuracy for test data
        #logits_test = net.forward(feature)
        #logp_test = F.log_softmax(logits_test, 1)

        #acc_val2 = util.accuracy(logp_test[test_id],test_y_label)
        #print('Epoch %d | Test_accuracy: %.4f' % (epoch, acc_val2))
    end = datetime.datetime.now()
    difference = end - start
    print("the time of graphpy GAT citeseer is:", difference)
    logits_test = net.forward(graph, feature)
    logp_test = F.log_softmax(logits_test, 1)
    acc_val2 = util.accuracy(logp_test[test_id],test_y_label)
    print('Epoch %d | Test_accuracy: %.4f' % (epoch, acc_val2 ))



