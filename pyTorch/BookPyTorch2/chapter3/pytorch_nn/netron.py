import torch
device = "cuda"                         #在这里读者默认使用GPU，如果读者出现运行问题可以将其改成cpu模式
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

#设定的多层感知机网络模型
class NeuralNetwork(torch.nn.Module):
    def __init__(self):
        super(NeuralNetwork, self).__init__()
        self.flatten = torch.nn.Flatten()
        # todo Sequential 的 model 属于比较简单一类的模型结构，就是一层一层的节点堆叠，每两层
        #   结点之间加一个激活函数。其重点还是输入输出的维度必须与输入数据的情况和输出的目标相符，
        #   然后就是层与层之间的维度必须要对应。（至于为什么要这么设计这么堆迭，现在来看还是玄学）
        self.linear_relu_stack = torch.nn.Sequential(
            torch.nn.Linear(28*28,312),
            torch.nn.ReLU(),
            torch.nn.Linear(312, 256),
            torch.nn.ReLU(),
            torch.nn.Linear(256, 10)
        )
    def forward(self, input):
        x = self.flatten(input)
        # todo 原始的 sequential 实例是否可以视作某个层次上的 model？其处理输入的模式与
        #  model.forward() 的调用方式类似。
        #  而对 forward 而言，forward 里还可以做很多其它工作。
        logits = self.linear_relu_stack(x)

        return logits

# todo 这样上面定义的 NN 就可以被其它文件引用，如果作 __name__ 这步判断，引用的时候会导致下面的代码执行。
if __name__ == "__main__":
    model = NeuralNetwork()
    model = model.to(device)                #将计算模型传入GPU硬件等待计算
    torch.save(model, './model.pth')
