# -*- coding: utf-8 -*-
# @Time    : 2018/8/21 10:39
# @Author  : Barry
# @File    : mnist_AB.py
# @Software: PyCharm Community Edition
 
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import accuracy_score
import tensorflow.examples.tutorials.mnist.input_data as input_data
import time
from datetime import datetime
 
data_dir = '../homework/data/'
mnist = input_data.read_data_sets(data_dir,one_hot=False)
batch_size = 50000
batch_x,batch_y = mnist.train.next_batch(batch_size)
test_x = mnist.test.images[:10000]
test_y = mnist.test.labels[:10000]
 
print("start Gradient Boosting")
StartTime = time.clock()
 
for i in range(10,200,10):
    clf_rf = AdaBoostClassifier(n_estimators=i)
    clf_rf.fit(batch_x,batch_y)
 
    y_pred_rf = clf_rf.predict(test_x)
    acc_rf = accuracy_score(test_y,y_pred_rf)
    print("%s n_estimators = %d, random forest accuracy:%f" % (datetime.now(), i, acc_rf))
 
EndTime = time.clock()
print('Total time %.2f s' % (EndTime - StartTime))