import random
from statistics import mean
import sys
import time
import numpy as np
from prometheus_client import Counter
from scipy import rand

mem = 0

def counter(func):
    def wrap(*args, **kwargs):
        wrap.count += 1
        return func(*args, **kwargs)
    wrap.count = 0
    return wrap

@counter
def mergeSortRecursive(array, left, right):
    global mem
    start_time = time.time()
    if left + 1 >= right:
        return
    mid = int((left + right) / 2)
    mergeSortRecursive(array, left, mid)
    mergeSortRecursive(array, mid, right)
    mem += merge(array, left, mid, right)
    sort_time = time.time() - start_time

    return sort_time

def analysis(N):
    global mem
    mem = 0
    mergeSortRecursive.count = 0
    min = 10e+5
    max = -1
    average = []
    for i in range(20):
        arr = np.array([random.uniform(-1,1) for i in range(N)])
        res = mergeSortRecursive(arr, 0, len(arr))
        if (res > max):
            max = res
        if (res < min):
            min = res
        average.append(res)
    print(f'При {N} элементах: min: {min} sec | max: {max} sec | avg:{mean(average)} sec | mem: {mem / 20} bytes | count_functions: {mergeSortRecursive.count / 20}')

def merge(array, left, mid, right):
    it1 = 0
    it2 = 0
    res = []

    while (left + it1 < mid) and (mid + it2 < right):
        if array[left + it1] < array[mid + it2]:
            res.append(array[left + it1])
            it1 += 1
        else:
            res.append(array[mid + it2])
            it2 += 1

    while left + it1 < mid:
        res.append(array[left + it1])
        it1 += 1
    
    while mid + it2 < right:
        res.append(array[mid + it2])
        it2 += 1
    
    for i in range(it1 + it2):
        array[left + i] = res[i]
    
    return sys.getsizeof(res)


items = 1000
for i in range(8):
    analysis(items)
    items = items * 2

