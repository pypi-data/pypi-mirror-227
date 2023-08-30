import torch
import torch.nn as nn
import itertools
import torch.nn.functional as F
import datetime
import pubmed_util
import torch
import torch.nn.functional as F
from torch_geometric.nn import GCNConv
import util
import argparse
from torch_geometric.data import Data

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
    #torch.save(edge_index, 'graph_tensor.pt')
    #print("save is done")
    # Construct a DGLGraph
    return edge_index


class Net(torch.nn.Module):
    def __init__(self, in_feats, hidden_feat, num_classes):
        super(Net, self).__init__()
        self.conv1 = GCNConv(in_feats, hidden_feat)
        self.conv2 = GCNConv(hidden_feat, num_classes)

    def forward(self, graph, data):
        data = self.conv1(data, graph)
        data = F.relu(data)
        data = F.dropout(data, training=self.training)
        data = self.conv2(data, graph)

        return F.log_softmax(data, dim=1)



if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='pick CPU or GPU to perform the graph deep learning ')
    parser.add_argument('--gdir', type=str, required=True, help='pick graph directory')
    parser.add_argument('--device', type=str, default= 'GPU', help='pick CPU or GPU')
    parser.add_argument('--graph', type=str, default= 'text', help='pick text or binary')
    parser.add_argument('--dim', type=int, default= 16, help='intermediate feature length')
    parser.add_argument('--category', type=int, required=True, help='classification category. e.g. cora has 7')
    parser.add_argument('--feature', type=str, default= 'text', help='pick text, binary, or feature length to generate')
    args = parser.parse_args()

    # Select Device
    use_cuda = args.device == 'GPU' and torch.cuda.is_available()
    device = torch.device('cuda' if use_cuda else 'cpu')
    if use_cuda:
        print("Using CUDA!")
    else:
        print('Not using CUDA!!!')

    graph_dir = args.gdir #"/mnt/huge_26TB/data/test2/cora/"
    if args.graph == 'text':
        graph_data_path = graph_dir + "graph_structure/graph.txt"
        line_needed_to_skip = 0
        src, dst, comment = read_graph_data(graph_data_path, line_needed_to_skip)
        graph = build_py_geo_graph(src, dst)
    else:
        graph_data_path = graph_dir + "dgl_graph/graph.dgl"
        list_graph, label_dict_none = load_graphs(graph_data_path)
        graph = list_graph[0]

    data_geo = Data(edge_index=graph) # graph here is a edge tensor, convert it to print graph info
    
    if args.feature == 'text':
        feature = pubmed_util.read_feature_info(graph_dir + "feature/feature.txt")
        feature = torch.tensor(feature).to(device)
    elif args.feature == 'binary':
        feature = torch.load(graph_dir + "feature/feature.pt")
        feature = feature.to(device)
    else:
        feature = torch.rand(data_geo.num_nodes,int(args.feature))
        feature = feature.to(device)


    print("edge count:", data_geo.num_edges)
    graph = graph.to(device)
    input_feature_dim = feature.size(1) 
    # the number of node in the graph
    #net = GCN(input_feature_dim, args.dim, args.category)
    # print("graph size", graph.size())
    net = Net(input_feature_dim, args.dim, args.category)
    #net = GCN(graph, input_feature_dim, 16, 6, 3, None, 1)
    net.to(device)
    
    train_id = pubmed_util.read_index_info(graph_dir + "index/train_index.txt")
    test_id = pubmed_util.read_index_info(graph_dir + "index/test_index.txt")
    test_y_label =  pubmed_util.read_label_info(graph_dir + "label/test_y_label.txt")
    train_y_label =  pubmed_util.read_label_info(graph_dir + "label/y_label.txt")

    train_id = torch.tensor(train_id).to(device)
    test_id = torch.tensor(test_id).to(device)
    train_y_label = torch.tensor(train_y_label).to(device)
    test_y_label = torch.tensor(test_y_label).to(device)

    # train the network
    optimizer = torch.optim.Adam(itertools.chain(net.parameters()), lr=0.01, weight_decay=5e-4)
    net.train()
    start = datetime.datetime.now()
    for epoch in range(200):
        start1 = datetime.datetime.now()
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
        end1 = datetime.datetime.now()
        difference1 = end1 - start1
        print("the time of each is:", difference1)

        print('Epoch %d | Train_Loss: %.4f' % (epoch, loss.item()))

        # check the accuracy for test data
        #logits_test = net.forward(graph,feature)
        #logp_test = F.log_softmax(logits_test, 1)

        #acc_val2 = util.accuracy(logp_test[test_id],test_y_label)
    end = datetime.datetime.now()
    difference = end - start
    print("the time of graphpy is:", difference)
    # check the accuracy for test data
    logits_test = net.forward(graph,feature)
    logp_test = F.log_softmax(logits_test, 1)
    acc_val2 = util.accuracy(logp_test[test_id],test_y_label)
    print('Epoch %d | Test_accuracy: %.4f' % (epoch, acc_val2))



