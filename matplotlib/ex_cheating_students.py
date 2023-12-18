import pymc3 as pm
import scipy.stats as stats
import numpy as np
import matplotlib.pyplot as plt
from IPython.core.pylabtools import figsize
import theano.tensor as tt


def with_p():
    N = 100
    with pm.Model() as model:
        # 这个是作弊的概率，不是说谎的概率！还没有考虑说谎。
        p = pm.Uniform("freq_cheating", 0, 1)

        # 也就是说，PyMC 并没有单独定义 Binomial 分布，而是通过指定参数 shape 通过 Bernoulli 分布来实现的 Binomial 分布
        # 这里使用的参数名为 testval, 不是 observed，应该是会有一些差别的。(差别是什么呢？)
        true_answers = pm.Bernoulli("truths", p, shape=N, testval=np.random.binomial(1, 0.5, N))
        # 前面用的是 stats 的binomial, 这里又用的是 numpy 的 binomial。这里的 testval 和 p 似乎还没有发生关联
        # binomail 分布里，第一个数字表示取值范围，这里是 [0,1]; 0.5 是 p; N 是采样次数。此分布的期望为 1x0.5=0.5，这是为了准确地模拟 Bernoulli 分布；
        # 实际上第一个参数可以取任意整数，第二个参数也可以取任意 p。(唉，当初没学好。)

        first_coin_flips = pm.Bernoulli("first_flips", 0.5, shape=N, testval=np.random.binomial(1, 0.5, N))

    # print(first_coin_flips.tag.test_value)

        second_coin_flips = pm.Bernoulli("second_flips", 0.5, shape=N, testval=np.random.binomial(1, 0.5, N))

    with model:
        # 通过这里计算出来的。第一次抛硬币得到正面且诚实(地回答了“作弊了”？)的人 + 第一次抛硬币得到反面且第二次抛硬币得到正面的人(必须回答“作弊了”)的人
        val = first_coin_flips*true_answers + (1 - first_coin_flips)*second_coin_flips
        observed_proportion = pm.Deterministic("observed_proportion", tt.sum(val)/float(N)) # 观察到的回答了“作弊了”的人数占比

    X = 35

    with model:
        # 又构造了一个二项分布，observed_proportion 作为 p，observed=X，X是一个整数？也就是说把最后观察到的数字看作一个随机变量，构造的二项分布？
        observations = pm.Binomial("obs", N, observed_proportion, observed=X)

    # To be explained in Chapter 3!
    with model:
        step = pm.Metropolis(vars=[p]) # p 是最初设定的作弊比例的先验分布。但是这个传参该怎么理解？
        trace = pm.sample(40000, step=step)
        burned_trace = trace[15000:]  # 这里为什么要取 15000 之后的数据，应该是 25000 个条目
        # Sampling 2 chains for 1_000 tune and 40_000 draw iterations (2_000 + 80_000 draws total)
        # 1000 tune 应该是个固定值；40000 是单轮(single iteration)采样量。
        # 最后得到的 trace 很奇怪，以上面的采样方式为例，len(trace)=40000，len(trace['first_flips'])=80000，len(trace['first_flips'][1000])=100
        # 这个 40000 和 80000 是怎么计算的？
        # 还有这个burned_trace ，len(burned_trace)=25000，len(burned_trace['first_flips'])=50000，len(burned_trace['first_flips'][1000])=100
        # 第一层按指定数量减，第二层按指定数量 x num_iterations 减，第三层不变为N。

    figsize(12.5, 3)
    # 其实就是 p，定义在模型里的名字叫 freq_cheating
    p_trace = burned_trace["freq_cheating"][15000:] # 这里取的是 15000 之后的数据？前15000是什么东西？
    plt.hist(p_trace, histtype="stepfilled", density=True, alpha=0.85, bins=100,
             label="posterior distribution", color="#348ABD")
    # 三个参数的情况下，第一个 [.05, .35] 表示位置，[0, 0] 表示竖线起点，[5, 5] 表示竖线终点
    plt.vlines([.05, .35], [0, 0], [5, 5], alpha=0.3)
    plt.xlim(0, 1)
    plt.legend()
    plt.show()


def with_p_skewed():
    with pm.Model() as model:
        p = pm.Uniform("freq_cheating", 0, 1)
        # 对 p 进行进一步分析
        p_skewed = pm.Deterministic("p_skewed", 0.5*p + 0.25)

    with model:
        # 用在这一步里，而不是最开始的 true_answers 那个步骤中
        yes_responses = pm.Binomial("number_cheaters", 100, p_skewed, observed=35)

    with model:
        # To Be Explained in Chapter 3!
        step = pm.Metropolis()
        trace = pm.sample(25000, step=step)
        burned_trace = trace[2500:]

    figsize(12.5, 3)
    p_trace = burned_trace["freq_cheating"]
    plt.hist(p_trace, histtype="stepfilled", density=True, alpha=0.85, bins=80,
             label="posterior distribution", color="#348ABD")
    plt.vlines([.05, .35], [0, 0], [5, 5], alpha=0.2)
    plt.xlim(0, 1)
    plt.legend()
    plt.show()


# p not skewed
# with_p()

# p skewed
with_p_skewed()
