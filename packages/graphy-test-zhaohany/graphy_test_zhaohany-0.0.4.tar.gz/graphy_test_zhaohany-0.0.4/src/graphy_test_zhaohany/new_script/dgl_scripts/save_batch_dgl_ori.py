
import torch.nn.functional as F
import torchmetrics.functional as MF
import dgl.nn as dglnn
from dgl.dataloading import DataLoader, NeighborSampler, MultiLayerFullNeighborSampler
import tqdm
import argparse
import os
from random import shuffle
import numpy as np
import torch
import itertools
import scipy.sparse as sp
import dgl
from datetime import datetime, timedelta
import torch.nn as nn
import dgl.function as fn
import create_graph_dgl as cg
from dgl.data.utils import load_graphs
from dgl.nn.pytorch import GraphConv
import pubmed_util
from dgl.data import DGLDataset


# defining GraphSAGE Model

class SAGE(nn.Module):
    def __init__(self, in_size, hid_size, out_size):
        super().__init__()
        self.layers = nn.ModuleList()
        # three-layer GraphSAGE-mean
        self.layers.append(dglnn.SAGEConv(in_size, hid_size, 'mean'))
        self.layers.append(dglnn.SAGEConv(hid_size, hid_size, 'mean'))
        self.layers.append(dglnn.SAGEConv(hid_size, out_size, 'mean'))
        self.dropout = nn.Dropout(0.5)
        self.hid_size = hid_size
        self.out_size = out_size

    def forward(self, blocks, x):
        h = x
        for l, (layer, block) in enumerate(zip(self.layers, blocks)):
            #print(h.size())
            h = layer(block, h)
            if l != len(self.layers) - 1:
                h = F.relu(h)
                h = self.dropout(h)
        return h

# load and preprocess dataset

def read_graph_data(file_path, line_needed_to_skip):
    crs = open(file_path, "r")
    #print ("Output of Read function is ")
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
    return dgl.graph((u, v))



def evaluate(model, graph, dataloader):
    model.eval()
    ys = []
    y_hats = []
    for it, (input_nodes, output_nodes, blocks) in enumerate(dataloader):
        #print("it for eva", it)
        with torch.no_grad():
            x = blocks[0].srcdata['feat']
            ys.append(blocks[-1].dstdata['label'])
            y_hats.append(model(blocks, x))
            accuracy = MF.accuracy(task="multiclass", num_classes= args.category, preds = torch.cat(y_hats), target = torch.cat(ys))
    return accuracy


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='pick CPU or GPU to perform the graph deep learning ')
    parser.add_argument('--gdir', type=str, required=True, help='pick graph directory')
    parser.add_argument('--device', type=str, default= 'GPU', help='pick CPU or GPU')
    parser.add_argument('--graph', type=str, default= 'text', help='pick text or binary')
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
    if args.graph == 'text':
        graph_data_path = graph_dir + "graph_structure/graph.txt"
        line_needed_to_skip = 4
        src, dst, comment = cg.read_graph_data(graph_data_path, line_needed_to_skip)
        graph = cg.build_dgl_graph(src, dst)
        graph=graph.to(device)

    else:
        graph_data_path = graph_dir + "dgl_graph/graph.dgl"
        list_graph, label_dict_none = load_graphs(graph_data_path)
        graph = list_graph[0]
        graph=graph.to(device)
    #print(type(graph))
    
    if args.feature == 'text':
        feature = pubmed_util.read_feature_info(graph_dir + "feature/feature.txt")
        feature = torch.tensor(feature).to(device)
    elif args.feature == 'binary':
        feature = torch.load(graph_dir + "feature/feature.pt")
        feature = feature.to(device)
    else :
        feature = torch.rand(graph.number_of_nodes(), int(args.feature))
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

    graph.ndata['feat'] = feature
    graph.ndata['label'] = labels


    num_classes = args.category 
    input_feature_dim = feature.size(1)
    in_size = graph.ndata['feat'].shape[1]
    out_size = num_classes
    print(args.dim)
    model = SAGE(input_feature_dim, args.dim, num_classes).to(device)
    model.to(device)

    sampler = NeighborSampler([30, 20, 10],  # fanout for [layer-0, layer-1, layer-2],
                              prefetch_node_feats=['feat'],
                              prefetch_labels=['label'])
    #use_uva = (args.mode == 'mixed')
    print("train length", len(train_id))
    train_dataloader = DataLoader(graph, train_id, sampler, device=device,
                                   batch_size=256, shuffle=True,
                                  drop_last=False, num_workers=0)
    print("val length", len(test_id))
    print("saving batch below \n")
    val_dataloader = DataLoader(graph, test_id, sampler, device=device,
                                batch_size=256, shuffle=True,
                                drop_last=False, num_workers=0)

    # Precompute the minibatches and neighbor sampling before the training loop
    precomputed_batches = []
    for input_nodes, output_nodes, blocks in train_dataloader:
        precomputed_batches.append((input_nodes, output_nodes, blocks))
   

    # train the network
    opt = torch.optim.Adam(model.parameters(), lr=1e-3, weight_decay=5e-4)
    start1 = datetime.now()
    overhead = 0
    for epoch in range(100):
        model.train()
        total_loss = 0
        for it, (input_nodes, output_nodes, blocks) in enumerate(precomputed_batches):
            #print("batch no ", it)
            #print(type(blocks))
            start = datetime.now()
            x = blocks[0].srcdata['feat']
            y = blocks[-1].dstdata['label']
            y_hat = model(blocks, x)
            loss = F.cross_entropy(y_hat, y)
            opt.zero_grad()
            loss.backward()
            opt.step()
            end = datetime.now()
            difference = end - start
            #print("the time of graphpy is:", difference)
            total_loss += loss.item()
            temp = difference.total_seconds()
            overhead = overhead+temp
            #print("inner loop overhead ", overhead)
        acc = evaluate(model, graph, val_dataloader)
        print("Epoch {:05d} | Loss {:.4f} | Accuracy {:.4f} ".format(epoch, total_loss / (it+1), acc.item()))
    end1 = datetime.now()
    training_time = end1 - start1
    training_time = training_time.total_seconds()
    print("the Total time of SAGE is:", training_time, "Overhead Time:", overhead)
    '''acc = evaluate(model, graph, val_dataloader)
    print("Epoch {:05d} | Loss {:.4f} | Accuracy {:.4f} ".format(epoch, total_loss / (it+1), acc.item()))'''

    #test the model
   # print('Testing...')
   # print("test len", len(test_id))
    #acc = layerwise_infer(device, g, dataset.test_idx, model, batch_size=4096)
    #print("Test Accuracy {:.4f}".format(acc.item()))

