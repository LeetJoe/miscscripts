
from utils import *


# 完成矩阵分解，当 type='qr' 时执行 QR 分解，其它情况执行 LU 分解。
def factorization(m, type='qr'):
    m = np.array(m)
    if type == 'qr':
        return qr_factor(m)
    else:
        return lu_factor(m)


m = [[1,2,-3,4],[4,8,12,-8],[2,3,2,1],[-3,-1,1,-4]]

A, B = factorization(m, type='lu')
print('A矩阵：')
print(A)
print('B矩阵：')
print(B)
if A is not None and B is not None:
    print('结果验证：')
    print(np.dot(A, B))
else:
    print('无法完成分解！')

