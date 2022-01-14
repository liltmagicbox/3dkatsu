import numpy as np
from time import time

print('---flip test ..seems same speed..fine.')

a= np.random.rand(1000_00000)
t=time()
c= a[::-1]
print(time()-t,'rev_indexing')


a= np.random.rand(1000_00000)
t=time()
c = np.flip(a)
print(time()-t,'flip')

#10M

#100M
#0.0 rev_indexing
#0.017949342727661133 flip

#0.0009975433349609375 flip
#0.01798248291015625 rev_indexing






#js 1M 2000ms
#c++ 1M 250ms
#np 1M 50ms
print('---sort test.')
#sort or argsort-idx. whatto 
a= np.random.rand(100_00000)
t=time()
c= np.sort(a)
print(time()-t,'mid') #680ms 10M


a= np.random.rand(100_0000)
t=time()
c= a.sort()
print(time()-t,'method') #60ms. 1M

a= np.random.rand(100_0000)
t=time()
#c= a.sort('stable')#err
c= a.sort(kind='stable')
print(time()-t,'stable') #70ms. 1M


#0.05684852600097656 method
#0.07383227348327637 stable
#sort for 1M was 56ms, not 5ms??






print('---see conditions took 6ms for 1M.')
a= np.random.rand(100_00000)
t=time()
c= a[a>0.01]
print(time()-t,'lower place') #30ms 10M

a= np.random.rand(100_00000)
t=time()
c= a[a>0.5]
print(time()-t,'mid') #60ms. 10M


a= np.random.rand(100_0000)
t=time()
c= a[a>0.5]
print(time()-t,'mid') #6ms. 1M








print('--- condition vs for loop.')
a= np.arange(1000_000)
t=time()
c= a[a>0.9]
print(time()-t,'lower place')

a= np.arange(1000_000)
t=time()
c=[]
for i in a:
    if i>0.9:
        1#c.append(i) #.85 from .95
print(time()-t,'mid')

#0.002003192901611328 lower place
#0.909130334854126 mid
#yeah..
#for loop 1M takes, 1seconds. fine.





print('--- div vs TF spedd')
a= np.random.rand(1000_0000)
t=time()
c = a[a>0.5]
print(time()-t,'normal 60ms')

a= np.random.rand(1000_0000)
t=time()
(a*10//5).astype('bool')
print(time()-t,'bool')




a= np.random.rand(1000_0000)
t=time()
trus = np.nonzero(a*10//5) #0.4557812213897705 for 10M mul,div,nonzero.
#above_05 = a[trus]
print(time()-t,'get only truth')

#0.05188870429992676 normal 60ms
#0.3849673271179199 bool 380ms.. too slow!!!! astype.
#0.46475648880004883 get only truth  anywhay its slow!
#y4eah , astype took so much time..


a= np.random.rand(1000_000)
t=time()
#a = a*10//5 #34ms
#a = a*10 # 1-2ms
#a *= 10 # 0ms
#a = a//5 #24ms
#a = np.mod(a,5) #23ms. fine.
a = np.floor_divide(a,5)#23ms.. too.

print(time()-t,'div mmult took')
#0.3480691909790039 div mmult took
#yeah. it took so much.
# 10M 340ms mul,div.
# 1M 34ms..? wow.. EXTREAM SLOW!!!!



a= np.random.rand(1000_0000)
bb = np.full(1000_0000, True)
t=time()
bb[:] = [a>0.5]
print(time()-t,'bool')




print('---  i don want use select.')
x = np.arange(6)
condlist = [x<3, x>3]
choicelist = [x, x**2]
np.select(condlist, choicelist, 42)

#0.026955366134643555 lower place
#3.674661636352539 select
