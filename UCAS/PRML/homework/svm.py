import time
from sklearn import svm
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import cross_val_score
from utils import load_mnist


data_path = 'data/'
(x_train, y_train), (x_test, y_test) = load_mnist(data_path, normalize=True)

stop_acc = 0.95
print("Start SVM Training...")
StartTime = time.clock()

parameters = {'kernel': ('linear', 'rbf'), 'C': [1, 10]}
svc = svm.SVC()
model = GridSearchCV(svc, parameters)
model.fit(x_train, y_train)

scores = cross_val_score(model, x_test, y_test, cv=5)
print("accuracy: ", scores.mean())

EndTime = time.clock()
print('Total time %.2f s' % (EndTime - StartTime))
