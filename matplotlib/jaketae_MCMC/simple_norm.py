import numpy as np
import matplotlib.pyplot as plt

# seaborn 是一个基于 matplotlib 的可视化库。可能 matplotlib 本身太难用了，所以弄了这？
import seaborn as sns
from scipy.stats import norm
sns.set_style('darkgrid')
np.random.seed(123)

data = np.random.randn(20)

print(data)

ax = plt.subplot()

# distplot 是一个过时的方法，这里只用来演示 MCMC 原理，忽略这些小问题。
# displot 应该类似直方图，对给定的数字列表，统计在每个整数区间内数字的个数。
# 下面这句的作用就是以 1 为粒度统计 data 里的数据落在各区间里的数字的数量。
sns.distplot(data, kde=False, ax=ax, color="skyblue")
_ = ax.set(xlabel='x', ylabel='Count')

plt.show()
