import numpy as np
import gzip
import os
from struct import unpack


def read_image(path):  # 读取图像数据
    with gzip.open(path, 'rb') as f:
        magic, num, rows, cols = unpack('>4I', f.read(16))
        img = np.frombuffer(f.read(), dtype=np.uint8).reshape(num, 28 * 28)
    return img


def read_label(path):  # 读取label数据
    with gzip.open(path, 'rb') as f:
        magic, num = unpack('>2I', f.read(8))
        label = np.frombuffer(f.read(), dtype=np.uint8)
    return label


def normalize_image(image):  # 图像灰度值的标准化
    img = image.astype(np.float32) / 255.0
    return img


def one_hot_label(label):  # 图像标签的one-hot向量化
    lab = np.zeros((label.size, 10))
    for i, row in enumerate(lab):
        row[label[i]] = 1
    return lab


def load_mnist(data_path, normalize=True, one_hot=False, train_num=10000, test_num=2000):  # 读取mnist数据集
    '''
    图像维度 img_dim = (1, 28, 28)
    28*28的图像 img_size = 784

    Parameter
    --------
    normalize：将图像的像素值标准化到0~1区间
    one_hot：返回的label是one_hot向量
    train_num = 10000  # 训练集样本数
    test_num = 2000  # 测试集样本数

    Return
    --------
    (训练图像，训练标签)，(测试图像，测试标签)
    '''
    x_train_path = os.path.join(data_path, 'train-images-idx3-ubyte.gz')
    y_train_path = os.path.join(data_path, 'train-labels-idx1-ubyte.gz')
    x_test_path = os.path.join(data_path, 't10k-images-idx3-ubyte.gz')
    y_test_path = os.path.join(data_path, 't10k-labels-idx1-ubyte.gz')

    image = {
        'train': read_image(x_train_path),
        'test': read_image(x_test_path)
    }

    label = {
        'train': read_label(y_train_path),
        'test': read_label(y_test_path)
    }

    if normalize:
        for key in ('train', 'test'):
            image[key] = normalize_image(image[key])

    if one_hot:
        for key in ('train', 'test'):
            label[key] = one_hot_label(label[key])

    print("train num: {}, test num: {}".format(train_num, test_num))
    return (image['train'][:train_num], label['train'][:train_num]), (image['test'][:test_num], label['test'][:test_num])


def generatebatch(X, Y, n_examples, batch_size):
    for batch_i in range(n_examples // batch_size):
        start = batch_i * batch_size
        end = start + batch_size
        batch_xs = X[start:end]
        batch_ys = Y[start:end]
        yield batch_xs, batch_ys  # 生成每一个batch
