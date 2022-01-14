import numpy as np
from time import time

x= np.random.rand(20).astype('float32')

r = np.round(x) #maybe 0.5>,1.
print(r)
print(r.dtype)

#The floor of the scalar x is the largest integer i, such that i <= x
f = np.rint(x)
print(f)
print(f.dtype)


#to blow up .xx , trunc. truncate.
#floor -0.1 to -1.fine.

np.round(x,3) # to N th floor
np.around #0.5
np.rint # near int
np.ceil  #up
np.trunc #down

np.fix # +- toward 0.


#Math.rint(2.5) is 2. to near number
#Math.round(2.5) is 3. to up from 0.5..

#samespd

x= np.random.rand(1000_0000).astype('float32')
t = time()
r = np.round(x) #maybe 0.5>,1.
print(r)
print(r.dtype)
print(time()-t)

x= np.random.rand(1000_0000).astype('float32')
t = time()
#The floor of the scalar x is the largest integer i, such that i <= x
f = np.rint(x)
print(f)
print(f.dtype)
print(time()-t)


x= np.random.rand(1000_0000).astype('float32')
t = time()
#The floor of the scalar x is the largest integer i, such that i <= x
f = np.trunc(x)
print(f)
print(f.dtype)
print(time()-t)



x= np.random.rand(1000_0000).astype('float32')
t = time()
#The floor of the scalar x is the largest integer i, such that i <= x
f = np.ceil(x)
print(f)
print(f.dtype)
print(time()-t)
