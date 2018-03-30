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
import champions

tf.reset_default_graph()
tf.logging.set_verbosity(tf.logging.INFO)

total_chunks = 64
data = data_process.Data(total_chunks)

learning_rate = 0.0005
epochs = 5
num_steps = 1000
batch_size = 50
display_step = 50

n_hidden_1 = 128
n_hidden_2 = 128
# n_hidden_3 = 128
num_input = 280
num_classes = 2 # output

# change to int
X = tf.placeholder("float", [None, num_input])
Y = tf.placeholder("float", [None, num_classes])

def neural_net(x):
    layer_1 = tf.layers.dense(x, n_hidden_1, activation=tf.nn.relu)
    layer_2 = tf.layers.dense(layer_1, n_hidden_2, activation=tf.nn.relu)
    # layer_3 = tf.layers.dense(layer_2, n_hidden_3)
    out_layer = tf.layers.dense(layer_2, num_classes)
    return out_layer

logits = neural_net(X)

loss_op = tf.reduce_mean(tf.nn.softmax_cross_entropy_with_logits(logits=logits, labels=Y))
optimizer = tf.train.AdamOptimizer(learning_rate=learning_rate)
train_op = optimizer.minimize(loss_op)

correct_pred = tf.equal(tf.argmax(logits, 1), tf.argmax(Y, 1))
accuracy = tf.reduce_mean(tf.cast(correct_pred, tf.float32))

init = tf.global_variables_initializer()

saver = tf.train.Saver()
 
sess = tf.Session()
sess.run(init)
saver.restore(sess, "tmp/model.ckpt")
pred_x, pred_y = data.test()

def train():
    for ep in range(1, epochs + 1):
        print("Epoch {}".format(ep))
        for step in range(1, num_steps + 1):
            batch_x, batch_y = data.next_batch(batch_size)
            if not batch_x:
                break
            sess.run(train_op, feed_dict={X: batch_x, Y: batch_y})
            if step % display_step == 0 or step == 1:
                loss, acc = sess.run([loss_op, accuracy], feed_dict={X: batch_x, Y: batch_y})
                print("testing accuracy:", sess.run(accuracy, feed_dict={X: pred_x,
                                                         Y: pred_y}))
                
                print("Step " + str(step) + ", Minibatch Loss= " + \
                      "{:.4f}".format(loss) + ", Training Accuracy= " + \
                      "{:.3f}".format(acc))
        data = data_process.Data(total_chunks)

    print("optimization finished")
    print("testing accuracy:", sess.run(accuracy, feed_dict={X: pred_x,
                                                         Y: pred_y}))
    # saving the model
    save_path = saver.save(sess, "tmp/model.ckpt")
    print("model saved!")

def predict():
    redTeam = []
    blueTeam = []
    # blue team wins
    defaultPred = [[1, 0]]
    print("type champions from blue -> red, newline on each")
    
    for i in range(5):
        redTeam.append(input())
    for i in range(5):
        blueTeam.append(input())

    a = champions.team_to_features(redTeam)
    b = champions.team_to_features(blueTeam)
    # assert(sum(a) + sum(b) == 10)
    acc = sess.run(accuracy, feed_dict={X: [a + b],
                                        Y: defaultPred})
    if acc > 0.5:
        print("Blue team victory!")
    else:
        print("Red team victory!")
    
