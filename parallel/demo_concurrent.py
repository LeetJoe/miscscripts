
# 既可以实现线程级并行，又可以实现进程进并行。
# 简单测试发现，进程级并行比 joblib 要快一倍以上；线程级并行又比进程级并行快 5 倍以上。

import time
import concurrent.futures


def job(start, end):
    result_list = []
    for i in range(start, end):
        result_list.append(i)

    return result_list


num_threads = 6
batch_size = 4
total_size = 3000

start = time.time()
with concurrent.futures.ProcessPoolExecutor(max_workers=num_threads) as executor:
    result = []
    future_to_sidx = {executor.submit(job, i, min(i + batch_size, total_size)): i
                      for i in range(0, total_size, batch_size)}
    for future in concurrent.futures.as_completed(future_to_sidx):
        # sidx = future_to_sidx[future]
        result += future.result()

    # print(result)
end = time.time()
print('Execution time in seconds: {}'.format(end - start))

start = time.time()
with concurrent.futures.ThreadPoolExecutor(max_workers=num_threads) as executor:
    result = []
    future_to_sidx = {executor.submit(job, i, min(i + batch_size, total_size)): i
                      for i in range(0, total_size, batch_size)}
    for future in concurrent.futures.as_completed(future_to_sidx):
        # sidx = future_to_sidx[future]
        result += future.result()

    # print(result)
end = time.time()
print('Execution time in seconds: {}'.format(end - start))
