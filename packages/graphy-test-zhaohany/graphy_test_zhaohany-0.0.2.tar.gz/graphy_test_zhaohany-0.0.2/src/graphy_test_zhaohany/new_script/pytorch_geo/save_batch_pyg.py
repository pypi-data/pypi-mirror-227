import torch
import torch.nn as nn
import itertools
import torch.nn.functional as F
import torchmetrics.functional as MF
import torch_geometric.nn as gnn
from torch_geometric.loader import DataLoader, NeighborLoader
from torch_geometric.data import NeighborSampler
import torch_geometric.transforms as T
import torch_geometric.utils as utils
import numpy as np
import scipy.sparse as sp
import pubmed_util
import argparse
from argparse import ArgumentParser
from torch_geometric.data import Data
from datetime import datetime, timedelta
import util


class SAGE(nn.Module):
    def __init__(self, in_size, hid_size, out_size):
        super().__init__()
        self.layers = nn.ModuleList()
        self.layers.append(gnn.SAGEConv(in_size, hid_size))
        self.layers.append(gnn.SAGEConv(hid_size, hid_size))
        self.layers.append(gnn.SAGEConv(hid_size, out_size))
        self.dropout = nn.Dropout(0.5)

    def forward(self, x, edge_index):
        
        for l, layer in enumerate(self.layers):
            x = layer(x, edge_index)
            #print("###########")
            #print(x.size(), edge_index)
            if l != len(self.layers) - 1:
                x = F.relu(x)
                x = self.dropout(x)
        return x.log_softmax(dim=-1)


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


"""def evaluate(model, dataloader):
    model.eval()
    ys = []
    y_hats = []
    for batch in dataloader:
        with torch.no_grad():
            batch.to(device)
            y_hat = model(batch.x, batch.edge_index)
            y = batch.y
            ys.append(y)
            y_hats.append(y_hat)

    y_true = torch.cat(ys, dim=0)
    y_pred = torch.cat(y_hats, dim=0)

    accuracy = MF.accuracy(preds=y_pred, target=y_true, num_classes=args.category, task="multiclass")
    return accuracy"""

