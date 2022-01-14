import numpy as np


a = np.arange(10)


#https://numpy.org/doc/stable/reference/generated/numpy.place.html

np.place( a, a>5, 999)
print(a)
#[  0   1   2   3   4   5 999 999 999 999]

a = np.arange(10)
np.copyto( a, 999, where= a>5)
print(a)
#same

#you can see it 's slite intension..


#https://numpy.org/doc/stable/reference/generated/numpy.put.html

a = np.arange(10)
np.put( a, 22, 999, mode='clip')
print(a)


a = np.arange(10)
np.put( a, [0,5], 999, mode='clip') #cant 0:5..
print(a)

# np have lots of, like diagonal!. how we could imagine seems to eyes..

#When axis is not None,
#this function does the same thing as “fancy” indexing
#ah, maybe screening is called fancy .
#np.take like a[4:5], but ahas aixs, so easy.


#extract eq of compress.fine.








#----------------------------------------------
from time import time

#https://numpy.org/doc/stable/reference/generated/numpy.mod.html
#np mod !wow.

ra= np.random.rand(1000_0000)
a= np.arange(1000_0000)
t=time()
#np.mod(a,5) #3ms

slicer = ra>0.5 #1ms<
#cc = ra[slicer] #5ms. SCREENING TOOK 5ms for 1M.
cc = np.extract(slicer, ra) #took 6ms!
print(time()-t)

a = np.arange(10)
#a>5
#np.nonzero(a>5)
#(array([6, 7, 8, 9], dtype=int64),)

a= np.random.rand(1000_0000)
t=time()
indices_of_TRUE = np.nonzero( a>.999 )
c= a[indices_of_TRUE]
#array([    222,    2622,    3953, ...,
#np.unravel_index( indices_of_TRUE, a this recovers shape.
print(time()-t)



a= np.random.rand(1000_0000)
t=time()
c = a[a>.999]
print(time()-t)


#was 0.0099 and now 0.04787492752075195
#because of creating new result array.hahaha!
#means, creating array costs too much while compare is too less cost.
#and this was named SCREENING, but was actually creating was the timetaker.
a= np.random.rand(1000_0000)
t=time()
c= a[np.where(a>.199)]
print(time()-t)

#0.05684685707092285 for 10M.fine.
# 60ms 10M,  8ms for 1M. 2ms for 100k.
#...for random!you!
a= np.random.rand(1000_0000)
t=time()
a= np.random.rand(1000_0000)
print(time()-t)

#2ms. yeah. for 10M.
t=time()
a= np.zeros(1000_0000)
print(time()-t)

#0ms beccause we did it, maybe cpu still have compiled function in cache..
t=time()
a= np.zeros(1000_0000)
print(time()-t)

#arange took 8ms, for 10M. fine.
t=time()
a= np.arange(1000_0000)
print(time()-t)


#seems, compare == random == heavy ==, for1M, maybe 4ms.fine.
#0.005968332290649414 for 1M . it really slow!
#0.0528562068939209 10M
a= np.random.rand(100_0000)
t=time()
c= a[np.where(a>.099)]
print(time()-t)


#3ms. TF since. maybe 2ms took for and 1ms took for..
a= np.random.rand(100_0000)
t=time()
c= a[a>.099]
print(time()-t)



#-------finalyl unesersttood time taken
a= np.random.rand(100_0000)
t=time()
c= a[a>.99]
print(time()-t,'highground') #2ms. that


a= np.random.rand(100_0000)
t=time()
c= a[a>0.5]
print(time()-t,'mid') #6ms. 

a= np.random.rand(100_0000)
t=time()
c= a[a>0.01]
print(time()-t,'lower place') #3ms

#0.0019898414611816406 highground
#0.005015850067138672 mid
#0.0029931068420410156 lower place


#-----------------------for empty OR BOOLEAN ARRAY
a= np.random.rand(100_0000)
t=time()
cc = np.empty(1000_0000)
cc = np.empty(1000_0000, dtype=bool)
print(time()-t,'extream fast!')
#0.0010364055633544922 extream fast!


#2ms for 10M.. this is the minimum standard.
#0.002027750015258789 extream fast!
a= np.random.rand(100_0000)
t=time()
np.full(1000_0000, True, dtype=bool)
print(time()-t,'extream fast!')


#np.zeros(10)
#np.empty(10)

#anyway use nonzero not where, if TF.

#whats this for??
x = np.array([[3, 0, 0], [0, 4, 0], [5, 6, 0]])
print(np.nonzero(x))
#(array([0, 1, 2, 2], dtype=int64), array([0, 1, 0, 1], dtype=int64))
#maybe 0,0,    1,1,   2,0,   2,1. .fine.





exit()
#----------------------------------------------
#when a[a>.99] first
#0.013963460922241211
#0.011967897415161133

#when nonzero indices first
#0.0
#0.011968135833740234

#np.unravel_index
#???

#https://stackoverflow.com/questions/47068017/alternative-to-numpy-argwhere-to-speed-up-for-loop-in-python




a = np.arange(10)
for x in np.nditer(a):
    print(x, end=' ')



0.9685750007629395
0.18650102615356445


print("-----------------------")

#0.18. faster
a = np.random.rand(1252350)
t=time()
for i in a:
    i==3
print(time()-t)

#while 0.97 slower!huh..why..why!
a = np.random.rand(1252350)
t=time()
for x in np.nditer(a):
    x==3
print(time()-t)


print("-----------------------")
a = np.arange(10)
#When forcing an iteration order, we observed that the external loop
# option may provide the elements in smaller chunks 
for x in np.nditer(a, flags=['external_loop','buffered'], order='F'):
    print(x, end=' ')


#https://numpy.org/doc/stable/reference/arrays.nditer.html
a = np.arange(6).reshape(2,3)
with np.nditer(a, op_flags=['readwrite']) as it:
   for x in it:
       x[...] = 2 * x
print(a)
