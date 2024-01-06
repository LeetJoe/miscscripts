import joblib

import sklearn.datasets as sk_datasets
import sklearn.datasets._samples_generator as sk_sample_generator
import sklearn.model_selection as sk_model_selection
import sklearn.preprocessing as sk_preprocessing

import sklearn.svm as sk_svm


digitals = sk_datasets.load_digits()
digitals_X = digitals.data
digitals_y = digitals.target

X, y = sk_sample_generator.make_classification(n_samples=6,n_features=5,n_informative=2,n_redundant=3,n_classes=2,n_clusters_per_class=2,scale=1,random_state=20)
'''
for x_,y_ in zip(X,y):
    print(y_,end=": ")
    print(x_)
'''

X_train, X_test, y_train, y_test = sk_model_selection.train_test_split(digitals_X, digitals_y, train_size=0.8, random_state=20)

scaler = sk_preprocessing.StandardScaler().fit(X)
new_X = scaler.transform(X)  # 基于mean和std的标准化
 
scaler = sk_preprocessing.MinMaxScaler(feature_range=(0,1)).fit(X)
new_X=scaler.transform(X)  # scale into [0, 1]

new_X = sk_preprocessing.normalize(X,norm='l2')  # L2 normalization

model = sk_svm.SVC(C=1.0, kernel='rbf', gamma='auto')
model.fit(X_train,y_train)
acc = model.score(X_test,y_test)  # 计算正确率的均值
print('model score: ',acc)

predictions = model.predict(X_test)

print(predictions)
