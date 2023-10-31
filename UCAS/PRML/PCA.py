# 什么狗屁！
#导入必要的工具包
import pandas as pd
import numpy as np
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.decomposition import PCA
import time
from scipy.io import loadmat
train = pd.read_csv('./data/MNIST_train.csv').values
test = pd.read_csv('./data/MNIST_test.csv').values#train

pca = PCA(n_components=n)
print ("PCA begin with n_components: {}".format(n))
pca.fit(X_train)
# 在训练集和测试集降维
X_train_pca = pca.transform(X_train)
x_val_pca = pca.transform(X_val)

# 利用svc训练
print('svc begin' )
#kernel : 核函数，默认是rbf，可以是“linear', 'poly', 'rbf', 'sigmoid', 'precomputed'
clf1 = svm.SVC(kernel='linear')
clf1.fit(X_train_pca, y_train)

# 返回accuracy
accuracy = clf1.score(X_val_pca， y_val)
end = time.time()
print("accuracy: {}, time elaps:{}".format (accuracy,int(end-start)))
return accuracy