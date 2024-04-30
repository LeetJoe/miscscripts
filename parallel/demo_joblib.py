
# 这个只支持多进程并行，不清楚是否有多线程的模式。
import time
from joblib import Parallel, delayed


def job(start, end):
    result_list = []
    for i in range(start, end):
        result_list.append(i)

    return result_list


num_jobs = 6
batch_size = 4
total_size = 3000

start = time.time()
# delayed means if blocks are more than jobs, it will be processed one by one.
output = Parallel(n_jobs=num_jobs)(
    delayed(job)(i, min(i + batch_size, total_size)) for i in range(0, total_size, batch_size)
)

result = output[0]
for i in range(1, len(output)):
    result += output[i]

print(result)

end = time.time()
print('Execution time in seconds: {}'.format(end - start))

