
import numpy as np


# 检查矩阵是否是 2 维矩阵
def check_2d(mt):
    return len(mt.shape) == 2


# 检查矩阵是否为非 0 方阵
def check_square(mt):
    if check_2d(mt) and mt.shape[1] == mt.shape[0] and mt.shape[0] > 0:
        return mt.shape[0]
    else:
        return False


# 交换矩阵的第 i, j 行
def row_switch(mt, i, j):
    mt[[i, j], :] = mt[[j, i], :]
    return mt


# 求矩阵的转置
# 输入必须是 np.array()
def transpose(mt):
    if len(mt.shape) != 2 or mt.shape[1] < 1 or mt.shape[0] < 1:
        return None
    m, n = mt.shape
    mtt = np.zeros((n, m), mt.dtype)
    for i in range(m):
        mtt[:, i] = mt[i, :]
    return mtt


# LU 分解
# 返回：L, U 矩阵；异常时返回 None, None
def lu_factor(mt):
    n = check_square(mt)
    if not n:
        print('非方阵无法进行 LU 分解。')
        return None, None
    L = np.zeros((n, n), dtype=np.double)
    U = mt.copy()
    for j in range(n):
        pivot = j
        if U[pivot][j] == 0:
            print('主元为 0，无法完成分解。')
            # 主元为 0，不可解
            return None, None
        for i in range(pivot+1, n):
            # 遍历主元下的元素
            if U[i][j] != 0:
                # 如果元素不为 0，通过第 III 类初等变换化为 0
                L[i][j] = U[i][j]/U[pivot][j]  # 填充 L
                U[i][j] = 0
                for k in range(j+1, n):
                    # 当前行主元右侧的每一列执行第 III 类初等变换
                    U[i][k] -= L[i][j] * U[pivot][k]

    # 填充 L 主对角线上的 1
    for i in range(n):
        L[i][i] = 1

    return L, U


# 部分主元法求行阶梯矩阵
# 返回：矩阵的秩、行阶梯阵、以及记录行交换的向量；异常时返回 -1, None, None
def partial_pivot(mt):
    if not check_2d(mt):
        return -1, None, None
    m, n = mt.shape
    emt = mt.copy()  # final echelon matrix
    pv = [i for i in range(m)]  # 记录行交换
    pivot = 0
    for j in range(n):
        # 找到当前列的主元
        i_max = pivot
        for i in range(pivot + 1, m):
            if np.abs(emt[i][j]) > np.abs(emt[i_max][j]):
                i_max = i

        # 如果最大行不在主元位置
        if i_max != pivot:
            # 记录行交换
            pv[i_max], pv[pivot] = pv[pivot], pv[i_max]
            # 完成行交换
            emt = row_switch(emt, i_max, pivot)

        # 主元位置是 0 则继续下一列
        if emt[pivot][j] == 0:
            continue

        # 主元位置不是 0，将其下面所有元素化为 0
        for l in range(pivot + 1, m):
            ratio = emt[l][j] / emt[pivot][j]
            for k in range(j, n):
                # 对整个行完成第 III 类初等变换
                emt[l][k] -= ratio * emt[pivot][k]
                if np.abs(emt[l][k]) < 1e-10:
                    emt[l][k] = 0

        pivot += 1
        if pivot == m:
            # 如果处理到了最后一行
            break

    # rank, echelon, P vector
    return pivot, emt, pv


# 利用部分主元法的结果，取得 rank
def get_rank(mt):
    r, _, _ = partial_pivot(mt)
    return r


# 计算输入向量的 2-norm
def v_norm2(v):
    if len(v.shape) != 1:
        return -1
    sqrt_sum = 0
    for i in range(v.shape[0]):
        sqrt_sum += np.power(v[i], 2)

    return np.sqrt(sqrt_sum)


