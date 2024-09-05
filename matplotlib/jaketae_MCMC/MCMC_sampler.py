import numpy as np
import matplotlib.pyplot as plt

# seaborn 是一个基于 matplotlib 的可视化库。可能 matplotlib 本身太难用了，所以弄了这？
import seaborn as sns
from scipy.stats import norm

from posterior_norm import normal_posterior


# 这只是一个简单的示例，在已知正态分布的先验以及正态分布的似然和方差的前提下，计算后验。
def sampler(data, iter_num, mu_init=.5, proposal_width=.5, mu_prior_mu=0, mu_prior_sd=1, sigma=1):
    '''

    :param data: 初始样本
    :param iter_num: 采样次数
    :param mu_init: 初始的 mu，即用来逼近后验 mu 的初始假定
    :param proposal_width: 对于当前迭代到的临时后验 mu_current，要产生新的临时后验 mu_proposal，使用这个 proposal_width 作为方差限定新后验的“生成范围”
    :param mu_prior_mu: 固定值，即先验分布使用的 mu
    :param mu_prior_sd: 固定值，即先验分布使用的方差
    :param sigma: 固定值，已知的后验方差
    :return:
    '''
    mu_current = mu_init
    posterior = [mu_current]
    for i in range(iter_num):
        # rvs() 函数用于从指定的分布中生成随机样本，这里是生成“一个”候选的 mu
        mu_proposal = norm(mu_current, proposal_width).rvs()
        # 当前（旧的）似然。
        # pdf(data) 表示正态分布函数为norm(mu_current, sigma)时对 data 中的每一个值应用此函数得到的结果，最终得到一个 list。
        likelihood_current = np.prod(norm(mu_current, sigma).pdf(data))
        # 根据新的 mu 计算的新的似然
        likelihood_proposal = np.prod(norm(mu_proposal, sigma).pdf(data))
        # 先验分布在 mu_current 处的值，即 mu_current 的先验
        prior_current = norm(mu_prior_mu, mu_prior_sd).pdf(mu_current)
        # mu_proposal 的先验
        prior_proposal = norm(mu_prior_mu, mu_prior_sd).pdf(mu_proposal)
        # 使用 mu_current 得到的后验
        p_current = likelihood_current * prior_current
        # 使用 mu_proposal 得到的后验
        p_proposal = likelihood_proposal * prior_proposal
        # 两个后验对比，np.random.rand() 就是公式里的 \alpha，它不是一个固定值，而是一个 [0,1] 的均匀分布上的采样
        accept = p_proposal/p_current > np.random.rand() # Compare with random number sampled from [0, 1]
        if accept:
            mu_current = mu_proposal
        posterior.append(mu_current)

    # 最后返回的是在对所有采样评估后，jump or not jump 判定后选择的 mu 形成的一个序列，包含最初的 mu_init
    return np.array(posterior)


def test_sampler_0(data):
    # 揭示采样器的工作方式，通过不断修正后验的 mu，可以得到一个 mu 估计的序列，
    result = sampler(data, 5)
    print(result)

    # result 中的 mu 序列的均值收敛于真实的后验 mu
    print(np.mean(result))


def test_sampler_1(data):
    # 增加采样次数到 15000 次，查看结果的变化情况，这样的图称为“trace plot”
    posterior = sampler(data, 15000, mu_init=1)
    fig, ax = plt.subplots()
    ax.plot(posterior, color="skyblue", label='Proposal Width = 0.5')
    _ = ax.set(xlabel='Samples', ylabel=r'$\mu$')

    plt.show()

    print(np.mean(posterior))


def test_sampler_2(data):
    # 这一段揭示的是当 proposal_width 取一个较小的值时，trace plot 的变化。前一个示例中，proposal_width=0.5，这里取值 0.01
    posterior_small = sampler(data, 15000, mu_init=1, proposal_width=.01)
    fig, ax = plt.subplots()
    ax.plot(posterior_small, color='skyblue', label='Proposal Width = 0.01')
    _ = ax.set(xlabel='Samples', ylabel=r'$\mu$')
    plt.legend()

    # 从结果来看，前面那个示例的结果曲线跳跃非常大，几乎难以形成一条线；而这里的示例曲线波动相对较小，更明显的显示出局部的某种走势。
    # 这说明如果这个 proposal_width 取值太小，随机性不够强，会导致采样结果收敛得慢一些。
    plt.show()


# 用来验证通过数学分析得到的后验分布与通过采样法得到的样本分布是否一致
def test_posterior_dist():
    ax = plt.subplot()
    posterior = sampler(data, 15000, mu_init=1)

    # 这里的 posterior 可以不用取全部，可以只取其中的某一段，如[2000:]，取的越多与理论分布越接近
    sns.distplot(posterior, ax=ax, label='Estimated Posterior', color='skyblue')
    x = np.linspace(-1, 1, 500)
    posterior_dist = normal_posterior(data, x, 0, 1)
    ax.plot(x, posterior_dist, color='silver', alpha=0.7, label='Analytic Posterior')
    ax.set(xlabel=r'$\mu$', ylabel='Posterior Belief')
    ax.legend()

    # 灰色曲线是数学分析得到的理论后验分布，蓝线是通过采样结果得到的分布，两者基本吻合。
    plt.show()

if __name__ == '__main__':
    sns.set_style('darkgrid')
    np.random.seed(123) # 随机种子固定，得到的随机序列也会固定，得到的结果总是相同的

    data = np.random.randn(20)

    # test_sampler_0(data)

    # test_sampler_1(data)

    # test_sampler_2(data)

    test_posterior_dist()
