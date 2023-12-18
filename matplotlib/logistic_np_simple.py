import numpy as np
import matplotlib.pyplot as plt
from IPython.core.pylabtools import figsize


def logistic(x, beta, alpha=0):
    return 1.0 / (1.0 + np.exp(np.dot(beta, x) + alpha))


figsize(10, 3)
x = np.linspace(-4, 4, 100)

# 注意这里的实现方式。即随意定义一个函数，然后定义出一个 x ，用线生插值组成一个均匀的自变量组
# 然后调用函数，将结果传给 plt.plot() 方法就能绘图了。

plt.plot(x, logistic(x, 1), label=r"$\beta = 1$", ls="--", lw=1)
plt.plot(x, logistic(x, 3), label=r"$\beta = 3$", ls="--", lw=1)
plt.plot(x, logistic(x, -5), label=r"$\beta = -5$", ls="--", lw=1)

plt.plot(x, logistic(x, 1, 1), label=r"$\beta = 1, \alpha = 1$",
         color="#348ABD")
plt.plot(x, logistic(x, 3, -2), label=r"$\beta = 3, \alpha = -2$",
         color="#A60628")
plt.plot(x, logistic(x, -5, 7), label=r"$\beta = -5, \alpha = 7$",
         color="#7A68A6")

plt.legend(loc="lower left")
plt.title("examples of logistic functions")
plt.show()
