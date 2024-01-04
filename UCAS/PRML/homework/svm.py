# 导入sklearn的数据集
import joblib
import sklearn.datasets as sk_datasets
 
digitals = sk_datasets.load_digits()
digitals_X = digitals.data #导入数据
digitals_y = digitals.target #导入标签
 
# 创建数据集
import sklearn.datasets._samples_generator as sk_sample_generator
X,y=sk_sample_generator.make_classification(n_samples=6,n_features=5,n_informative=2,n_redundant=3,n_classes=2,n_clusters_per_class=2,scale=1,random_state=20)
for x_,y_ in zip(X,y):
    print(y_,end=": ")
    print(x_)
 
# 数据集划分
import sklearn.model_selection as sk_model_selection
X_train,X_test,y_train,y_test = sk_model_selection.train_test_split(digitals_X,digitals_y,train_size=0.8,random_state=20)
 
# 数据预处理
import sklearn.preprocessing as sk_preprocessing
 
# 数据归一化
scaler = sk_preprocessing.StandardScaler().fit(X)
new_X = scaler.transform(X)
print('基于mean和std的标准化:',new_X)
 
scaler = sk_preprocessing.MinMaxScaler(feature_range=(0,1)).fit(X)
new_X=scaler.transform(X)
print('规范化到一定区间内',new_X)
 
# 数据正则化
new_X = sk_preprocessing.normalize(X,norm='l2')
print('求二范数',new_X)
 
# 简易版(二选一)
# 直接使用SVM模型
import sklearn.svm as sk_svm
model = sk_svm.SVC(C=1.0,kernel='rbf',gamma='auto')
# 拟合模型
model.fit(X_train,y_train)
# 为模型打分
acc=model.score(X_test,y_test) #根据给定数据与标签返回正确率的均值
print('SVM模型评价:',acc)
# 结果：0.494
 
# 优化版(二选一)
from sklearn.model_selection import GridSearchCV
from sklearn import svm
# 定义模型和参数
parameters = {'kernel': ('linear', 'rbf'), 'C': [1, 10]}
svc = svm.SVC()
# 进行网格搜索
model = GridSearchCV(svc, parameters)
model.fit(digitals.data, digitals.target)
# 输出最优模型参数和得分
print(model.best_params_)
print(model.best_score_)
# 结果：0.974
 
# 交叉验证(可选)
# 执行交叉验证并计算模型的性能指标
from sklearn.model_selection import cross_val_score
scores = cross_val_score(model, digitals_X, digitals_y, cv=5)
# 输出交叉验证的性能指标
print("交叉验证得分: ", scores)
print("平均准确率: ", scores.mean())
 
# 模型保存载入
# 保存模型
joblib.dump(model, 'svm_model.pkl')
# 加载模型
loaded_model = joblib.load('svm_model.pkl')
# 使用加载的模型进行预测
predictions = loaded_model.predict(X_test)
# 看看预测结果
print(predictions)