import numpy as np
from time import time

a = np.random.rand(1000_0000)

aa = np.arange(1000_0000)

t=time()
b = a[a==0.5]
print(time()-t)

t=time()
b = a[a==505053]
print(time()-t)
