import pymc3 as pm  # pymc3 已经过时了，现在的 pymc3 改名叫 PyMC 了。
import numpy as np
import time
import matplotlib.pyplot as plt
from MCMC_sampler import sampler
import seaborn as sns


# 手搓实现的 MCMC sampler 结果
data = np.random.randn(20)

start_time = time.time()
posterior = sampler(data, 15000, mu_init=1)
end_time = time.time()
print('Manual cost: {}s'.format(end_time - start_time))

start_time = time.time()
# 使用 PyMC3 实现的 MCMC
with pm.Model():
    mu = pm.Normal('mu', 0, 1)
    sigma = 1.
    returns = pm.Normal('returns', mu=mu, sd=sigma, observed=data)
    step = pm.Metropolis()
    trace = pm.sample(15000, step)
end_time = time.time()

# PyMC 要略快一些
print('PyMC3 cost: {}s'.format(end_time - start_time))

sns.distplot(trace[2000:]['mu'], label='PyMC3', color='silver')
sns.distplot(posterior[2000:], label='Manual', color='skyblue')
plt.xlabel(r'$\mu$');
plt.ylabel('Posterior Belief')
plt.legend()
plt.show()
