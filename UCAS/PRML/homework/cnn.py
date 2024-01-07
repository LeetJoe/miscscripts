import tensorflow as tf
import time

from utils import load_mnist, generatebatch


data_path = '../data/'
(x_train, y_train), (x_test, y_test) = load_mnist(data_path, normalize=True, one_hot=True)

# 创建占位符
x = tf.placeholder("float", shape=[None, 784])  # x是输入的图像数据维度，28*28=784，初始化为784维
y = tf.placeholder("float", shape=[None, 10])  # y是图像类别的标签维度，0~9一共10个数字，初始化为10维

# 定义卷积层1的权重和bias
w_conv1 = tf.Variable(tf.truncated_normal([5, 5, 1, 32], stddev=0.1))  # 截断生成正态分布随机数
b_conv1 = tf.Variable(tf.constant(0.1, shape=[32]))  # 初始化bias，值均为0.1

# 搭建卷积层1
x_image = tf.reshape(x, [-1, 28, 28, 1])  # [batch_size, height, weight, channel]
r_conv1 = tf.nn.conv2d(x_image, w_conv1, strides=[1, 1, 1, 1],
                       padding='SAME') + b_conv1  # [batch_size, filter_height, filter_weight, nums]
h_conv1 = tf.nn.relu(r_conv1)

# 搭建池化层1
h_pool1 = tf.nn.max_pool(h_conv1, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

# 定义卷积层2的权重和bias
w_conv2 = tf.Variable(tf.truncated_normal([5, 5, 32, 64], stddev=0.1))
b_conv2 = tf.Variable(tf.constant(0.1, shape=[64]))

# 搭建卷积层2
r_conv2 = tf.nn.conv2d(h_pool1, w_conv2, strides=[1, 1, 1, 1], padding='SAME') + b_conv2
h_conv2 = tf.nn.relu(r_conv2)

# 搭建池化层2
h_pool2 = tf.nn.max_pool(h_conv2, ksize=[1, 2, 2, 1], strides=[1, 2, 2, 1], padding='SAME')

# 定义全连接层的权重和bias
w_fc1 = tf.Variable(tf.truncated_normal([7 * 7 * 64, 1024], stddev=0.1))
b_fc1 = tf.Variable(tf.constant(0.1, shape=[1024]))

# 搭建全连接层
h_pool2_flat = tf.reshape(h_pool2, [-1, 7 * 7 * 64])
h_fc1 = tf.nn.relu(tf.matmul(h_pool2_flat, w_fc1) + b_fc1)

# 添加dropout
keep_prob = tf.placeholder(tf.float32)
h_fc1_drop = tf.nn.dropout(h_fc1, keep_prob)

# 搭建输出层
w_fc2 = tf.Variable(tf.truncated_normal([1024, 10], stddev=0.1))
b_fc2 = tf.Variable(tf.constant(0.1, shape=[10]))
y_conv = tf.nn.softmax(tf.matmul(h_fc1_drop, w_fc2) + b_fc2)

# 做交叉熵
cross_entropy = -tf.reduce_sum(y * tf.log(y_conv))

# 梯度下降法
train_step = tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)

# 计算正确率
correct_prediction = tf.equal(tf.argmax(y_conv, 1), tf.argmax(y, 1))

accuracy = tf.reduce_mean(tf.cast(correct_prediction, "float"))

stop_acc = 0.95
print("Start CNN Training...")
StartTime = time.clock()
with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    for epoch in range(10):
        bnum = 0
        for batch_xs, batch_ys in generatebatch(x_train, y_train, 10000, 50):
            sess.run(train_step, feed_dict={x: batch_xs, y: batch_ys, keep_prob: 0.5})
        if epoch % 1 == 0:
            epoch_acc = sess.run(accuracy, feed_dict={x: x_test[:2000], y: y_test[:2000], keep_prob: 1.0})
            print("Epoch {}, accuracy: {:.4f}".format(epoch, epoch_acc))
            # print(sess.run(y_conv[:10], feed_dict={x: batch_xs, y: batch_ys, keep_prob: 1.0}))
            # print(sess.run(y[:10], feed_dict={x: batch_xs, y: batch_ys, keep_prob: 1.0}))

            if epoch_acc > stop_acc:
                break

EndTime = time.clock()
print('Total time %.2f s' % (EndTime - StartTime))