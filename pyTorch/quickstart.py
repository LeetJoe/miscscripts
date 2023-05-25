import torch
from torch import nn
from torch.utils.data import DataLoader
from torchvision import datasets
from torchvision.transforms import ToTensor


import random

# from coati.models.llama import LlamaLM


# Define model
class NeuralNetworkModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.flatten = nn.Flatten()
        self.linear_relu_stack = nn.Sequential(    # 一组变换序列，从28*28的图片变换成维度为10的向量，从而实现分类。
            nn.Linear(28*28, 512),
            nn.ReLU(),   # ReLU, Rectified Linear Unit，线性整流函数
            nn.Linear(512, 512),
            nn.ReLU(),
            nn.Linear(512, 10)
        )

    def forward(self, x):       # 应该是基类里的抽象方法，必须要实现的，就像有些类里的run()一样。
        x = self.flatten(x)
        logits = self.linear_relu_stack(x)
        return logits


def train(train_dataloader, model, loss_fn, optimizer):
    size = len(train_dataloader.dataset)
    model.train()     # set the model in training mode，设置为训练模式，训练结果会修改模型的状态（？）。
    for batch, (X, y) in enumerate(train_dataloader):       # 这种写法里，batch是循环次数，从0开始计数；X和y的含义不变。
        X, y = X.to(device), y.to(device)                   # Tensor to device?

        # Compute prediction error
        pred = model(X)            # pred.shape = [64, 10]，是对这一批64张图片进行的分类预测
        loss = loss_fn(pred, y)    # 将预测结果pred与实际标注y比较，得到一个数值，数值越大损失（误差）越大。loss.item()可取得其中的数值。

        # Backpropagation
        optimizer.zero_grad()      # 反向传播？？可能是针对损失情况对预测进行修正？
        loss.backward()
        optimizer.step()

        if batch % 100 == 0:       # 每循环100次，即每处理6400条，输出一下状态
            loss, current = loss.item(), (batch + 1) * len(X)
            print(f"loss: {loss:>7f}  [{current:>5d}/{size:>5d}]")


def test(dataloader, model, loss_fn):
    size = len(dataloader.dataset)
    num_batches = len(dataloader)
    model.eval()       # set the model in evaluation mode，设置为评估模式
    test_loss, correct = 0, 0
    with torch.no_grad():
        for X, y in dataloader:     # 使用另一组样本进行模型预测准确率的评估
            X, y = X.to(device), y.to(device)
            pred = model(X)
            test_loss += loss_fn(pred, y).item()
            correct += (pred.argmax(1) == y).type(torch.float).sum().item()
    test_loss /= num_batches
    correct /= size
    print(f"Test Error: \n Accuracy: {(100*correct):>0.1f}%, Avg loss: {test_loss:>8f} \n")


# Download training data from open datasets.
training_data = datasets.FashionMNIST(         # 结构是[60000,2,1,28,28]
    root="data",
    train=True,
    download=True,
    transform=ToTensor(),
)

# Download test data from open datasets.
test_data = datasets.FashionMNIST(             # 结构是[10000,2,1,28,28]
    root="data",
    train=False,
    download=True,
    transform=ToTensor(),
)

batch_size = 64

# Create data loaders.
train_dataloader = DataLoader(training_data, batch_size=batch_size)
test_dataloader = DataLoader(test_data, batch_size=batch_size)


for X, y in test_dataloader:        # 是一个iterable，根据batch_size对data进行分批，这里就只是看看结构，展示分批效果，无实际功能。
    print(f"Shape of X [N, C, H, W]: {X.shape}")     # N=64，这一批数据的容量；C=1，H=28，W=28，参考上面data的结构
    print(f"Shape of y: {y.shape} {y.dtype}")        # y是64个tensor.int64，对应X里64张图片
    break

# Get cpu, gpu or mps device for training.
device = (
    "cuda"
    if torch.cuda.is_available()
    else "mps"
    if torch.backends.mps.is_available()
    else "cpu"
)
print(f"Using {device} device")

model = NeuralNetworkModel().to(device)

loss_fn = nn.CrossEntropyLoss()    # 损失函数，这里实现为叉熵损失。
optimizer = torch.optim.SGD(model.parameters(), lr=1e-3)    # 优化器，用来根据损失来优化模型提高准确率的？而不是指硬件性能优化。


epochs = 10   #  训练的时候，损失从2.2降到1.2（5轮）降到0.8（10轮），在5轮时，预测出错的概率还是很高的；10轮的时候出错的概率已经大大下降了。
for t in range(epochs):
    print(f"Epoch {t+1}\n-------------------------------")
    train(train_dataloader, model, loss_fn, optimizer)     # 执行一轮(Epoch)训练
    test(test_dataloader, model, loss_fn)                  # 评估训练结果，每过一轮评估准确率都会提高一些。
print("Done!")

torch.save(model.state_dict(), "neosong_model.pth")        # 保存之前的训练结果
print("Saved PyTorch Model State to neosong_model.pth")

model = NeuralNetworkModel()                               # 这是一个新的model实例
model.load_state_dict(torch.load("neosong_model.pth"))     # 加载前面的训练结果(state)

classes = [              # 就是一个id到name的映射，为了human read。
    "T-shirt/top",
    "Trouser",
    "Pullover",
    "Dress",
    "Coat",
    "Sandal",
    "Shirt",
    "Sneaker",
    "Bag",
    "Ankle boot",
]

model.eval()          # 进入评估模式
for i in range(5):
    idx = random.randint(0, 9999)
    x, y = test_data[idx][0], test_data[idx][1]    # 现在x里是一个图片数组，x是它标记的名称
    with torch.no_grad():    # disabled gradient calculation，停用梯度运算？？
        pred = model(x)      # 对x进行预测
        predicted, actual = classes[pred[0].argmax(0)], classes[y]     # 分别是预测的分类，实际的分类
        print(f'Turn {i}: Predicted: "{predicted}", Actual: "{actual}"')
