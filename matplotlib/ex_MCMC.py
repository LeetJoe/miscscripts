import scipy.stats as stats
from IPython.core.pylabtools import figsize
import numpy as np
figsize(12.5, 4)

import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# jet is matplotlib.colors.LinearSegmentedColormap
# jet 是一个“线性分段颜色映射”？
jet = plt.cm.jet
fig = plt.figure()
# 0 到 5 线性插值 100 个
x = y = np.linspace(0, 5, 100)
# 使用 x, y 构建一个“网格”？

# X 每一行都是均匀线性插值，每一列都是同一个值
# Y 每一列都是均匀线性插值，每一行都是同一个值
X, Y = np.meshgrid(x, y)


def show_data():
    plt.subplot(121)
    uni_x = stats.uniform.pdf(x, loc=0, scale=5)
    uni_y = stats.uniform.pdf(y, loc=0, scale=5)
    # uni_x 是均匀分布，但每个值是 0.2? 100 值，总和为 20?
    M = np.dot(uni_x[:, None], uni_y[None, :])
    # M 是 100 个 0.04, 打个 100 个均匀的点
    # imshow(): 以图片的形式显示图。 extent=(l,r,b,t)，表示绘图范围，左右 0 到 5，上下 0 到 5.
    im = plt.imshow(M, interpolation='none', origin='lower',
                    cmap=jet, vmax=1, vmin=-.15, extent=(0, 5, 0, 5))

    plt.xlim(0, 5)
    plt.ylim(0, 5)
    plt.title("Landscape formed by Uniform priors.")

    #
    ax = fig.add_subplot(122, projection='3d')
    ax.plot_surface(X, Y, M, cmap=plt.cm.jet, vmax=1, vmin=-.15)
    ax.view_init(azim=390)
    plt.title("Uniform prior landscape; alternate view");
    plt.show()

    return


def show_grad():
    figsize(12.5, 5)
    fig = plt.figure()
    plt.subplot(121)

    exp_x = stats.expon.pdf(x, scale=3)
    exp_y = stats.expon.pdf(x, scale=10)
    # M 是一个二维的点集，应该就是 exp_x 与 exp_y 的联合分布
    M = np.dot(exp_x[:, None], exp_y[None, :])
    # CS matplotlib.contour.QuadContourSet, 二次等高线集合，即第一幅图里的等高线
    CS = plt.contour(X, Y, M)
    im = plt.imshow(M, interpolation='none', origin='lower',
                    cmap=jet, extent=(0, 5, 0, 5))
    # plt.xlabel("prior on $p_1$")
    # plt.ylabel("prior on $p_2$")
    plt.title("$Exp(3), Exp(10)$ prior landscape")

    # 3D 图
    ax = fig.add_subplot(122, projection='3d')
    # 这里的 X, Y 是直接用的上面那段代码里的定义
    ax.plot_surface(X, Y, M, cmap=jet)
    ax.view_init(azim=390)
    plt.title("$Exp(3), Exp(10)$ prior landscape; \nalternate view")
    plt.show()


def test_sample():
    # create the observed data

    # sample size of data we observe, trying varying this (keep it less than 100 ;)
    # 当增大 N 时，分布的高峰会不断向 (3,1) 点逼近，即下面的 lambda_1,2 的值
    N = 6

    # the true parameters, but of course we do not see these values...
    lambda_1_true = 1
    lambda_2_true = 3

    # ...we see the data generated, dependent on the above two values.
    data = np.concatenate([
        stats.poisson.rvs(lambda_1_true, size=(N, 1)),
        stats.poisson.rvs(lambda_2_true, size=(N, 1))
    ], axis=1)
    print("observed (2-dimensional,sample size = %d):" % N, data)

    # plotting details.
    x = y = np.linspace(.01, 5, 100)
    likelihood_x = np.array([stats.poisson.pmf(data[:, 0], _x)
                             for _x in x]).prod(axis=1)
    likelihood_y = np.array([stats.poisson.pmf(data[:, 1], _y)
                             for _y in y]).prod(axis=1)
    L = np.dot(likelihood_x[:, None], likelihood_y[None, :])

    figsize(12.5, 12)
    # matplotlib heavy lifting below, beware!
    plt.subplot(221)
    uni_x = stats.uniform.pdf(x, loc=0, scale=5)
    uni_y = stats.uniform.pdf(x, loc=0, scale=5)
    M = np.dot(uni_x[:, None], uni_y[None, :])
    im = plt.imshow(M, interpolation='none', origin='lower',
                    cmap=jet, vmax=1, vmin=-.15, extent=(0, 5, 0, 5))
    plt.scatter(lambda_2_true, lambda_1_true, c="k", s=50, edgecolor="none")
    plt.xlim(0, 5)
    plt.ylim(0, 5)
    plt.title("Landscape formed by Uniform priors on $p_1, p_2$.")

    plt.subplot(223)
    plt.contour(x, y, M * L)
    im = plt.imshow(M * L, interpolation='none', origin='lower',
                    cmap=jet, extent=(0, 5, 0, 5))
    plt.title("Landscape warped by %d data observation;\n Uniform priors on $p_1, p_2$." % N)
    plt.scatter(lambda_2_true, lambda_1_true, c="k", s=50, edgecolor="none")
    plt.xlim(0, 5)
    plt.ylim(0, 5)

    plt.subplot(222)
    exp_x = stats.expon.pdf(x, loc=0, scale=3)
    exp_y = stats.expon.pdf(x, loc=0, scale=10)
    M = np.dot(exp_x[:, None], exp_y[None, :])

    plt.contour(x, y, M)
    im = plt.imshow(M, interpolation='none', origin='lower',
                    cmap=jet, extent=(0, 5, 0, 5))
    plt.scatter(lambda_2_true, lambda_1_true, c="k", s=50, edgecolor="none")
    plt.xlim(0, 5)
    plt.ylim(0, 5)
    plt.title("Landscape formed by Exponential priors on $p_1, p_2$.")

    plt.subplot(224)
    # This is the likelihood times prior, that results in the posterior.
    plt.contour(x, y, M * L)
    im = plt.imshow(M * L, interpolation='none', origin='lower',
                    cmap=jet, extent=(0, 5, 0, 5))

    plt.scatter(lambda_2_true, lambda_1_true, c="k", s=50, edgecolor="none")
    plt.title("Landscape warped by %d data observation;\n Exponential priors on \
    $p_1, p_2$." % N)
    plt.xlim(0, 5)
    plt.ylim(0, 5)

    plt.show()

    return


test_sample()