# QR 分解
def qr_factor(mt):
    if not check_2d(mt):
        return None, None
    m, n = mt.shape
    if n > m:
        # 列数大于行数，列之间必线性相关
        return None, None

    r, emt, pv = partial_pivot(mt)
    if r != n:
        # 列线性相关，不可解
        return None, None

    # 保持一定精度
    mt = np.array(mt, dtype=np.double)
    q = np.zeros((m, n), dtype=np.double)
    r = np.zeros((n, n), dtype=np.double)
    for j in range(n):
        # 单位化当前列
        v = v_norm2(mt[:, j])
        u = mt[:, j]/v
        q[:, j] = u  # 记录到 Q 中
        r[j, j] = v  # v 是 R 的主对角元素
        if j == n - 1:
            # 已经到达最后一列，就不需要再计算下面的 w 了
            break
        for k in range(j+1, n):
            # 对所有尚未处理完的列向量，取它与新得到的单位向量的内积
            w = np.dot(u, mt[:, k])
            r[j, k] = w  # 填在 R 对应的位置上
            mt[:, k] -= np.multiply(u, w)  # 列减去本轮新得到的 u 方向上的分量

    return q, r


# 检查一个矩阵是否为上三角阵
def check_upper(mt):
    n = check_square(mt)
    if not n:
        return False
    for j in range(n):
        if mt[j][j] == 0:
            return False
        for i in range(j+1, n):
            if mt[i][j] != 0:
                return False

    return True


# 找到行阶梯矩阵对应的自由变量的位置。
# 输入必须是一个行阶梯阵。
def find_free_pos(mt):
    if not check_2d(mt):
        return None
    m, n = mt.shape
    j = 0  # 列
    i = 0  # 行
    pos = []
    while j < n:
        if i >= m:
            break
        if mt[i][j] == 0:
            for k in range(j, n):
                if mt[i][k] == 0:
                    pos.append(k)
                else:
                    i += 1
                    j = k + 1
                    break
        else:
            i += 1
            j += 1

    return pos


# 通过上阶梯形求解 x
# 输入 mt 必须是行阶梯形式，且 mt、b 必须是 np.array(dtype=double)
def echelon_calc_x(mt, b):
    m, n = mt.shape
    x = [0 for i in range(n)]
    for i in range(m-1, -1, -1):
        s = 0
        for j in range(n):
            if mt[i][j] != 0:
                s = j
                break

        for j in range(s+1, n):
            b[i] -= mt[i][j] * x[j]
        x[s] = b[i]/mt[i][s]
    return np.array(x)



# 通过上三角阵求解 x
def upper_calc_x(mt, b):
    if not check_upper(mt):
        print('矩阵不是上三角矩阵')
        return None

    n = len(b)
    x = [0 for i in range(n)]

    for i in range(n-1, -1, -1):
        for j in range(i+1, n):
            b[i] -= mt[i][j] * x[j]
        x[i] = b[i]/mt[i][i]

    return np.array(x)


# 求解行列式
def calc_x(mt, b):
    mt = np.array(mt, dtype=np.double)
    b = np.array(b, dtype=np.double)
    # 矩阵应是二维矩阵，b 应该是一维向量
    if (not check_2d(mt)) or (len(b.shape) != 1):
        print('输入参数维度有误')
        return None, None

    m, n = mt.shape
    # 矩阵行数应与 b 长度相同
    if m != len(b):
        print('向量长度应与矩阵行数相同')
        return None, None

    # 矩阵的秩
    r_1, emt_1, pv_1 = partial_pivot(mt)

    # 增广矩阵的秩
    amt = np.hstack((mt, b.reshape(len(b), 1)), dtype=np.double)
    r_2, emt_2, pv_2 = partial_pivot(amt)

    # 无解
    if r_1 != r_2:
        print('方程无解，将返回最小二乘解。')
        b = np.dot(transpose(mt), b)
        mt = np.dot(transpose(mt), mt)
        return calc_x(mt, b)

    if r_1 == n:
        # 列满秩
        q, r = qr_factor(mt)
        b = np.dot(transpose(q), b)
        return upper_calc_x(r, b), []
    else:
        # 存在自由变量
        return echelon_calc_x(emt_2[:, :-1], emt_2[:, -1]), find_free_pos(emt_2[:, :-1])


# 计算排序次数
def sort_count(v):
    n = len(v)
    c = 0
    for i in range(n):
        for j in range(i+1, n):
            if v[i] > v[j]:
                v[i], v[j] = v[j], v[i]
                c += 1
    return c


def det(mt):
    n = check_square(mt)
    if not n:
        print('必须是方阵！')
        return None

    r, emt, pv = partial_pivot(mt)

    if r < n:
        # 不满秩
        return 0

    switch_count = sort_count(pv)
    result = np.power(-1, switch_count)

    for i in range(n):
        result *= emt[i][i]

    return result