import sklearn.datasets as sk_datasets
import sklearn.datasets._samples_generator as sk_sample_generator
import sklearn.model_selection as sk_model_selection
import sklearn.preprocessing as sk_preprocessing

from sklearn import svm
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score

digitals = sk_datasets.load_digits()

X_train, X_test, y_train, y_test = sk_model_selection.train_test_split(digitals.data, digitals.target, train_size=0.8,
                                                                       random_state=20)

parameters = {'kernel': ('linear', 'rbf'), 'C': [1, 10]}
svc = svm.SVC()
model = GridSearchCV(svc, parameters)
model.fit(X_train, y_train)

scores = cross_val_score(model, X_train, y_train, cv=5)
print("train score: ", scores.mean())

scores = cross_val_score(model, X_test, y_test, cv=5)
print("test score: ", scores.mean())
