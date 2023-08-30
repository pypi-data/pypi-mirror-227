import torch
import torch.nn as nn
import util
import itertools
import torch.nn.functional as F
import pygraph as gone
import kernel 
import numpy as np
import gcnconv 
import datetime

def memoryview_to_np(memview, nebr_dt):
    arr = np.array(memview, copy=False)
    #a = arr.view(nebr_dt).reshape(nebr_reader.get_degree())
    a = arr.view(nebr_dt)
    return a;



if __name__ == "__main__":
    ingestion_flag = gone.enumGraph.eUnidir | gone.enumGraph.eDoubleEdge | gone.enumGraph.eCreateEID
    edge_dt = np.dtype([('src', np.int32), ('dst', np.int32), ('edgeid', np.int32)])
    csr_dt = np.dtype([('dst', np.int32), ('edgeid', np.int32)])
    offset_dt = np.dtype([('offset', np.int32)])

    ifile = "/home/datalab/data/test3/cora"
    num_node = 2708
    outdir = ""
    num_sources = 1
    num_thread = 8
    
    graph = gone.init(1, 1, outdir, num_sources, num_thread)  # Indicate one pgraph, and one vertex type
    tid0 = graph.init_vertex_type(num_node, True, "gtype")  # initiate the vertex type
    pgraph = graph.create_schema(ingestion_flag, tid0, "friend", edge_dt)  # initiate the pgraph
    # creating graph directly from file requires some efforts. Hope to fix that later
    manager = graph.get_pgraph_managerW(0)  # This assumes single weighted graph, edgeid is the weight
    manager.add_edges_from_dir(ifile, ingestion_flag)  # ifile has no weights, edgeid will be generated
    pgraph.wait()  # You can't call add_edges() after wait(). The need of it will be removed in future.
    manager.run_bfs(1)
    
    #snap_t = gone.create_static_view(pgraph, gone.enumView.eStale)
    
    offset_csr1, offset_csc1, nebrs_csr1, nebrs_csc1 = gone.create_csr_view(pgraph);
    offset_csr = memoryview_to_np(offset_csr1, offset_dt);
    offset_csc = memoryview_to_np(offset_csc1, offset_dt);
    nebrs_csr = memoryview_to_np(nebrs_csr1, csr_dt);
    nebrs_csc = memoryview_to_np(nebrs_csc1, csr_dt);
    snap_t = kernel.init_graph(offset_csr, nebrs_csr, offset_csc, nebrs_csc);
    
    snap_t.run_bfs(1);
    input_feature_dim = 1433
    net = gcnconv.GCN(snap_t, input_feature_dim, 16, 7, 3, 1)

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
    all_logits = []
    print(input_X)
    print("-------------------")
    start = datetime.datetime.now()
    for epoch in range(200):
        logits = net(input_X)
        all_logits.append(logits.detach())
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


