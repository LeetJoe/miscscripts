import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
import gzip
from struct import unpack

train_num=60000  # 训练集样本数
test_num=10000  # 测试集样本数
img_dim=(1,28,28)  # 图像维度
img_size=784  # 28*28的图像

x_train_path=r'D:\deep_learning_pratice\mnist\train_images\train-images-idx3-ubyte.gz'
y_train_path=r'D:\deep_learning_pratice\mnist\train_labels\train-labels-idx1-ubyte.gz'
x_test_path=r'D:\deep_learning_pratice\mnist\test_images\t10k-images-idx3-ubyte.gz'
y_test_path=r'D:\deep_learning_pratice\mnist\test_labels\t10k-labels-idx1-ubyte.gz'


def read_image(path):  # 读取图像数据
    with gzip.open(path,'rb') as f:
        magic,num,rows,cols=unpack('>4I',f.read(16))
        img=np.frombuffer(f.read(),dtype=np.uint8).reshape(num,28*28)
    return img


def read_label(path):  # 读取label数据
    with gzip.open(path,'rb') as f:
        magic,num=unpack('>2I',f.read(8))
        label=np.frombuffer(f.read(),dtype=np.uint8)
    return label


def normalize_image(image):  # 图像灰度值的标准化
    img=image.astype(np.float32)/255.0
    return img


def one_hot_label(label):  # 图像标签的one-hot向量化
    lab=np.zeros((label.size,10))
    for i,row in enumerate(lab):
        row[label[i]]=1
    return lab


def load_mnist(x_train_path,y_train_path,x_test_path,y_test_path,normalize=True,one_hot=True):  # 读取mnist数据集
    '''
    Parameter
    --------
    normalize：将图像的像素值标准化到0~1区间
    one_hot：返回的label是one_hot向量

    Return
    --------
    (训练图像，训练标签)，(测试图像，测试标签)
    '''
    image={
        'train':read_image(x_train_path),
        'test':read_image(x_test_path)
    }

    label={
        'train':read_label(y_train_path),
        'test':read_label(y_test_path)
    }

    if normalize:
        for key in ('train','test'):
            image[key]=normalize_image(image[key])

    if one_hot:
        for key in ('train','test'):
            label[key]=one_hot_label(label[key])

    return (image['train'],label['train']),(image['test'],label['test'])

def generatebatch(X,Y,n_examples, batch_size):
    for batch_i in range(n_examples // batch_size):
        start = batch_i*batch_size
        end = start + batch_size
        batch_xs = X[start:end]
        batch_ys = Y[start:end]
        yield batch_xs, batch_ys # 生成每一个batch


(x_train,y_train),(x_test,y_test)=load_mnist(x_train_path,y_train_path,x_test_path,y_test_path,normalize=True,one_hot=True)
'''
f,ax=plt.subplots(2,2)
ax[0,0].imshow(x_train[0].reshape(28,28),cmap='Greys')  # 灰度图，reshape为28*28的像素图
ax[0,1].imshow(x_train[1].reshape(28,28),cmap='Greys')
ax[1,0].imshow(x_train[2].reshape(28,28),cmap='Greys')
ax[1,1].imshow(x_train[3].reshape(28,28),cmap='Greys')
plt.show()
'''
# 创建占位符
x=tf.placeholder("float",shape=[None,784])  # x是输入的图像数据维度，28*28=784，初始化为784维
y=tf.placeholder("float",shape=[None,10])  # y是图像类别的标签维度，0~9一共10个数字，初始化为10维

# 定义卷积层1的权重和bias
w_conv1=tf.Variable(tf.truncated_normal([5,5,1,32],stddev=0.1)) # 截断生成正态分布随机数
b_conv1=tf.Variable(tf.constant(0.1,shape=[32]))  # 初始化bias，值均为0.1


# 搭建卷积层1
x_image=tf.reshape(x,[-1,28,28,1])  # [batch_size, height, weight, channel]
r_conv1=tf.nn.conv2d(x_image,w_conv1,strides=[1,1,1,1],padding='SAME')+b_conv1  # [batch_size, filter_height, filter_weight, nums]
h_conv1=tf.nn.relu(r_conv1)

# 搭建池化层1
h_pool1=tf.nn.max_pool(h_conv1,ksize=[1,2,2,1],strides=[1,2,2,1],padding='SAME')

# 定义卷积层2的权重和bias
w_conv2=tf.Variable(tf.truncated_normal([5,5,32,64],stddev=0.1))
b_conv2=tf.Variable(tf.constant(0.1,shape=[64]))

# 搭建卷积层2
r_conv2=tf.nn.conv2d(h_pool1,w_conv2,strides=[1,1,1,1],padding='SAME')+b_conv2
h_conv2=tf.nn.relu(r_conv2)

# 搭建池化层2
h_pool2=tf.nn.max_pool(h_conv2,ksize=[1,2,2,1],strides=[1,2,2,1],padding='SAME')

# 定义全连接层的权重和bias
w_fc1=tf.Variable(tf.truncated_normal([7*7*64,1024],stddev=0.1))
b_fc1=tf.Variable(tf.constant(0.1,shape=[1024]))

# 搭建全连接层
h_pool2_flat=tf.reshape(h_pool2,[-1,7*7*64])
h_fc1=tf.nn.relu(tf.matmul(h_pool2_flat,w_fc1)+b_fc1)

# 添加dropout
keep_prob=tf.placeholder(tf.float32)
h_fc1_drop=tf.nn.dropout(h_fc1,keep_prob)

# 搭建输出层
w_fc2=tf.Variable(tf.truncated_normal([1024,10],stddev=0.1))
b_fc2=tf.Variable(tf.constant(0.1,shape=[10]))
y_conv=tf.nn.softmax(tf.matmul(h_fc1_drop,w_fc2)+b_fc2)

# 做交叉熵
cross_entropy=-tf.reduce_sum(y*tf.log(y_conv))

# 梯度下降法
train_step=tf.train.AdamOptimizer(1e-4).minimize(cross_entropy)

# 计算正确率
correct_prediction=tf.equal(tf.argmax(y_conv,1),tf.argmax(y,1))

accuracy=tf.reduce_mean(tf.cast(correct_prediction,"float"))

with tf.Session() as sess:
    sess.run(tf.global_variables_initializer())
    for epoch in range(5):
        for batch_xs,batch_ys in generatebatch(x_train,y_train,60000,50):
            sess.run(train_step,feed_dict={x:batch_xs,y:batch_ys,keep_prob:0.5})
        if epoch % 1 ==0:
            print("Epoch {0}, accuracy: {1}".format(epoch,sess.run(accuracy,feed_dict={x:x_test,y:y_test,keep_prob:1.0})))
            print(sess.run(y_conv[:10],feed_dict={x:batch_xs,y:batch_ys,keep_prob:1.0}))
            print(sess.run(y[:10],feed_dict={x:batch_xs,y:batch_ys,keep_prob:1.0}))