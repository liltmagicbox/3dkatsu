import numpy as np
from time import time


#-------finalyl unesersttood time taken

a= np.random.rand(100_00000)
t=time()
c= a[a>0.01]
print(time()-t,'lower place') #3ms

a= np.random.rand(100_00000)
t=time()
c= a[a>0.5]
print(time()-t,'mid') #6ms. 

a= np.random.rand(100_00000)
t=time()
c= a[a>0.01]
print(time()-t,'lower place') #3ms


a= np.random.rand(100_00000)
t=time()
c= a[a>.99]
print(time()-t,'highground') #2ms. that



a= np.random.rand(100_00000)
t=time()
c= a[a>0.9]
print(time()-t,'mid2') #5ms.  still slow.


#0.79 300M
#30M 80ms
a= np.random.rand(3000_0000)
t=time()
c= a[a>0.9]
print(time()-t,'gaga') #5ms.  still slow.

#0.0019898414611816406 highground
#0.005015850067138672 mid
#0.0029931068420410156 lower place

#0.0019948482513427734 highground
#0.005990743637084961 mid
#0.002993345260620117 lower place

#why?

#0.004987001419067383 mid
#0.0029921531677246094 lower place
#0.001994609832763672 highground

# 0.5 is most slower. even 2x. why???
# 1ms took for creating 1M array, maybe?? yeah since it's float, not zeros.

#100k create took +2ms while 2ms is not the fact.



#lower fisrt. mid really is slow!!!!!

##0.026927947998046875 lower place
##0.05585050582885742 mid
##0.029919862747192383 lower place
##0.015957355499267578 highground
##0.02892279624938965 mid2
