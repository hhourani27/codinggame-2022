from time import time
import timeit
import numpy as np
from sys import getsizeof
#%%

N = 1000000
a = np.ones((N,8),dtype=np.int64)
start = time()
for i in range(N):
    a[i][0] = 10
print(time()-start)

start = time()
for i in range(N):
    b = [i]*8
print(time()-start)
