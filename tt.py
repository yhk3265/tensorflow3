
# coding: utf-8

# In[191]:


from tensorflow.examples.tutorials.mnist import input_data
mnist = input_data.read_data_sets('MNIST_data', one_hot=True)


# In[192]:


import tensorflow as tf
sess = tf.InteractiveSession()


# In[193]:


x = tf.placeholder(tf.float32, shape=[None, 784])
y_ = tf.placeholder(tf.float32, shape=[None, 10])


# In[194]:


W = tf.Variable(tf.zeros([784,10]))
b = tf.Variable(tf.zeros([10]))


# In[195]:


sess.run(tf.global_variables_initializer())
y = tf.nn.softmax(tf.matmul(x,W) + b)


# In[196]:



cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y), reduction_indices=[1]))


# In[197]:


train_step = tf.train.GradientDescentOptimizer(0.5).minimize(cross_entropy)


# In[198]:


for i in range(2000):
  batch = mnist.train.next_batch(50)
  train_step.run(feed_dict={x: batch[0], y_: batch[1]})


# In[199]:


correct_prediction = tf.equal(tf.argmax(y,1), tf.argmax(y_,1))


# In[200]:


accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))


# In[205]:


print(accuracy.eval(feed_dict={x: mnist.test.images, y_: mnist.test.labels}))


# In[206]:



def weight_variable(shape):
  initial = tf.truncated_normal(shape, stddev=0.1)
  return tf.Variable(initial)

def bias_variable(shape):
  initial = tf.constant(0.1, shape=shape)
  return tf.Variable(initial)


# In[207]:


def conv2d(x, W):
  return tf.nn.conv2d(x, W, strides=[1, 1, 1, 1], padding='SAME')

def max_pool_2x2(x):
  return tf.nn.max_pool(x, ksize=[1, 2, 2, 1],
                        strides=[1, 2, 2, 1], padding='SAME')

#def max_pool_1x1(x):
  #return tf.nn.max_pool(x, ksize=[1, 1, 1, 1],
                        #strides=[1, 1, 1, 1], padding='SAME')


# In[208]:


#W_conv1 = weight_variable([5, 5, 1, 32])
W_conv1 = tf.get_variable("W_conv1", shape=[5, 5, 1, 32],
           initializer=tf.contrib.layers.xavier_initializer())
b_conv1 = bias_variable([32])


# In[209]:


x_image = tf.reshape(x, [-1,28,28,1])


# In[210]:


h_conv1 = tf.nn.relu(conv2d(x_image, W_conv1) + b_conv1)
h_pool1 = max_pool_2x2(h_conv1)


# In[211]:



W_conv2 = tf.get_variable("W_conv2", shape=[5, 5, 32, 64],
           initializer=tf.contrib.layers.xavier_initializer())
b_conv2 = bias_variable([64])

h_conv2 = tf.nn.relu(conv2d(h_pool1, W_conv2) + b_conv2)
h_pool2 = max_pool_2x2(h_conv2)


W_conv3 = tf.get_variable("W_conv3", shape=[5, 5, 64, 128],
           initializer=tf.contrib.layers.xavier_initializer())
b_conv3 = bias_variable([128])

h_conv3 = tf.nn.relu(conv2d(h_pool2, W_conv3) + b_conv3)
h_pool3 = max_pool_2x2(h_conv3)


# In[212]:


W_fc1 = weight_variable([4 * 4 *128 , 1024])
b_fc1 = bias_variable([1024])

h_pool3_flat = tf.reshape(h_pool3, [-1, 4*4*128])
h_fc1 = tf.nn.relu(tf.matmul(h_pool3_flat, W_fc1) + b_fc1)


# In[213]:


keep_prob = tf.placeholder(tf.float32)
h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)


# In[214]:


W_fc2 = weight_variable([1024, 10])
b_fc2 = bias_variable([10])

y_conv=tf.nn.softmax(tf.matmul(h_fc1_drop, W_fc2) + b_fc2)


# In[215]:


cross_entropy = tf.reduce_mean(-tf.reduce_sum(y_ * tf.log(y_conv), reduction_indices=[1]))
train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)
correct_prediction = tf.equal(tf.argmax(y_conv,1), tf.argmax(y_,1))
accuracy = tf.reduce_mean(tf.cast(correct_prediction, tf.float32))
sess.run(tf.global_variables_initializer())
for i in range(1000):
  batch = mnist.train.next_batch(50)
  if i%100 == 0:
    train_accuracy = accuracy.eval(feed_dict={
        x:batch[0], y_: batch[1], keep_prob: 1.0})
    print("step %d, training accuracy %g"%(i, train_accuracy))
  train_step.run(feed_dict={x: batch[0], y_: batch[1], keep_prob: 0.5})

print("test accuracy %g"%accuracy.eval(feed_dict={
    x: mnist.test.images, y_: mnist.test.labels, keep_prob: 1.0}))


# In[41]:




