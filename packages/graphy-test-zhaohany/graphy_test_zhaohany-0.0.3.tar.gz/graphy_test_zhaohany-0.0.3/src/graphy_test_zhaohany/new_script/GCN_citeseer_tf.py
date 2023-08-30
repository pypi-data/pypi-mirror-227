import tensorflow as tf
import itertools
import datetime
import pygraph as gone
import pubmed_util
import gcnconv_tf as gcnconv
import create_graph as cg

def evaluate(model, features, labels, mask):
    logits = model(features)
    logits = tf.gather(logits,test_id)
    indices = tf.math.argmax(logits, axis=1)
    acc = tf.reduce_mean(tf.cast(indices == labels, dtype=tf.float32))
    return acc.numpy().item()

if __name__ == "__main__":
    ingestion_flag = gone.enumGraph.eUnidir | gone.enumGraph.eDoubleEdge | gone.enumGraph.eCreateEID
    ifile = "/home/datalab/data/test2/citeseer/graph_structure"
    num_vcount = 3327
    G = cg.create_csr_graph(ifile, num_vcount, ingestion_flag)
    weight_decay=5e-4
    input_feature_dim = 3703
    net = gcnconv.GCN(G, input_feature_dim, 16, 6)
    #net = gcnconv.GCN(G, input_feature_dim, 16, 7, 3, 1)
    feature = pubmed_util.read_feature_info("/home/datalab/data/test2/citeseer/feature/feature.txt")
    train_id = pubmed_util.read_index_info("/home/datalab/data/test2/citeseer/index/train_index.txt")
    test_id = pubmed_util.read_index_info("/home/datalab/data/test2/citeseer/index/test_index.txt")
    test_y_label =  pubmed_util.read_label_info("/home/datalab/data/test2/citeseer/label/test_y_label.txt")
    train_y_label =  pubmed_util.read_label_info("/home/datalab/data/test2/citeseer/label/y_label.txt")
    
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
