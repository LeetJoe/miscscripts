import os
import numpy as np
import pandas as pd
from sklearn.experimental import enable_hist_gradient_boosting
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LogisticRegression
from xgboost import XGBClassifier
from lightgbm import LGBMClassifier
from catboost import CatBoostClassifier
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.ensemble import HistGradientBoostingClassifier
from sklearn.ensemble import StackingClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import roc_auc_score
from sklearn.model_selection import train_test_split
import warnings
from tqdm import tqdm
warnings.filterwarnings('ignore')

def model_train(model, model_name, kfold=5):
    oof_preds = np.zeros((train.shape[0]))
    test_preds = np.zeros(test.shape[0])
    skf = StratifiedKFold(n_splits=kfold)
    print(f"Model = {model_name}")
    for k, (train_index, test_index) in enumerate(skf.split(train, label)):
        x_train, x_test = train.iloc[train_index, :], train.iloc[test_index, :]
        y_train, y_test = label.iloc[train_index], label.iloc[test_index]

        model.fit(x_train,y_train)

        y_pred = model.predict_proba(x_test)[:,1]
        oof_preds[test_index] = y_pred.ravel()
        auc = roc_auc_score(y_test,y_pred)
        print("- KFold = %d, val_auc = %.4f" % (k, auc))
        test_fold_preds = model.predict_proba(test)[:, 1]
        test_preds += test_fold_preds.ravel()
    print("Overall Model = %s, AUC = %.4f" % (model_name, roc_auc_score(label, oof_preds)))
    return test_preds / kfold

gbc = GradientBoostingClassifier(
    n_estimators=50,
    learning_rate=0.1,
    max_depth=5
)
hgbc = HistGradientBoostingClassifier(
    max_iter=100,
    max_depth=5
)
xgbc = XGBClassifier(
    objective='binary:logistic',
    eval_metric='auc',
    n_estimators=100,
    max_depth=6,
    learning_rate=0.1
)
gbm = LGBMClassifier(
    objective='binary',
    boosting_type='gbdt',
    num_leaves=2 ** 6,
    max_depth=8,
    colsample_bytree=0.8,
    subsample_freq=1,
    max_bin=255,
    learning_rate=0.05,
    n_estimators=100,
    metrics='auc'
)
cbc = CatBoostClassifier(
    iterations=210,
    depth=6,
    learning_rate=0.03,
    l2_leaf_reg=1,
    loss_function='Logloss',
    verbose=0
)
LG = LogisticRegression(C = 0.1, penalty = 'l1',solver='liblinear')
estimators = [
    ('gbc', gbc),
    ('hgbc', hgbc),
    ('xgbc', xgbc),
    ('gbm', gbm),
    ('cbc', cbc),
    ('LG', LG)
]
clf = StackingClassifier(
    estimators=estimators,
    final_estimator=LogisticRegression()
)

data_path = 'newdata'
result_path = 'result'
train = pd.read_csv(os.path.join(data_path, 'dataTrain.csv'))
test = pd.read_csv(os.path.join(data_path, 'dataB.csv'))
label = pd.read_csv(os.path.join(data_path, 'label.csv'))
submission = pd.read_csv(os.path.join(result_path, 'submission.csv'))

feature_columns = [ col for col in train.columns ]

X_train, X_test, y_train, y_test = train_test_split(
    train, label, stratify=label, random_state=2023)
clf.fit(X_train, y_train)
y_pred = clf.predict_proba(X_test)[:, 1]
auc = roc_auc_score(y_test, y_pred)
print('auc = %.8f' % auc)
ff = []
for col in feature_columns:
    x_test = X_test.copy()
    x_test[col] = 0
    auc1 = roc_auc_score(y_test, clf.predict_proba(x_test)[:, 1])
    if auc1 < auc:
        ff.append(col)
    print('%5s | %.8f | %.8f' % (col, auc1, auc1 - auc))
clf.fit(X_train[ff], y_train)
y_pred = clf.predict_proba(X_test[ff])[:, 1]
auc = roc_auc_score(y_test, y_pred)
print('auc = %.8f' % auc)
train = train[ff]
test = test[ff]

clf_test_preds = model_train(clf, "StackingClassifier", 10)

submission['label'] = clf_test_preds
submission.to_csv(os.path.join(result_path, 'submission.csv'), index=False)
