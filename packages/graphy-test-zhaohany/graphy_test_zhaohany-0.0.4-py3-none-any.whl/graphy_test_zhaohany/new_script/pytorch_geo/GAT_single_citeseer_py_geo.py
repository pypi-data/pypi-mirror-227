import torch
import torch.nn as nn
import itertools
import torch.nn.functional as F
import datetime
import pubmed_util
import torch
import torch.nn.functional as F
from torch_geometric.nn import GATConv
import util


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


def build_py_geo_graph(src, dst):
    # while the other for destination endpoints.
    edge_index = torch.tensor([src, dst], dtype=torch.long)
    # Construct a DGLGraph
    return edge_index


class GAT(torch.nn.Module):
    def __init__(self, in_channels, out_channels, num_heads):
        super(GAT, self).__init__()

        self.conv1 = GATConv(in_channels, 16, heads = num_heads, dropout=0.0)
        # On the Pubmed dataset, use heads=8 in conv2.
        self.conv2 = GATConv(16 * num_heads, 16, heads= num_heads, dropout=0.0)
        self.conv3 = GATConv(16 * num_heads, 16, heads= num_heads, dropout=0.0)
        self.conv4 = GATConv(16 * num_heads, out_channels, heads=1, concat=False, dropout=0.0)

    def forward(self, x, edge_index):
        #x = F.dropout(x, p=0.6, training=self.training)
        x = self.conv1(x, edge_index)
        #x = F.elu(x)
        #x = F.dropout(x, p=0.6, training=self.training)
        x = self.conv2(x, edge_index)
        #x = F.elu(x)
        x = self.conv3(x, edge_index)
        #x = F.elu(x)
        x = self.conv4(x, edge_index)
        return F.log_softmax(x, dim=-1)



if __name__ == "__main__":


    graph_data_path = "/home/ygong07/data/test2/citeseer/graph_structure/citeseer_graph_undirect.txt"
    # the number of node in the graph
    num_node = 3327
    input_feature_dim = 3703
    cuda = torch.device('cuda')
    # the features have 5 dimensions
    # net = GCN(input_feature_dim, 16, 7)
    line_needed_to_skip = 4
    g_start = datetime.datetime.now()
    src, dst, comment = read_graph_data(graph_data_path, line_needed_to_skip)
    graph = build_py_geo_graph(src, dst)
    # print("graph size", graph.size())
    g_end = datetime.datetime.now()
    diff = g_end - g_start
    print ('graph creation time is:', diff)
    graph=graph.to(cuda)
    num_heads = 1
    num_output_class = 6
    net = GAT(input_feature_dim, num_output_class, num_heads)
    #net = GCN(graph, input_feature_dim, 16, 6, 3, None, 1)
    net.to(cuda)
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
    #cuda
    feature=feature.to(cuda)
    train_id=train_id.to(cuda)
    test_id=test_id.to(cuda)
    train_y_label=train_y_label.to(cuda)
    test_y_label=test_y_label.to(cuda)

    # train the network
    optimizer = torch.optim.Adam(itertools.chain(net.parameters()), lr=0.01, weight_decay=5e-4)
    net.train()
    start = datetime.datetime.now()
    for epoch in range(200):
        logits = net(feature, graph)
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
        #logits_test = net.forward(graph,feature)
        #logp_test = F.log_softmax(logits_test, 1)

        #acc_val2 = util.accuracy(logp_test[test_id],test_y_label)
    end = datetime.datetime.now()
    difference = end - start
    print("the time of graphpy is:", difference)
    # check the accuracy for test data
    logits_test = net.forward(feature, graph)
    logp_test = F.log_softmax(logits_test, 1)
    acc_val2 = util.accuracy(logp_test[test_id],test_y_label)
    print('Epoch %d | Test_accuracy: %.4f' % (epoch, acc_val2))



