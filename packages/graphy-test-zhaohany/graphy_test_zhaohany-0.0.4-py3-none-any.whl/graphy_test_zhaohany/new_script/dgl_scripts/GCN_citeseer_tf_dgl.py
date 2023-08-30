import datetime
import pubmed_util
import tensorflow as tf
import dgl
import numpy as np
from tensorflow.keras import layers
from dgl.nn.tensorflow import GraphConv
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


def evaluate(model, features, labels, mask):
    logits = model(features)
    logits = tf.gather(logits,test_id)
    indices = tf.math.argmax(logits, axis=1)
    acc = tf.reduce_mean(tf.cast(indices == labels, dtype=tf.float32))
    return acc.numpy().item()


class GCN(layers.Layer):
    def __init__(self,
                 g,
                 in_feats,
                 n_hidden,
                 n_classes):
        super(GCN, self).__init__()
        self.graph = g
        self.conv1 = GraphConv(in_feats, n_hidden, allow_zero_in_degree = True)
        self.conv2 = GraphConv(n_hidden, n_classes, allow_zero_in_degree = True)

    def call(self, inputs):
        h = self.conv1(self.graph, inputs)
        h = tf.nn.relu(h)
        h = self.conv2(self.graph, h)
        return h

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

    graph_data_path = "/home/ygong07/data/test2/citeseer/graph_structure/citeseer_graph_undirect.txt"
    num_vcount = 3327
    weight_decay=5e-4
    input_feature_dim = 3703
    line_needed_to_skip = 4
    src, dst, comment = read_graph_data(graph_data_path, line_needed_to_skip)
    graph = build_dgl_graph(src, dst)
    net = GCN(graph, input_feature_dim, 16, 6)
    #net = gcnconv.GCN(G, input_feature_dim, 16, 7, 3, 1)
    feature = pubmed_util.read_feature_info("/home/ygong07/data/test2/citeseer/feature/feature.txt")
    train_id = pubmed_util.read_index_info("/home/ygong07/data/test2/citeseer/index/train_index.txt")
    test_id = pubmed_util.read_index_info("/home/ygong07/data/test2/citeseer/index/test_index.txt")
    test_y_label =  pubmed_util.read_label_info("/home/ygong07/data/test2/citeseer/label/test_y_label.txt")
    train_y_label =  pubmed_util.read_label_info("/home/ygong07/data/test2/citeseer/label/y_label.txt")
    
    feature = tf.convert_to_tensor(feature)
    train_id = tf.convert_to_tensor(train_id)
    test_id = tf.convert_to_tensor(test_id)
    train_y_label = tf.convert_to_tensor(train_y_label)
    #print("111", train_y_label)
    test_y_label = tf.convert_to_tensor(test_y_label, dtype= tf.int64)
    # train the network
    loss_fcn = tf.keras.losses.SparseCategoricalCrossentropy(from_logits=True)
    # use optimizer
    optimizer = tf.keras.optimizers.Adam(learning_rate=0.01, epsilon=1e-8)
    #optimizer = torch.optim.Adam(itertools.chain(net.parameters()), lr=0.01, weight_decay=5e-4)
    #print(input_X)
    #print("-------------------")
    start = datetime.datetime.now()
    for epoch in range(200):
        with tf.GradientTape() as tape:
            logits = net(feature)        
            #logp = tf.nn.log_softmax(logits, 1)
            #print("wuhu", tf.gather(logits,train_id))
            loss_value = loss_fcn(train_y_label, tf.gather(logits,train_id))
            #print("9999")
            for weight in net.trainable_weights:
                loss_value = loss_value + weight_decay*tf.nn.l2_loss(weight)
            grads = tape.gradient(loss_value, net.trainable_weights)
            optimizer.apply_gradients(zip(grads, net.trainable_weights))
        #print("prediction",logp[train_id])
    
        #print('loss_size', logp[train_id].size(), train_y_label.size())
        #loss = F.nll_loss(logp[train_id], train_y_label)

        #print('Epoch %d | Train_Loss: %.4f' % (epoch, loss.item()))
        # optimizer.zero_grad()
        # loss.backward()
        # optimizer.step()

        #print('Epoch %d | Train_Loss: %.4f' % (epoch, loss.item()))

        # check the accuracy for test data
        #logits_test = net.forward(feature)
        #logp_test = F.log_softmax(logits_test, 1)
        #acc_val = pubmed_util.accuracy(logp_test[test_id], test_y_label)
        #print('Epoch %d | Test_accuracy: %.4f' % (epoch, acc_val))

    end = datetime.datetime.now()
    difference = end - start
    print("the time of graphpy is:", difference)
    acc = evaluate(net, feature, test_y_label, test_id)
    print("Test Accuracy {:.4f}".format(acc))
    # logits_test = net(feature)
    # logp_test = tf.nn.log_softmax(logits_test, 1)
    # acc_val = pubmed_util.accuracy(tf.gather(logp_test,test_id), test_y_label)
    # print('Epoch %d | Test_accuracy: %.4f' % (epoch, acc_val))
