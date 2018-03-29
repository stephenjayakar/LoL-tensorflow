""" 
Representing each team as a 140 bit value, where each bit 
indicates if that champion is present on the team
There are two teams, so there are 280 features total input
"""
import numpy as np
import tensorflow as tf
import matplotlib.pyplot as plt
import json
import data_process

tf.logging.set_verbosity(tf.logging.INFO)

data = data_process.Data()

learning_rate = 0.001
# epochs = 40
num_steps = 3000
batch_size = 50
display_step = 50

n_hidden_1 = 128
n_hidden_2 = 128
# n_hidden_3 = 64
num_input = 280
num_classes = 2 # output

# change to int
X = tf.placeholder("float", [None, num_input])
Y = tf.placeholder("float", [None, num_classes])

def neural_net(x):
    layer_1 = tf.layers.dense(x, n_hidden_1)
    layer_2 = tf.layers.dense(layer_1, n_hidden_2)
    out_layer = tf.layers.dense(layer_2, num_classes)
    return out_layer

logits = neural_net(X)

loss_op = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=logits, labels=Y))
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate)
train_op = optimizer.minimize(loss_op)

correct_pred = tf.equal(tf.argmax(logits, 1), tf.argmax(Y, 1))
accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

init = tf.global_variables_initializer()

with tf.Session() as sess:
    sess.run(init)
    pred_x, pred_y = data.test()
    
    
    for step in range(1, num_steps + 1):
        batch_x, batch_y = data.next_batch(batch_size)
        sess.run(train_op, feed_dict={X: batch_x, Y: batch_y})
        if step % display_step == 0 or step == 1:
            loss, acc = sess.run([loss_op, accuracy], feed_dict={X: batch_x, Y: batch_y})
            print("testing accuracy:", sess.run(accuracy, feed_dict={X: pred_x,
                                                             Y: pred_y})
            )
            
            print("Step " + str(step) + ", Minibatch Loss= " + \
                  "{:.4f}".format(loss) + ", Training Accuracy= " + \
                  "{:.3f}".format(acc))

    print("optimization finished")
    print("testing accuracy:", sess.run(accuracy, feed_dict={X: pred_x,
                                                             Y: pred_y})
    )
