import os
os.environ['CUDA_VISIBLE_DEVICES'] = '0' #指定GPU编
import torch
import numpy as np
from tqdm import tqdm

batch_size = 320                        #设定每次训练的批次数
epochs = 1024                           #设定训练次数

#device = "cpu"                         #Pytorch的特性，需要指定计算的硬件，如果没有GPU的存在，就使用CPU进行计算
device = "cuda"                         #在这里读者默认使用GPU，如果读者出现运行问题可以将其改成cpu模式


#设定的多层感知机网络模型
class NeuralNetwork(torch.nn.Module):
    def __init__(self):
        super(NeuralNetwork, self).__init__()
        self.flatten = torch.nn.Flatten()
        self.linear_relu_stack = torch.nn.Sequential(
            torch.nn.Linear(28*28,312),
            torch.nn.ReLU(),
            torch.nn.Linear(312, 256),
            torch.nn.ReLU(),
            torch.nn.Linear(256, 10)
        )
    def forward(self, input):
        x = self.flatten(input)
        logits = self.linear_relu_stack(x)

        return logits

model = NeuralNetwork()
model = model.to(device)                #将计算模型传入GPU硬件等待计算
torch.save(model, './model.pth')
#model = torch.compile(model)            #Pytorch2.0的特性，加速计算速度
loss_fu = torch.nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(model.parameters(), lr=2e-5)   #设定优化函数

#载入数据
x_train = np.load("../../dataset/mnist/x_train.npy")
y_train_label = np.load("../../dataset/mnist/y_train_label.npy")

train_num = len(x_train)//batch_size

#开始计算
for epoch in range(20):
    train_loss = 0
    for i in range(train_num):
        start = i * batch_size
        end = (i + 1) * batch_size

        train_batch = torch.tensor(x_train[start:end]).to(device)
        label_batch = torch.tensor(y_train_label[start:end]).to(device)

        pred = model(train_batch)
        loss = loss_fu(pred,label_batch)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        train_loss += loss.item()  # 记录每个批次的损失值

    # 计算并打印损失值
    train_loss /= train_num
    accuracy = (pred.argmax(1) == label_batch).type(torch.float32).sum().item() / batch_size
    print("epoch：",epoch,"train_loss:", round(train_loss,2),"accuracy:",round(accuracy,2))
