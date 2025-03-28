import os
os.environ['CUDA_VISIBLE_DEVICES'] = '0' #指定GPU编
import torch
import numpy as np
from tqdm import tqdm
from netron import NeuralNetwork


batch_size = 320                        #设定每次训练的批次数
epochs = 30                           #设定训练次数

#device = "cpu"                         #Pytorch的特性，需要指定计算的硬件，如果没有GPU的存在，就使用CPU进行计算
device = "cuda"                         #在这里读者默认使用GPU，如果读者出现运行问题可以将其改成cpu模式

model = NeuralNetwork()
model = model.to(device)                #将计算模型传入GPU硬件等待计算
torch.save(model, './model.pth')
model = torch.compile(model)            #Pytorch2.0的特性，加速计算速度
loss_fu = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=2e-5)   #设定优化函数

#载入数据
x_train = np.load("../../dataset/mnist/x_train.npy")
y_train_label = np.load("../../dataset/mnist/y_train_label.npy")

train_num = len(x_train)//batch_size

#开始计算
for epoch in range(epochs):
    train_loss = 0
    accuracy = 0
    for i in range(train_num):
        start = i * batch_size
        end = (i + 1) * batch_size

        # todo 对 torch.Tensor 进行截取操作时 [start:end]，如果 end 超过其长度，不会报错，只会取到最后一个。
        train_batch = torch.tensor(x_train[start:end]).to(device)
        label_batch = torch.tensor(y_train_label[start:end]).to(device)

        pred = model(train_batch)
        loss = loss_fu(pred,label_batch)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        train_loss += loss.item()  # 记录每个批次的损失值
        # todo 原来的 accuracy 实际上只计算了最后一个 batch
        # todo 注意这个 argmax()，如果没有参数，返回的是 input(tensor).flatten() 的最大元素下标；
        #   而 input.argmax(0) 则表示：行之间（每个元素）比较大小，一列一个结果，结果长度为 dim(0)；
        #   input.argmax(1) 表示列之间比较大小，一行一个结果，结果长度为 dim(1)；
        #   pred.argmax(1) 表示找到每行中最大值所在下标，对应于预测认为最有可能的数字的位置，对应于分类结果。
        accuracy += (pred.argmax(1) == label_batch).type(torch.float32).sum().item()

    # 计算并打印损失值
    train_loss /= train_num
    accuracy /= len(x_train)
    print("epoch：",epoch,"train_loss:", round(train_loss,2),"accuracy:",round(accuracy,2))
