import numpy as np
from sklearn import metrics
# 样本数量为N
N = 10000
# 生成80%简单负样本，20%平衡的正负样本
a = [0,0,0,0,0,0,0,0,1,-1]
d = np.random.choice(a, size=N, replace=True, p=None)
label = np.zeros(d.size)
label[d>0] = 1

rand_preds, good_preds, better_preds = [], [], []
for i in d:
    rand = abs(i)*np.random.uniform(0,1)
    rand_preds.append(rand)  # 对简单负样本分类正确,对其余随机预测
    good_preds.append(rand+i*0.1)  # 对简单负样本分类正确,对其余增加预测度
    better_preds.append(rand+i*0.3)
rand_auc = metrics.roc_auc_score(label,rand_preds)
good_auc = metrics.roc_auc_score(label,good_preds)
better_auc = metrics.roc_auc_score(label,better_preds)
print(rand_auc, good_auc, better_auc)