import torch
import torch.nn as nn
import gatconv
import util
import itertools
import torch.nn.functional as F
import pygraph as gone
import kernel
import numpy as np
import datetime

def memoryview_to_np(memview, nebr_dt, count):
    arr = np.array(memview, copy=False)
    #a = arr.view(nebr_dt).reshape(nebr_reader.get_degree())
    #a = arr.view(nebr_dt).reshape(count)
    a = arr.view(nebr_dt)
    print(type(a))
    print(a)
    return a;

def accuracy(prediction, label):
    correct = 0
    result = []
    for i in range(len(label)):
        #print("nani?")
        result.append(prediction[i])
        if (prediction[i] == label[i]):
            correct = correct + 1
    return correct / float(len(label)), result



def read_graph_data(file_path, line_needed_to_skip):
    crs = open(file_path, "r")
    print ("Output of Read function is ")
    #print (crs.read())
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




if __name__ == "__main__":

    ingestion_flag = gone.enumGraph.eDdir | gone.enumGraph.eDoubleEdge| gone.enumGraph.eCreateEID
    ifile = "/home/datalab/data/test2/"
    num_node = 34
    num_sources = 1
    num_thread = 8
    # manager = gone.pgraph_manager_tW(ifile, "", ingestion_flag, num_node)
    # snap_t = manager.create_static_view(gone.enumView.eStale)

    edge_dt = np.dtype([('src', np.int32), ('dst', np.int32), ('edgeid', np.int32)])
    csr_dt = np.dtype([('dst', np.int32), ('edgeid', np.int32)])
    offset_dt = np.dtype([('offset', np.int32)])

    outdir = ""
    graph = gone.init(1, 1, outdir, num_sources, num_thread)  # Indicate one pgraph, and one vertex type
    tid0 = graph.init_vertex_type(34, True, "gtype") # initiate the vertex type
    pgraph = graph.create_schema(ingestion_flag, tid0, "friend", edge_dt) # initiate the pgraph

    # creating graph directly from file requires some efforts. Hope to fix that later
    manager = graph.get_pgraph_managerW(0) # This assumes single weighted graph, edgeid is the weight
    manager.add_edges_from_dir(ifile, ingestion_flag)  # ifile has no weights, edgeid will be generated
    pgraph.wait()  # You can't call add_edges() after wait(). The need of it will be removed in future.
    manager.run_bfs(13)

    snap_t = gone.create_static_view(pgraph, gone.enumView.eStale)
    v_count = snap_t.get_vcount();
    e_count = snap_t.get_edge_count();
    print (v_count, e_count);

    offset_csr1, offset_csc1, nebrs_csr1, nebrs_csc1 = gone.create_csr_view(pgraph);
    offset_csr = memoryview_to_np(offset_csr1, offset_dt, v_count + 1);
    offset_csc = memoryview_to_np(offset_csc1, offset_dt, v_count + 1);
    nebrs_csr = memoryview_to_np(nebrs_csr1, csr_dt, e_count);
    nebrs_csc = memoryview_to_np(nebrs_csc1, csr_dt, e_count);
    snap_t = kernel.init_graph(offset_csr, nebrs_csr, offset_csc, nebrs_csc);
    v_count = snap_t.get_vcount();
    e_count = snap_t.get_edge_count();
    print (v_count, e_count);
    snap_t.run_bfs(13)


    input_feature_dim = 5
   
    embed = nn.Embedding(num_node, input_feature_dim)  # 34 nodes with embedding dim equal to 5
    inputs = torch.tensor([[ 1.0697, -0.1419,  0.0782, -1.0929,  1.1936],
        [-0.3677,  0.9840,  0.5001,  0.5691,  2.8748],
        [ 1.4907,  1.0489,  0.8279,  0.3542,  0.0923],
        [ 0.2266, -0.9223,  0.1327,  0.0550,  0.4363],
        [-1.9041, -0.9566,  0.1589, -0.4105, -0.7027],
        [-0.5105,  1.0170, -1.9042, -0.8973,  0.0485],
        [-1.3870, -2.6555,  0.6737,  0.5907, -1.4471],
        [-0.3273, -2.5961,  1.4094,  0.2120, -0.3798],
        [ 1.1695,  0.2795,  0.1744,  1.7339,  0.1272],
        [ 0.1529,  0.6807,  1.3838,  0.8028,  0.8778],
        [ 0.0781, -0.8352, -0.1175, -0.7997,  0.3524],
        [ 0.4686,  0.1325,  0.7024, -0.0676,  0.0301],
        [-0.8012,  1.6288, -1.3279,  0.5307, -0.5970],
        [ 0.0422, -0.8449,  0.8808,  0.6338, -0.4419],
        [-0.7238,  0.1553, -0.2273, -0.3242,  0.1480],
        [ 1.3768,  0.0718,  0.3425,  1.1562, -1.7056],
        [-0.0632,  0.1719, -0.6857,  0.2136,  0.2518],
        [-0.7727,  0.3532, -0.0727, -0.0459, -0.1422],
        [-0.1596, -1.4240, -0.5345,  1.0060, -0.1158],
        [ 0.4385, -0.0561,  0.8155, -0.3299, -0.6185],
        [ 0.9935, -1.7025,  1.9390, -0.3929,  0.2246],
        [ 0.6437, -0.4821, -0.6707,  1.4761,  0.9519],
        [ 0.8429,  0.4821,  1.2774, -0.4937, -0.3242],
        [ 0.1918, -0.3590, -1.5829, -0.7261, -0.2126],
        [-0.7885, -0.0722,  0.3902,  2.0317,  0.0518],
        [ 0.4079,  0.4579, -0.6410,  0.0372, -1.1750],
        [ 1.1448, -0.3493, -1.0203,  0.6427, -0.9110],
        [-0.2889,  2.0563,  0.9192,  0.0903,  0.5734],
        [ 0.6687, -0.6856,  1.3001,  0.4206,  0.4641],
        [ 0.7421,  1.2220,  0.7890,  1.0467, -0.3200],
        [-0.4786,  1.3458, -0.3373,  0.4424,  0.8443],
        [ 0.5896, -1.6171, -0.2082, -0.6664, -0.5781],
        [ 1.2394,  0.2473, -1.9055, -1.3474, -1.4021],
        [ 1.8865, -0.3820, -0.4517,  1.0323,  0.4815]], requires_grad = True)


    #embed = nn.Embedding.from_pretrained(weight1)
    weight2 = torch.tensor([[-0.0202, -0.1091,  0.0603,  0.2008, -0.6365],
        [-0.1158, -0.4139, -0.4007, -0.3206, -0.3624],
        [-0.6508,  0.2236, -0.1202, -0.5056,  0.2951],
        [ 0.1367,  0.4756, -0.1852, -0.2253,  0.2737],
        [-0.3203,  0.4027,  0.6177, -0.4073,  0.0845]], requires_grad =True)

    #graph.ndata['feat'] = embed.weight
    #inputs = embed.weight
    weight3 = torch.tensor([[-0.4980, -0.6419],
        [-0.0758, -0.3551],
        [-0.9030,  0.2837],
        [-0.4302, -0.8633],
        [-0.6338,  0.7542]], requires_grad = True)

    # print ("input")
    # print (inputs)
    # net = GCN(input_feature_dim, 5, 2)
    # print ("parameter")
    # print (net.parameters())

    #assign two labels to only two nodes
    labeled_nodes = torch.tensor([0, 33])  # only the instructor and the president nodes are labeled
    labels = torch.tensor([0, 1])  # their labels are different

    # define the test for the remaining node
    temp = []
    for i in range(33):
        temp.append(i)
    temp.remove(0)
    labeled_nodes_test = torch.tensor(temp)
    labels_test = torch.tensor([0,0,0,0,0,0,0,0,1,0,0,0,0,1,1,0,0,1,0,1,1,1,1,1,1,1,1,1,1,1,1,1])



    # num_heads = 2
    num_layers = 1 
    # heads_array = ([num_heads] * num_layers) + [1]
    net = gatconv.GAT(snap_t, num_layers, input_feature_dim, 5, 2, activation = None, feat_drop = 0., attn_drop = 0., negative_slope =0.2, residual = False)

    # labels, node_id, input_X = util.read_data()
    #print("type", type(input_X))
    # train_idx, val_idx, test_idx = util.limit_data(labels)
    # input_train, input_test, output_train, output_test = util.get_train_test_data(train_idx, test_idx, input_X, labels)

    # label_set = set(labels)
    # class_label_list = []
    # for each in label_set:
    #     class_label_list.append(each)
    # labeled_nodes_train = torch.tensor(train_idx)  # only the instructor and the president nodes are labeled
    # # labels_train = torch.tensor(output_train_label_encoded )  # their labels are different
    # labeled_nodes_test = torch.tensor(test_idx)  # only the instructor and the president nodes are labeled
    # labels_test = torch.tensor(output_test_label_encoded)  # their labels are different
    # train the network
    optimizer = torch.optim.Adam(itertools.chain(net.parameters()), lr=0.01, weight_decay=5e-4)
    start = datetime.datetime.now()
    for epoch in range(200):
        #print("epoch",epoch)
        #print("forward")
        logits = net(inputs)
        # print ('check result')
        # #print(logits)
        # print (logits.size())
        # print("details")
        # print(logits)
        logp = F.log_softmax(logits, 1)
        loss = F.nll_loss(logp[labeled_nodes], labels)
        #print("backward")
        #print('Epoch %d | Train_Loss1: %.4f' % (epoch, loss.item()))
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        print('Epoch %d | Train_Loss: %.4f' % (epoch, loss.item()))

        # check the accuracy for test data
        logits_test = net.forward(inputs)
        logp_test = F.log_softmax(logits_test, 1)

        acc_val2 = util.accuracy(logp_test[labeled_nodes_test],labels_test)
        print('Epoch %d | Test_accuracy: %.4f' % (epoch, acc_val2))




