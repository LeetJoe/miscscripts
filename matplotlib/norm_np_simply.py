import scipy.stats as stats
import numpy as np
import matplotlib.pyplot as plt
from IPython.core.pylabtools import figsize


figsize(10, 3)
nor = stats.norm
# 第三个参数表示打点数量，数量越多线越平滑
x = np.linspace(-8, 7, 600)
mu = (-2, 0, 3)
tau = (.7, 1, 2.8)
colors = ["#348ABD", "#A60628", "#7A68A6"]
parameters = zip(mu, tau, colors)

for _mu, _tau, _color in parameters:
    plt.plot(x, nor.pdf(x, _mu, scale=1./_tau),
             label="$\mu = %d,\;\\tau = %.1f$" % (_mu, _tau), color=_color)
    plt.fill_between(x, nor.pdf(x, _mu, scale=1./_tau), color=_color,
                     alpha=.33)

plt.legend(loc="upper right")
plt.xlabel("$x$")
plt.ylabel("density function at $x$")
plt.title("Probability distribution of three different Normal random variables")
plt.show()