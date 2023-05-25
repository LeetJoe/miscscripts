import torch
import numpy as np


data = [[1, 2],[3, 4]]
x_data = torch.tensor(data)

np_array = np.array(data)
x_np = torch.from_numpy(np_array)


x_ones = torch.ones_like(x_data) # retains the properties of x_data
print(f"Ones Tensor: \n {x_ones} \n")

x_rand = torch.rand_like(x_data, dtype=torch.float) # overrides the datatype of x_data
print(f"Random Tensor: \n {x_rand} \n")

shape = (3,4,)
rand_tensor = torch.rand(shape)
ones_tensor = torch.ones(shape)
zeros_tensor = torch.zeros(shape)

print(f"Random Tensor: \n {rand_tensor} \n")
print(f"Ones Tensor: \n {ones_tensor} \n")
print(f"Zeros Tensor: \n {zeros_tensor}")


tensor = torch.rand(3,4)

# We move our tensor to the GPU if available
if torch.cuda.is_available():
    tensor = tensor.to("cuda")

print(f"Shape of tensor: {tensor.shape}")
print(f"Datatype of tensor: {tensor.dtype}")
print(f"Device tensor is stored on: {tensor.device}")


tensor = torch.ones(4, 4)
print(f"First row: {tensor[0]}")
print(f"First column: {tensor[:, 0]}")
print(f"Last column: {tensor[..., -1]}")
print(tensor[..., -1] == tensor[:, 3])   # tensor([True, True, True, True]) ??
tensor[:,1] = 0
print(tensor)


tensor = torch.ones(4, 4)

# 三个 4 * 4 矩阵拼接在一起成为一个 4 * 12 的矩阵。dim = 1 表示按列拼接， dim = 0 表示按行拼接。
t1 = torch.cat([tensor, tensor, tensor], dim=0)
print(t1)



tensor = torch.ones(4, 4)
tensor[1,:] = 0


# This computes the matrix multiplication between two tensors. y1, y2, y3 will have the same value
# ``tensor.T`` returns the transpose of a tensor

y1 = tensor @ tensor.T
y2 = tensor.matmul(tensor.T)


y3 = torch.rand_like(y1)
torch.matmul(tensor, tensor.T, out=y3)


# This computes the element-wise product. z1, z2, z3 will have the same value
# 按元素积，而非矩阵乘。z1 * z2 = z3, 则z3[x, y] = z1[x, y] * z2[x, y]
z1 = tensor * tensor
z2 = tensor.mul(tensor)


z3 = torch.rand_like(tensor)
torch.mul(tensor, tensor, out=z3)

# element-wise 平方再开方，然后累加
print(torch.pow(tensor, 2).sqrt().sum())

# element-wise 累加
agg = tensor.sum()

# agg里面只有一个值的时候可以，如果agg是一个矩阵或者向量，就不能使用agg.item()
agg_item = agg.item()
print(agg_item, type(agg_item))


tensor = torch.ones(4, 4)
tensor[:,0] = -1
tensor[:,1] = -1

print(f"{tensor} \n")
tensor.add_(5)
print(tensor)

t = torch.ones(5)
print(f"t: {t}")
n = t.numpy()  # 直接将 tensor 转化成 numpy
print(f"n: {n}")

# t.add_(1) <=> t += 1, t.add_(torch.rand(5)) <=> t+= torch.rand(5)
# t.add(1)不会直接改变t的值，需要使用变量接受返回值，如t = t.add(1)，而且这句里t的值变了，n的值却不会跟着变。

t1 = t.add(1)
t = t.add(1)
print(f"t: {t}")
print(f"t1: {t1}")
print(f"n: {n}")


n = np.ones(5)
t = torch.from_numpy(n)

np.add(n, 1, out=n)
print(f"t: {t}")
print(f"n: {n}")


