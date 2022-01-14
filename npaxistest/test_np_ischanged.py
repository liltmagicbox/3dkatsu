import numpy as np
from time import time

a = np.random.rand(1000_0000)

oldman = a.copy()

if not np.array_equal(a, oldman):
    1
    #update()
    #sort
    #new oldman

t=time()
sum(a)
print(time()-t)
#10M 14ms for copy
#np.array_equal(a, oldman) #10M 10ms for equal
#d = hash(a.tobytes()) #44ms for 10M hash
#d = hash(a.data.tobytes())
#sum(a) 540ms!

#we can check for 1M, cost of 2.4ms,
# 1ms if not changed.


#what if hash? we don need exact check, but ischanged.
#https://madhatter106.github.io/DataScienceCorner/posts/speeding-up-numpy-array-comparison/
#https://stackoverflow.com/questions/16589791/most-efficient-property-to-hash-for-numpy-array
c = a.tobytes()
d = hash(c)
#>>> d
#6220987984616995882

#10M 44ms, 1M 5ms.
