import numpy as np
from time import time

a = np.random.rand(1000_000) #5ms for 1M for iteration. wow!

b = np.empty(1000_000)

t = time()
#a[a>0.5] = 30 #6ms.
a*=5#10M 6ms.fine.
print(time()-t)



t = time()
for idx in np.nonzero(a>0.015)[0]: #nonz returns true. why?
    a[idx] ==5
    #if a[idx] ==5:
    #    1
print(time()-t, 'actually slow for indexing') #230ms

t = time()
for i in a[a>0.015]:
    c = i
print(time()-t,'this simple always fast..hahaha..') #53ms
#this memory access continuously. so fast, yeah.


t = time()
for idx in np.nonzero(a>0.015):
    a[idx]
print(time()-t)
#(array([0, 3, 4, 6, 8], dtype=int64),)

#0.5
#0.054856061935424805
#0.23189902305603027
#0.05690193176269531

#wowwowowwowowowowow
#just get index and iter is so fast!!!!

#10M 230ms iter 0.5 , 5M?

#0.015 fullsped
#0.04388236999511719
#0.3831472396850586
#0.051921844482421875

#10M, 50ms, for item by index
#10M, 380ms, for item, a[a>0.5]