def evaluate(model, dataloader):
    model.eval()
    total_accuracy = 0
    total_samples = 0
    #v_count = 0
    for batch in dataloader:
        with torch.no_grad():
            batch.to(device)
            y_hat = model(batch.x, batch.edge_index)
            y = batch.y
            accuracy = MF.accuracy(preds=y_hat, target=y, num_classes=args.category, task="multiclass")
            total_accuracy += accuracy.item() * y.size(0)  # sum of accuracies multiplied by batch size
            total_samples += y.size(0)  # count of all samples
            #v_count += 1
            #print("valid batch no", v_count)
    average_accuracy = total_accuracy / total_samples
    return average_accuracy



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='pick CPU or GPU to perform the graph deep learning ')
    parser.add_argument('--gdir', type=str, required=True, help='pick graph directory')
    parser.add_argument('--device', type=str, default= 'GPU', help='pick CPU or GPU')
    parser.add_argument('--dim', type=int, default= 128, help='intermediate feature length')
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
    
    graph_data_path = graph_dir + "graph_structure/graph.txt"
    line_needed_to_skip = 4
    src, dst, comment = read_graph_data(graph_data_path, line_needed_to_skip)
    graph = build_py_geo_graph(src, dst)
    graph=graph.to(device)
    #print(graph)
    #print("graph size ",graph.size())
    
    
    if args.feature == 'text':
        feature = pubmed_util.read_feature_info(graph_dir + "feature/feature.txt")
        feature = torch.tensor(feature).to(device)
    elif args.feature == 'binary':
        feature = torch.load(graph_dir + "feature/feature.pt")
        feature = feature.to(device)
    else :
        num_nodes = graph.max().item() + 1
        feature = torch.rand(num_nodes, int(args.feature))
        feature = feature.to(device)


    train_id = pubmed_util.read_index_info(graph_dir + "index/train_index.txt")
    test_id = pubmed_util.read_index_info(graph_dir + "index/test_index.txt")
    test_y_label =  pubmed_util.read_label_info(graph_dir + "label/test_y_label.txt")
    train_y_label =  pubmed_util.read_label_info(graph_dir + "label/y_label.txt")
    labels =  pubmed_util.read_label_info(graph_dir + "label/label.txt")
    
    train_id = torch.tensor(train_id).to(device)
    test_id = torch.tensor(test_id).to(device)
    train_y_label = torch.tensor(train_y_label).to(device)
    test_y_label = torch.tensor(test_y_label).to(device)
    labels = torch.tensor(labels).to(device)

    #print("Train Length", train_id.size())
    #print("Valid Length", test_id.size())

    
    data_geo = Data(x=feature, edge_index=graph, y=labels) # graph here is a edge tensor, convert it to print graph info
    data_geo=data_geo.to(device)
    #print(type(data_geo))
    #print(data_geo)
    #print((data_geo.edge_index))
    #print(data_geo.x)
    

    ###### Masking for calculating the loss in training#####
    # assuming that train_id contains the indices of nodes used for training
    train_mask = torch.zeros(data_geo.num_nodes, dtype=torch.bool)
    train_mask[train_id] = True

    val_mask = torch.zeros(data_geo.num_nodes, dtype=torch.bool)
    val_mask[test_id] = True
    # Now add the train_mask to your data object
    data_geo.train_mask = train_mask
    data_geo.val_mask = val_mask
    #print((train_mask))

    
    num_classes = args.category 
    input_feature_dim = feature.size(1)
    print((input_feature_dim))
    print(args.dim)
    model = SAGE(input_feature_dim, args.dim, num_classes).to(device)
    model.to(device)

    
    # Initialize DataLoader with NeighborSampler
    train_dataloader = NeighborLoader(data_geo, input_nodes= train_mask, num_neighbors=[30, 20, 10], batch_size=256, shuffle=True)
    #print("Train mask", train_mask.size())
    val_dataloader = NeighborLoader(data_geo, input_nodes= val_mask, num_neighbors=[30, 20, 10], batch_size=256, shuffle=True)
    #print("Valid mask", val_mask.size())

    # Prepare the data before the training loop:
    train_batches = list(NeighborLoader(data_geo, input_nodes=train_mask, num_neighbors=[30, 20, 10], batch_size=256, shuffle=True))
    val_batches = list(NeighborLoader(data_geo, input_nodes=val_mask, num_neighbors=[30, 20, 10], batch_size=256, shuffle=True))

    opt = torch.optim.Adam(model.parameters(), lr=1e-3, weight_decay=5e-4)
    start1 = datetime.now()
    overhead = 0

    # Now in your training loop, you iterate through the pre-prepared data:
    for epoch in range(10):
        model.train()
        total_loss = 0
        batch_count = 0 
        for batch in train_batches:  # change here
            '''print("batch size", batch.x.size())
            print(batch)
            print(type(batch))
            print("batch edge",batch.edge_index)'''
            start = datetime.now()
            batch.to(device)
            opt.zero_grad()
            out = model(batch.x, batch.edge_index)
            # Create a mask for batch data
            batch_train_mask = batch.train_mask[batch.batch].squeeze(0)

            #print(f'Out shape: {out.size()}')

            loss = F.nll_loss(out[batch_train_mask], batch.y[batch_train_mask])
            loss.backward()
            opt.step()
            end = datetime.now()
            difference = end - start
            total_loss += loss.item()
            temp = difference.total_seconds()
            overhead = overhead+temp
            batch_count += 1 
            #print("batch no",batch_count) 
        """acc = evaluate(model, val_dataloader)
        print("Epoch {:05d} | Loss {:.4f} | Accuracy {:.4f} ".format(epoch, total_loss / batch_count, acc))"""
    end1 = datetime.now()
    training_time = end1 - start1
    training_time = training_time.total_seconds()
    print("the Total time of SAGE is:", training_time, "Overhead Time:", overhead)
    '''acc = evaluate(model, val_dataloader)
    print("Epoch {:05d} | Loss {:.4f} | Accuracy {:.4f} ".format(epoch, total_loss / batch_count, acc))'''


