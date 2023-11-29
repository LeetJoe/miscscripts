import numpy as np

print(np.__version__)

np.show_config()    # may prompt to install pyyaml

Z = np.zeros(10, dtype=np.int32)    # an vector of 10 with only 0s

Z_mem = Z.size * Z.itemsize    # mem allocated to Z in Byte

np.info(np.add)    # show the manual of function built in Numpy

Z[4] = 1    # Z is all 0s except pos 4

Z = np.arange(10, 50)    # [10, 50)

Z = Z[::-1]   # revert a vector

Z = Z.reshape(5, 8)   # reshape Z to a 5 x 8 matrix

Z = [1, 2, 3, 0, 4, 9, 0, 2, 0]

I = np.nonzero(Z)   # index list of Z where not zero

Z = np.eye(10)   # I of size 10

# 注意有两层括号，里面那层 (3,3,3) 整个作为 random() 的第一个参数
Z = np.random.random((3, 3, 3))    # generate a random matrix of 3x3x3

Z_min = Z.min()    # get the min/max of the matrix
Z_max = Z.max()

Z = np.random.random(10)
Z_mean = Z.mean()     # get mean of a vector or matrix

# numpy 擅长画矩形，不擅长画方框，把画方框的操作变换成一个大矩形减一个小矩形的操作
Z = np.ones((10, 10))
Z[1:-1, 1:-1] = 0    # 将内部一定范围里的矩形赋另外的值，得到一个边界是 1 内部是 0 的矩阵。

# 16. 对于一个存在在数组，如何添加一个用 3 填充的边界?

np.pad(Z, pad_width=1, mode='constant', constant_values=3)

# 17. 以下表达式运行的结果分别是什么?

Z = 0*np.nan

Z = np.nan==np.nan

Z = np.inf>np.nan

Z = np.nan-np.nan

Z = 0.3==3*0.1

# np.nan 表示非数，它与任何数字进行四则运算得到的都是 nan, 与任何数字进行比较返回的都是 false； 0.1*3=0.30000000000000004
# 可以使用 np.round(0.300002, 2) 来对小数进行舍入

# 19. 创建一个8x8 的矩阵，并且设置成棋盘样式

Z = np.zeros((10, 10))
Z[1::2, ::2] = 1
Z[::2, 1::2] = 1

# 20. 考虑一个 (6,7,8) 形状的数组，其第100个元素的索引(x,y,z)是什么?

Z = np.unravel_index(100, (6, 7, 8))

# 这个仅用来进行计算，组出数组 shape 即可，不需要使用真实的数组。
# todo 第一个参数可以是数组，但是输出结果有点不太理解

# 21. 用tile函数去创建一个 8x8的棋盘样式矩阵

np.tile(np.array([[0, 1],[1, 0]]), (4, 4))

# 第一个参数直接给了一个矩阵，然后用矩阵重复 tile 得到目标结果。第一个参数也可以向量，自己组合尝试下不同的结果。

# 22. 对一个5x5的随机矩阵做归一化

Z = np.random.random((5,5))
Zmax, Zmin = Z.max(), Z.min()
Z = (Z - Zmin)/(Zmax - Zmin)
print(Z)

# 23. 创建一个将颜色描述为(RGBA)四个无符号字节的自定义dtype？

color = np.dtype([("r", np.ubyte, (1,)),
("g", np.ubyte, (1,)),
("b", np.ubyte, (1,)),
("a", np.ubyte, (1,))])

# dtype([('r', 'u1', (1,)), ('g', 'u1', (1,)), ('b', 'u1', (1,)), ('a', 'u1', (1,))])
# 但是不清楚这个要怎么用？

# 24. 一个5x3的矩阵与一个3x2的矩阵相乘，实矩阵乘积是什么？

Z = np.dot(np.ones((5,3)), np.ones((3,2)))

# 点乘要使用 np.dot()，不能直接让矩阵相乘。

# 25. 给定一个一维数组，对其在3到8之间的所有元素取反

Z = np.arange(11)
Z[(Z > 3) & (Z <= 8)] *= -1
Z[(3 < 3) & (Z <= 8)] *= -1

# 上面两个式子结果是一样的


# 26. 下面脚本运行后的结果是什么?

print(sum(range(5),-1))  # 输出是数组的和，加上第二个参数

# todo 实测不 import numpy 也可以用 sum(range(10), 2)

# 27. 考虑一个整数向量Z,下列表达合法的是哪个?

Z = np.arange(10)

Z**Z  # 相当于将数组中每一个数字，按其值对自己取幂

2<<Z>>2 # 2<<Z 表示以 2 为底数，Z 中的数字为指数求各个位置的幂形成新的向量；再 >>2 表示按二进制右移两位，相当于除以 4 向下取整。

Z<-Z  # Z 直接与数字比较，相当于对 Z 中各个位置分别比较并将结果放在对应位置；如果两个向量比较，则接对应位置比较，结果放在对应位置。

1j*Z  # 这里 1j 表示虚数，在 python 里用 j 表示虚数。各对应位置表示为虚数，如 0.+5.j

# 28. 下列表达式的结果分别是什么?

# 29. 如何从零位对浮点数组做舍入 ?

Z = np.random.uniform(-10,+10,10)  # 按均匀分布，在 -10 到 10 之间生成 10 个样本
print(np.copysign(np.ceil(np.abs(Z)), Z)) # 如果直接使用 ceil，正负值都向上取，然而有时候需要对负值按其绝对值取 ceil。这里先取 abs 再用 ceil，再用 copysign 可以实现。

# 30. 如何找到两个数组中的共同元素?

Z1 = np.random.randint(0,10,10)
Z2 = np.random.randint(0,10,10)

print(np.intersect1d(Z1,Z2))     # 只有 intersect1d，没有 intersect2d

# imaginary number can not generated by np.sqrt(-1), we will get an error. We should use np.emath.sqrt(-1) and We will get 1j.

np.emath.sqrt(-1)

# 33 calculate date time by numpy

# date time of today in Date mimus time delta 1 day
np.datetime64('today', 'D') - np.timedelta64(1, 'D')

# 35. 如何直接在位计算(A+B)\*(-A/2)(不建立副本)? A = A + B can not be used

A = np.ones(3)*1
B = np.ones(3)*2
C = np.ones(3)*3
np.add(A,B,out=B)
np.divide(A,2,out=A)
np.negative(A,out=A)
np.multiply(A,B,out=A)


# calculate the norm of a matrix

A = np.random.random((4, 4))

# axis=1 means calc norm along rows, default 0; ord=n means the n-norm, default 2
A_norm = np.linalg.norm(A, axis=1)

