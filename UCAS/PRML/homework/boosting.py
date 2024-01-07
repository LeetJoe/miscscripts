from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score
import time
from datetime import datetime
from utils import load_mnist

data_path = '../data/'
(batch_x, batch_y), (test_x, test_y) = load_mnist(data_path, normalize=True)
stop_acc = 0.95

print("Start Gradient Boosting...")
StartTime = time.clock()

for i in range(10, 100, 10):
    clf_rf = GradientBoostingClassifier(n_estimators=i)
    clf_rf.fit(batch_x, batch_y)

    y_pred_rf = clf_rf.predict(test_x)
    acc_rf = accuracy_score(test_y, y_pred_rf)
    print("%s n_estimators = %d, accuracy:%f" % (datetime.now(), i, acc_rf))
    if acc_rf > stop_acc:
        break

EndTime = time.clock()
print('Total time %.2f s' % (EndTime - StartTime))
