import numpy as np
import matplotlib.pyplot as plt

# seaborn 是一个基于 matplotlib 的可视化库。可能 matplotlib 本身太难用了，所以弄了这？
import seaborn as sns
from scipy.stats import norm
sns.set_style('darkgrid')
np.random.seed(123)

data = np.random.randn(20)

# 这个函数由 Metropolis-Hasting 算法的后验方程得到
def normal_posterior(data, x, mu_prior, sigma_prior, sigma=1):
    n = len(data)
    sigma_posterior = (1/sigma_prior**2 + n/sigma)**-1
    mu_posterior = sigma_posterior * (mu_prior/sigma_prior**2 + data.sum()/sigma**2)
    # pdf: Probability density function，概率密度函数
    return norm(mu_posterior, np.sqrt(sigma_posterior)).pdf(x)

if __name__ == '__main__':
    # 揭示在已知先验分布和后验方差的情况下，后验所呈现的分布（即后验 mu 的分布）
    ax = plt.subplot()
    x = np.linspace(-1, 1, 100)
    posterior = normal_posterior(data, x, 0, 1)
    ax.plot(x, posterior, color="skyblue")
    ax.set(xlabel=r'$\mu$', ylabel='Posterior Belief')
    sns.despine()
    plt.show()
