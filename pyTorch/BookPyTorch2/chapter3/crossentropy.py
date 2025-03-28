import torch

y = torch.LongTensor([0])
z = torch.Tensor([[0.1,0.01,-0.01]])
# todo 交叉熵是比较的两者分布越接近，结果越小。
criterion = torch.nn.CrossEntropyLoss()
loss = criterion(z,y)
print(y)
print(z)
print(loss.item())
