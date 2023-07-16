import numpy as np
import matplotlib.pyplot as plt


# 使用均方差方法求 theta，公式为 y = ax + b，theta = [[b], [a]], x 为自变量， y 是预测值，theta 用来估计 a 和 b。
def get_theta(x, y):
    m = len(y)
    # x中新增一列常数1
    x = np.c_[np.ones(m).T, x]
    # 通过公式计算theta
    theta = np.dot(np.dot(np.linalg.inv(np.dot(x.T, x)), x.T), y)
    return theta

# 使用梯度下降法来计算 theta
def gradient_get_theta(X, y):
    eta = 0.1  # 学习率
    n_iterations = 1000  # 迭代次数
    m = 100

    theta = np.random.randn(2, 1)  # 随机初始值
    X = np.c_[np.ones(100).T, X]
    for iteration in range(n_iterations):
        gradients = 1 / m * X.T.dot(X.dot(theta) - y)  # 根据梯度公式迭代
        theta = theta - eta * gradients
    return theta

def show_graph(X, y, theta):
    # 我们画出模型x在0到2区间内的值
    X_new = np.array([[0], [2]])
    # 新增一列常数1的结果
    X_new_b = np.c_[np.ones((2, 1)), X_new]
    # 预测的端点值
    y_predict = X_new_b.dot(theta)

    # 画出模型拟合的结果
    plt.plot(X_new, y_predict, "r-")
    # 画出原来的样本
    plt.scatter(X, y)
    plt.show()


# 生成 100 个 0 ~ 2 的随机浮点数
X = 2 * np.random.rand(100, 1)

# 设置 a=3, b=4, 加上 0~1 的随机误差来模拟真实情况
y = 4 + 3 * X + np.random.randn(100, 1)

# 假设不知道 a 和 b，在仅有 X 和 y 的情况下，使用均方差法计算 a 和 b 的值
theta = gradient_get_theta(X, y)

# 每次得到的结果各不相同，b 在 4 左右，a 在 3 左右，与实际情况接近
# print(theta)

show_graph(X, y, theta)