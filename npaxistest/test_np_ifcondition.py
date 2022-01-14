import numpy as np
from time import time

#result
# vectorize inner for loop. dont use it

# a>0.5 check TF 10M 6ms. fast.
#BUT accessing by TF, 10M 50ms. so slow, since per-item.

# a[a>0.5] screening took 1M 6ms
# a[a>0.5]==555 value insert took 1M 6ms? fast anyway

#from TF,  1000 1ms 10000 also 1ms 100k 4ms 50k 2ms. fine.

# bool flaoat anyway compare seems samespd or vary.. donno well.


#+++ what if small amount SCRENNING?
#0.009973526000976562 10ms for .. 10000.
a = np.random.rand(1000_000)
t = time()
#a>0.999 #yeah 10M 6ms for TF.
b = a[a>0.999] #10000, +4ms. fine.
print( time()-t )
print(len(b),'result items, from 1M, took 1ms. wow!')


a = np.random.rand(1000_000)
t = time()
b = a[a>0.95] #10000, +4ms. fine.
print( time()-t )
print(len(b),'result items, from 1M, took 1ms. wow!')
#from TF,  1000 1ms 10000 also 1ms 100k 4ms 50k 2ms. fine.


#61ms for 10M True insert
a = np.random.rand(1000_0000)
t = time()
a[a>0.5]=888
print( time()-t )

#52ms for 10M create new True array
a = np.random.rand(1000_0000)
t = time()
b = a[a>0.5]
print( time()-t )

#5ms for 10M create TF array
a = np.random.rand(1000_0000)
t = time()
BB = a>0.5
print( time()-t )



#8ms for 10M True insert
a = np.random.rand(1000_0000)
t = time()
a[a>5]=888 #if maybe SCREENING for-like assess, it access not! so fast.
print( time()-t )


#-------------------------------------


a = np.random.rand(1000_0000)

def mas(X):
    if X>0.5:
        return 99
    return X


a = np.random.rand(10)


#c = mas(a) #err.

vfunc = np.vectorize(mas, otypes=[float])
#it works!!!!!!!!!!
#but its for easy use, it's basically for loop. fine.
c = vfunc(a)

print(c)

from time import time


a = np.random.rand(1000_0000)
t = time()
c = vfunc(a)
print( time()-t )

a = np.random.rand(1000_0000)
t = time()
np.place( a, a>0.5, 99)
print( time()-t )

#this is faster!!! .. ah? yeah. do this, not place. fine.yeah.
a = np.random.rand(1000_0000)
t = time()
a[a>0.5]=999
print( time()-t )
#this is view, and change value directly. so fast.


a = np.random.rand(1000_0000)
t = time()
np.place( a, a>0.5, 99)
print( time()-t )

#11ms for place where condition is True.
#it's extream fast, not conditioning.. SCREENING.. yeah.


#>>> np.place( a  , np.arange(10)>5, 999)
#>>> a
#array([  0,   1,   2,   3,   4,   5, 999, 999, 999, 999])


#a[a>5]=999
#array([  0,   1,   2,   3,   4,   5, 999, 999, 999, 999])




#int compare 1M 1ms
#float compare 1M 5ms



#8ms . 1M compare. fine. fine. 6ms for compare, 2ms for new array.
a = np.random.rand(1000_000)
t = time()
c = a[a>0.5]
print( time()-t, 'yeah' )


#----------------check took so fast. yeah. 10M 6ms,fine.

a = np.random.rand(1000_0000)
c = a>0.5
t = time()
c==True
print( time()-t ,'bool check') #not that fast. ok..

#0.004987478256225586 floatcheck
#0.0069811344146728516 bool check

a = np.random.rand(1000_0000)
t = time()
a>0.5
print( time()-t, 'floatcheck' )



#both check took 6ms for 10M. fine.
#0.5 or 5. what..? antyway..
#10 and 1M both 6ms????what?????

#see, compare int is 5x faster than float.

# when int 5
1.0888502597808838
0.010960102081298828
0.007970094680786133
0.010971784591674805
0.006982326507568359

#when float 0.5
1.0895206928253174
0.04487872123718262
0.05784916877746582
0.04487967491149902
0.00698399543762207
