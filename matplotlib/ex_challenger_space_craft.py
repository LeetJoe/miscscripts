
import numpy as np
import matplotlib.pyplot as plt
from IPython.core.pylabtools import figsize
import theano.tensor as tt # todo 这句会报错，网上有类似问题但是没有解决方案
import pymc3 as pm
from scipy.stats.mstats import mquantiles


def logistic(x, beta, alpha=0):
    return 1.0 / (1.0 + np.exp(np.dot(beta, x) + alpha))


def show_rings_temperature(challenger_data):
    figsize(12.5, 3.5)
    np.set_printoptions(precision=3, suppress=True)

    #drop the NA values
    challenger_data = challenger_data[~np.isnan(challenger_data[:, 1])]

    #plot it, as a function of tempature (the first column)
    # print("Temp (F), O-Ring failure?")
    # print(challenger_data)

    plt.scatter(challenger_data[:, 0], challenger_data[:, 1], s=75, color="k",
                alpha=0.5)
    plt.yticks([0, 1])
    plt.ylabel("Damage Incident?")
    plt.xlabel("Outside temperature (Fahrenheit)")
    plt.title("Defects of the Space Shuttle O-Rings vs temperature")


def show_alpha_beta(beta_samples, alpha_samples):
    figsize(12.5, 6)

    # histogram of the samples:
    plt.subplot(211)
    plt.title(r"Posterior distributions of the variables $\alpha, \beta$")
    plt.hist(beta_samples, histtype='stepfilled', bins=70, alpha=0.85,
             label=r"posterior of $\beta$", color="#7A68A6", density=True)
    plt.legend()

    plt.subplot(212)
    plt.hist(alpha_samples, histtype='stepfilled', bins=70, alpha=0.85,
             label=r"posterior of $\alpha$", color="#A60628", density=True)
    plt.legend()
    plt.show()


def show_posterior(t, p_t, mean_prob_t, temperature, D):
    figsize(12.5, 4)

    plt.plot(t, mean_prob_t, lw=3, label="average posterior \nprobability of defect")
    # 随便从采样中取两条线，有 20000 条可取。这里取的第 1 条和倒数第 2 条
    plt.plot(t, p_t[0, :], ls="--", label="realization from posterior")
    plt.plot(t, p_t[-2, :], ls="--", label="realization from posterior")

    # 打点原始数据
    plt.scatter(temperature, D, color="k", s=50, alpha=0.5)

    plt.title("Posterior expected value of probability of defect; plus realizations")
    plt.legend(loc="lower left")
    plt.ylim(-0.1, 1.1)
    plt.xlim(t.min(), t.max())
    plt.ylabel("probability")
    plt.xlabel("temperature")
    plt.show()


def show_prob_range_by_temp(p_t, t, mean_prob_t, temperature, D):
    # vectorized bottom and top 2.5% quantiles for "confidence interval"
    # 取 p_t 的 [0.025, 0.975] 共 95% 的数据。即舍弃极端值
    qs = mquantiles(p_t, [0.025, 0.975], axis=0)

    # *qs ?? 这TM是什么写法？指针？
    # 这个是画了一个条带，*qs 应该是一维参数展开，意味着一维子元素作为参数在此位置罗列
    plt.fill_between(t[:, 0], *qs, alpha=0.7, color="#7A68A6")

    # 这条是 “下限”
    plt.plot(t[:, 0], qs[0], label="95% CI", color="#7A68A6", alpha=0.7)

    # 这条是均值，跟上面的图是一样的
    plt.plot(t, mean_prob_t, lw=1, ls="--", color="k", label="average posterior \nprobability of defect")

    plt.xlim(t.min(), t.max())
    plt.ylim(-0.02, 1.02)
    plt.legend(loc="lower left")
    plt.scatter(temperature, D, color="k", s=50, alpha=0.5)
    plt.xlabel("temp, $t$")

    plt.ylabel("probability estimate")
    plt.title("Posterior probability estimates given temp. $t$")
    plt.show()


def single_temp_prob(beta_samples, alpha_samples, temp=31):
    figsize(12.5, 2.5)

    # 只取一个点，返回的结果是单点的可能性列表，所以下图的 x 轴不再用温度而是直接用概率
    prob_single = logistic(temp, beta_samples, alpha_samples)

    # plt.xlim(0.995, 1)
    plt.hist(prob_single, bins=2000, density=True, histtype='stepfilled')
    plt.title("Posterior distribution of probability of defect, given $t = " + str(temp) + "$")
    plt.xlabel("probability of defect occurring in O-ring")
    plt.show()


challenger_data = np.genfromtxt("data/challenger_data.csv", skip_header=1,
                                usecols=[1, 2], missing_values="NA",
                                delimiter=",")

# 查看数据基本情况
show_rings_temperature(challenger_data)

temperature = challenger_data[:, 0]  # 取第一列，温度
D = challenger_data[:, 1]  # defect or not?

# notice the`value` here. We explain why below.
with pm.Model() as model:
    # pymc 定义正态分布的方式，使用 mu 和 tau 指定参数
    beta = pm.Normal("beta", mu=0, tau=0.001, testval=0)
    alpha = pm.Normal("alpha", mu=0, tau=0.001, testval=0)
    # p 是 logistic 函数，即目标函数，而 alpha 和 beta 是参数，这两个参数用正态分布来估计
    p = pm.Deterministic("p", 1.0 / (1. + tt.exp(beta * temperature + alpha)))

# connect the probabilities in `p` with our observations through a Bernoulli random variable.
with model:
    # p 的定义使用了 temperature，在这里和 D 关联了起来
    observed = pm.Bernoulli("bernoulli_obs", p, observed=D)

    # Mysterious code to be explained in Chapter 3
    start = pm.find_MAP()  # 最大后验估计？
    step = pm.Metropolis()
    trace = pm.sample(120000, step=step, start=start)
    # 这个是从样本里每 2 个取一个。看来这个 trace 里的东西随便取？
    burned_trace = trace[100000::2]

alpha_samples = burned_trace["alpha"][:, None]  # best to make them 1d，意思是将它们降为 1 维？
beta_samples = burned_trace["beta"][:, None]

# 查看 alpha 和 beta 的采样结果
show_alpha_beta(beta_samples, alpha_samples)

t = np.linspace(temperature.min() - 5, temperature.max() + 5, 50)[:, None]
# t.T 表示对 t 进行转置，t 是列向量
# 打点画线，t.T 作为自变量，beta_samples 和 alpha_samples 各有 20000 组，得到的 p_t 也是有 20000 组，可以画 20000 条线
p_t = logistic(t.T, beta_samples, alpha_samples)

mean_prob_t = p_t.mean(axis=0)

# 查看 p 的后验分布
show_posterior(t, p_t, mean_prob_t, temperature, D)

# 查看在温度坐标下的概率范围
show_prob_range_by_temp(p_t, t, mean_prob_t, temperature, D)

#
single_temp_prob(beta_samples, alpha_samples, 65)
