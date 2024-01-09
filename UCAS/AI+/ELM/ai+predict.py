#!/usr/bin/python
# -*- coding: utf-8 -*-
import time
import os
import pickle
import numpy as np
import data_utils as dus
from elm import GenELMClassifier
from random_layer import MLPRandomLayer


def pred_save(model, col_clip, in_file, out_file):
    data = np.loadtxt(in_file, dtype=np.float64, delimiter=',', unpack=False)
    X = data[:, 1:]
    X = np.delete(X, col_clip, 1)

    # normalization
    X = dus.normalize(X)
    y = model.predict(X)

    with open(out_file, 'w') as fo:
        fo.write("id,label\n")
        for r in range(len(y)):
            fo.write("{},{}\n".format(r + 1, np.round(y[r], 2)))

        fo.close()


ps_thresh = 0.01  # pearson rate & spearman rate threshold
ol_percent = 0.1  # outlier percentage: we predict there were 10% noise data randomly mixed in the train data
act_func = 'sigmoid'
auc_train = 50000
hn = 10000  # 100000 will be better
save_model = True
load_model = False
do_predict = False

data_path = '../newdata'
save_path = '../result'
data = np.loadtxt(os.path.join(data_path, 'dataTrain_test.csv'), dtype=np.float64, delimiter=',', unpack=False)

model_file = os.path.join(save_path, 'model_{}.sav'.format(hn))

s_time = time.time()
if load_model:
    if not os.path.exists(model_file):
        print('Error! Model file {} not found.'.format(model_file))
        exit(-1)
    with open(model_file, 'rb') as fi:
        model_loaded = pickle.load(fi)

        params = model_loaded['params']
        idx_clip = params['clip']
        auc_train = params['auct']
        idx_outliers = params['idol']

        if auc_train < 0:
            auc_train = len(data)
        X = data[:auc_train, 1:-1]
        y = data[:auc_train, -1]
        # normalization
        X = dus.normalize(X)
        X_clip = np.delete(X, idx_clip, 1)
        X_dense = np.delete(X_clip[:auc_train, :], idx_outliers, 0)
        y_dense = np.delete(y[:auc_train], idx_outliers, 0)

        clf = model_loaded['model']
        print('Model loaded from {}.'.format(model_file))
else:
    if auc_train < 0:
        auc_train = len(data)
    X = data[:auc_train, 1:-1]
    y = data[:auc_train, -1]
    # normalization
    X = dus.normalize(X)
    idx_clip = []
    # idx_clip = dus.clip_list(X, y, ps_thresh)
    # X_clip = np.delete(X, idx_clip, 1)
    X_dense = X
    y_dense = y
    idx_outliers = []

    # idx_outliers = dus.idx_outlier(X_clip[:auc_train, :], ol_percent, idx_clip)
    # X_dense = np.delete(X_clip[:auc_train, :], idx_outliers, 0)
    # y_dense = np.delete(y[:auc_train], idx_outliers, 0)

    sig_rl = MLPRandomLayer(n_hidden=hn, activation_func=act_func)
    clf = GenELMClassifier(hidden_layer=sig_rl)
    print('Start training with {} hidden nodes...'.format(hn))
    clf.fit(X_dense, y_dense)

score = np.round(clf.score(X_dense, y_dense)*100, 2)
c_time = np.round(time.time() - s_time, 2)
print("func: {}, hn: {}, score: {}, time: {}".format('sigmoid', hn, score, c_time))

if (not load_model) and save_model:
    params = {
        'ps': ps_thresh,
        'ol': ol_percent,
        'f': act_func,
        'hn': hn,
        'clip': idx_clip,
        'idol': idx_outliers,
        'auct': auc_train
    }
    with open(model_file, 'wb') as fo:
        pickle.dump({'model': clf, 'params': params}, fo)
    print('Saved model into {}...'.format(model_file))

if do_predict:
    '''
    print('Predicting data A...')
    result_file_A = os.path.join(save_path, 'predictA_{}.csv'.format(hn))
    pred_save(clf, idx_clip, os.path.join(data_path, 'dataA_test.csv'), result_file_A)
    print('Predict result of data A saved in {}.'.format(result_file_A))
    '''

    print('Predicting data B...')
    result_file_B = os.path.join(save_path, 'predictB_{}.csv'.format(hn))
    pred_save(clf, idx_clip, os.path.join(data_path, 'dataB_test.csv'), result_file_B)
    print('Predict result of data B saved in {}.'.format(result_file_B))
