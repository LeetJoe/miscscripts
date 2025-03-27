import numpy as np
import torch
x_train = np.load("../dataset/mnist/x_train.npy")
y_train_label = np.load("../dataset/mnist/y_train_label.npy")
x = torch.tensor(y_train_label[:5],dtype=torch.int64)
# 定义一个张量输入，因为此时有 5 个数值，且最大值为9，类别数为10
# 所以我们可以得到 y 的输出结果的形状为 shape=(5,10)，即5行12列
y = torch.nn.functional.one_hot(x, 10)  # 一个参数张量x，10为类别数
print(y)