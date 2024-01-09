#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import os
import numpy as np
import data_utils as dus
from elm import GenELMClassifier, GenELMRegressor
from random_layer import MLPRandomLayer


def pred_save(model, col_clip, in_file, out_file):
    data = np.loadtxt(in_file, dtype=np.float64, delimiter=',', unpack=False)
    lx = np.delete(data[:, 1:], col_clip, 1)

    # normalization
    lx = dus.normalize(lx)
    y = model.predict(lx)

    with open(out_file, 'w') as fo:
        fo.write("id,label\n")
        for r in range(len(y)):
            fo.write("{},{}\n".format(r + 1, np.round(y[r], 2)))

        fo.close()

data_path = '../newdata'
act_func = 'sigmoid'  # fixed, the best
hn = 6000

sig_rl = MLPRandomLayer(n_hidden=hn, activation_func=act_func)
clf = GenELMRegressor(hidden_layer=sig_rl)

X_train = np.loadtxt(os.path.join(data_path, 'dataTrain.csv'),dtype=np.float64,delimiter=',',unpack=False)
y_train = np.loadtxt(os.path.join(data_path, 'label.csv'),dtype=np.float64,delimiter=',',unpack=False)
X_test = np.loadtxt(os.path.join(data_path, 'dataB.csv'),dtype=np.float64,delimiter=',',unpack=False)



print('Start training with {} hidden nodes...'.format(hn))
s_time = time.time()
clf.fit(X_train, y_train)
score = np.round(clf.score(X_train, y_train) * 100, 2)

y_test = clf.predict(X_test)
print(y_test[:10])
c_time = np.round(time.time() - s_time, 2)



exit()


ps_thresh = 0.01  # pearson rate & spearman rate threshold
ol_percent = 0.1  # outlier percentage: we predict there were 10% noise data randomly mixed in the train data
ol_no_label = False  # use no label data for outliers
ol_nl_type = 0  # how to use no labeled data: 0-full, 1-pre 34000, 2-beyond 34000
auc_train = 50000  # train data filter use auc

do_predict = True

auc_dict = {
    'a0': -1,  # use full train data
    'a1': 50000  # use pre 50000 rows of train data
}

cl_dict = {
    'cl0': 0,  # no clip
    'cl1': 0.01,  # co-relationship > 0.01
    'cl2': 0.05,  # co-relationship > 0.05
    'cl3': 0.1,  # co-relationship > 0.1
}

ol_dict = {
    't0': (False, 0, 0),  # no out
    't1': (False, 0.05, 0),  # train data core after auc&clip, 5% out
    't2': (False, 0.1, 0),  # train data core after auc&clip, 10% out
    'o1': (True, 0.05, 1),  # no label data core in 34000 after clip, 5% out
    'o2': (True, 0.1, 1),  # no label data core in 34000 after clip, 10% out
    'o3': (True, 0.05, 2),  # no label data core beyond 34000 after clip, 5% out
    'o4': (True, 0.1, 2),  # no label data core beyond 34000 after clip, 10% out
    'o5': (True, 0.05, 0),  # no label data core in whole after clip, 5% out
    'o6': (True, 0.1, 0),  # no label data core in whole after clip, 10% out
}


data = np.loadtxt(os.path.join(data_path, 'dataTrain_test.csv'),dtype=np.float64,delimiter=',',unpack=False)

# func: function, h_num: number of hidden nodes, data: data group, d_size: data size, m_aux: aux_mark,
# m_clip: clip type, m_out: outlier type, t_score: score on data, t_cost: time cost, ol_score: online score of B
result = [['func', 'h_num', 'd_size', 'm_aux', 'm_clip', 'm_out', 't_score', 't_cost', 'ol_score']]

for auc_mark in auc_dict:
    auc_train = auc_dict[auc_mark]
    if auc_train < 0:
        auc_train = len(data)

    X = data[:auc_train, 1:-1]
    y = data[:auc_train, -1]

    # normalization
    X = dus.normalize(X)

    # clip
    for cl_mark in cl_dict:
        ps_thresh = cl_dict[cl_mark]
        if ps_thresh == 0:
            idx_clip = []
        else:
            idx_clip = dus.clip_list(X, y, ps_thresh)

        X_clip = np.delete(X, idx_clip, 1)
        # outlier filter
        for ol_mark in ol_dict:
            ol_no_label, ol_percent, ol_nl_type = ol_dict[ol_mark]
            if ol_percent == 0:
                idx_outliers = []
            else:
                idx_outliers = dus.idx_outlier(X_clip, ol_percent, idx_clip, ol_no_label, ol_nl_type)

            X_dense = np.delete(X_clip, idx_outliers, 0)
            y_dense = np.delete(y, idx_outliers, 0)

            # hn_list = [1000, 2000, 4000, 8000, 10000]
            hn_list = [1000, 2000]

            for hn in hn_list:
                sig_rl = MLPRandomLayer(n_hidden=hn, activation_func=act_func)

                clf = GenELMClassifier(hidden_layer=sig_rl)
                print('Start training with {} hidden nodes...'.format(hn))
                s_time = time.time()
                clf.fit(X_dense, y_dense)
                score = np.round(clf.score(X_dense, y_dense)*100, 2)
                c_time = np.round(time.time() - s_time, 2)
                result.append(['sigmoid', hn, len(y), auc_mark, cl_mark, ol_mark, score, c_time, '*'])
                print("func: {}, h_num: {}, d_size: {}, m_aux: {}, m_clip: {}, m_out: {}, t_score: {}, t_cost: {}".format(
                    'sigmoid', hn, len(y), auc_mark, cl_mark, ol_mark, score, c_time))

                # predict on B
                if do_predict:
                    print('Predicting data B...')
                    result_file_B = 'predictB_{}_{}_{}_{}_{}_{}.csv'.format(hn, len(y), auc_mark, cl_mark, ol_mark, score)
                    pred_save(clf, idx_clip, os.path.join(data_path, 'dataB_test.csv'), os.path.join(data_path, result_file_B))
                    print('Predict result of data B saved in {}.'.format(result_file_B))

with open(os.path.join(data_path, 'test_result.csv'), 'w') as fo:
    for r in result:
        fo.write("{},{},{},{},{},{},{},{},{}\n".format(r[0], r[1], r[2], r[3], r[4], r[5], r[6], r[7], r[8]))

    fo.close()
