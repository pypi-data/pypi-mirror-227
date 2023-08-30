import itertools
import datetime
import torch
import torch.nn.functional as F
import pubmed_util
import argparse
import create_graph_dgl as cg
from dgl.data.utils import load_graphs
import gcnconv_dgl as gnn


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='pick CPU or GPU to perform the graph deep learning ')
    parser.add_argument('--gdir', type=str, required=True, help='pick graph directory')
    parser.add_argument('--device', type=str, default= 'GPU', help='pick CPU or GPU')
    parser.add_argument('--graph', type=str, default= 'text', help='pick text or binary')
    parser.add_argument('--dim', type=int, default= 16, help='intermediate feature length')
    parser.add_argument('--head', type=int, default= 1, help='GAT head value')
    parser.add_argument('--category', type=int, required=True, help='classification category. e.g. cora has 7')
    parser.add_argument('--feature', type=str, default= 'text', help='pick text, binary, or gen')

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
    else:
        graph_data_path = graph_dir + "dgl_graph/graph.dgl"
        list_graph, label_dict_none = load_graphs(graph_data_path)
        graph = list_graph[0]
    
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
    
    train_id = torch.tensor(train_id).to(device)
    test_id = torch.tensor(test_id).to(device)
    train_y_label = torch.tensor(train_y_label).to(device)
    test_y_label = torch.tensor(test_y_label).to(device)

    #print("vcount", graph.number_of_vertices())
    print("edge", graph.number_of_edges())
    
    graph=graph.to(device)
    
    head = ([args.head] * 3) + [1]
    #head = ([1] * 3) + [1]
    input_feature_dim = feature.size(1) 
    #print(input_feature_dim)
    net = gnn.GAT(graph,3,input_feature_dim,
                args.dim,
                args.category,
                head,
                F.elu,
                0,
                attn_drop = 0,
                negative_slope = 0.2,
                residual = None)
    net.to(device)

    print("with CudaGraph \n")
    # train the network
    optimizer = torch.optim.Adam(itertools.chain(net.parameters()), lr=0.01, weight_decay=5e-4, capturable=True)

    # capture-----------
    start_graph = datetime.datetime.now()
    g = torch.cuda.CUDAGraph()
    #if epoch == 0:  # Warmup and capture once at the first epoch
    # Warmup
    s = torch.cuda.Stream()
    s.wait_stream(torch.cuda.current_stream())
    with torch.cuda.stream(s):
        for _ in range(3):
            logits = net(feature)
            logp = F.log_softmax(logits, 1)
            loss = F.nll_loss(logp[train_id], train_y_label)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
    torch.cuda.current_stream().wait_stream(s)

    # capture
    optimizer.zero_grad(set_to_none=True)
    with torch.cuda.graph(g):
        static_logits = net(feature)
        static_logp = F.log_softmax(static_logits, 1)
        static_loss = F.nll_loss(static_logp[train_id], train_y_label)
        static_loss.backward()
        optimizer.step()
    
    end_graph = datetime.datetime.now()
    print(end_graph - start_graph)
    # -------------

    start = datetime.datetime.now()
    for epoch in range(200):
        # We now replay the graph instead of running the computations
        g.replay()

        #acc_val2 = pubmed_util.accuracy(logp[test_id],test_y_label)
        #print('Epoch %d | Train_Loss: %.4f accuracy %.4f' % (epoch, loss.item(), acc_val2))
    
    end = datetime.datetime.now()
    difference = end - start
    print("DGL Training time is:", difference)
    logits_test = net.forward(feature)
    logp_test = F.log_softmax(logits_test, 1)
    acc_val2 = pubmed_util.accuracy(logp_test[test_id],test_y_label)
    print('Epoch %d | Test_accuracy: %.4f' % (epoch, acc_val2))

