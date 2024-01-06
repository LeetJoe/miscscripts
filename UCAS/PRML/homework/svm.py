import joblib

import sklearn.datasets as sk_datasets
import sklearn.datasets._samples_generator as sk_sample_generator
import sklearn.model_selection as sk_model_selection
import sklearn.preprocessing as sk_preprocessing

from sklearn import svm
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score


digitals = sk_datasets.load_digits()
digitals_X = digitals.data
digitals_y = digitals.target

X, y = sk_sample_generator.make_classification(n_samples=6,n_features=5,n_informative=2,n_redundant=3,n_classes=2,n_clusters_per_class=2,scale=1,random_state=20)
X_train, X_test, y_train, y_test = sk_model_selection.train_test_split(digitals_X, digitals_y, train_size=0.8, random_state=20)

scaler = sk_preprocessing.StandardScaler().fit(X)
new_X = scaler.transform(X)  # 基于mean和std的标准化
 
scaler = sk_preprocessing.MinMaxScaler(feature_range=(0,1)).fit(X)
new_X=scaler.transform(X)  # scale into [0, 1]

new_X = sk_preprocessing.normalize(X,norm='l2')  # L2 normalization

parameters = {'kernel': ('linear', 'rbf'), 'C': [1, 10]}
svc = svm.SVC()
model = GridSearchCV(svc, parameters)
model.fit(digitals.data, digitals.target)

scores = cross_val_score(model, digitals_X, digitals_y, cv=5)
print("平均正确率: ", scores.mean())

# 测试集上的预测
# predictions = model.predict(X_test)
# print(predictions)