#     # train the network
#     optimizer = torch.optim.Adam(itertools.chain(net.parameters(), embed.parameters()), lr=0.01)
#     loss_record = []
#     accu_record = []
#     print ("1111")
#     print (net.parameters())
#     for epoch in range(200):
#         logits = net(graph, inputs)
#         print ("prediction")
#         print (logits)
#         # we save the logits for visualization later
#         logp = F.log_softmax(logits, 1)
#         # we only compute loss for labeled nodes
#         loss = F.nll_loss(logp[labeled_nodes], labels)
#         make_dot(loss).render("dgl", format="png")

#         optimizer.zero_grad()
#         loss.backward()
#         optimizer.step()
#         print("after one update:")
#         print(weight2)
#         print("weoght3:")
#         print(weight3)

#         print('Epoch %d | Loss: %.4f' % (epoch, loss.item()))
#         loss_record.append(loss.item())

#         logp_acc = torch.max(logp, 1).indices
#         accu, labels_test_temp = accuracy(logp_acc[labeled_nodes_test],labels_test)
#         accu_record.append(accu)
#         print('Epoch %d | accuracy: %.4f' % (epoch, accu))
#         print("evaluation report:")
#         print(metrics.classification_report(labels_test, labels_test_temp, digits=3))


        

#     # check the predction class
#     for v in range(34):
#         cls = temp.argmax()
#         print("node" + str(v) + ":" + str(cls) + "\n")


# print ("loss_record")
# print(loss_record)
# print("accu")
# print(accu_record)
