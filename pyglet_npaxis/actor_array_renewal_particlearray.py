import numpy as np
import numba as nb


import random
import timeit
from time import time

attributes = 7
class Actorarray:
    def __init__(self, modelN):
        row = attributes
        column = modelN
        self.array = np.zeros(column*row).reshape(column,row).astype('float32')#232 vs 170.wow.
        
        self.id= np.index_exp[:,0]
        self.posx = np.index_exp[:,1]
        self.posy = np.index_exp[:,2]
        self.posz = np.index_exp[:,3]
        self.pos = np.index_exp[:,1:4]
        self.speedx = np.index_exp[:,4]
        self.speedy = np.index_exp[:,5]
        self.speedz = np.index_exp[:,6]
        self.speed = np.index_exp[:,4:7]

        # self.id= np.index_exp[0,:]
        # self.posx = np.index_exp[1]
        # self.posy = np.index_exp[2]
        # self.posz = np.index_exp[3]
        # self.pos = np.index_exp[1:4]
        # self.speedx = np.index_exp[4]
        # self.speedy = np.index_exp[5]
        # self.speedz = np.index_exp[6]
        # self.speed = np.index_exp[4:7]

    def update(self,dt):
        self.updateLocation(dt)

    def updateLocation(self,dt):
        speed = self.array[self.speed]
        pos = self.array[self.pos]

        pos = calculate_location(pos,speed,dt)




class Actorarray_rowmajor:
    def __init__(self, modelN):
        row = modelN
        column = attributes
        self.array = np.zeros(column*row).reshape(column,row).astype('float32')#232 vs 170.wow.
        
        self.id= np.index_exp[0,:]
        self.posx = np.index_exp[1]
        self.posy = np.index_exp[2]
        self.posz = np.index_exp[3]
        self.pos = np.index_exp[1:4]
        self.speedx = np.index_exp[4]
        self.speedy = np.index_exp[5]
        self.speedz = np.index_exp[6]
        self.speed = np.index_exp[4:7]

    def update(self,dt):
        self.updateLocation(dt)

    def updateLocation(self,dt):
        speed = self.array[self.speed]
        pos = self.array[self.pos]

        pos = calculate_location(pos,speed,dt)



#=======================================

#@nb.jit(nopython=True , parallel = True)#9000
def calculate_location(pos,speed,dt):
    pos += speed*dt    
    return pos

def test(creater,NN):
    #NN = 1000000
    A = creater(NN) #272 for 1M. fine. ..with no jit?? ...jit 913.huh..
    A.array[A.speedx] = np.random.rand(NN)
    A.array[A.speedy] = np.random.rand(NN)
    A.array[A.speedz] = np.random.rand(NN)
    t = time()
    for i in range(100000):
        A.update(0.01)
        if time()-t>1.0:
            break
    print(i,NN)

print('without jit')
test(Actorarray, 100_000)
test(Actorarray_rowmajor, 100_000)
test(Actorarray, 100_0000)
test(Actorarray_rowmajor, 100_0000)


@nb.jit(nopython=True , parallel = True)#9000
def calculate_location(pos,speed,dt):
    pos += speed*dt    
    return pos

print(' jit fullcore')
test(Actorarray, 100_000)
test(Actorarray_rowmajor, 100_000)
test(Actorarray, 100_0000)
test(Actorarray_rowmajor, 100_0000)


#=======================================
#i7 10700

# without jit
# 463 100000
# 3100 100000
# 43 1000000
# 278 1000000
#  jit fullcore
# 9600 100000
# 13464 100000
# 697 1000000
# 1389 1000000

#100k, 9x / 1.3x faster
#1M, 6.5x / 2x faster.


#---at items 70. row more win!
# without jit
# 292 100000
# 3087 100000
# 22 1000000
# 267 1000000
#  jit fullcore
# 1710 100000
# 13392 100000
# 95 1000000
# 1385 1000000


#10M, 25,78fps.fine.


#-------------------------------below old trash data

# SPEED TEST RESULT:

#--with acc colmajor
#1M, 12,85
#--without acc colmajor
#1M, 44, 414
#--without acc row major
#1M, 269, 979

#rowmajor extream fast, as we expected. EVEN FASTER than JIT!

#100k row, 3274,10338 .huh..EXTREAM FAST. while col 458,9159

#=======================================================


#10452 for 100k. seems fair..
#1M 868. nearly 10x slower. acceptable.!

#100k, 3256, 10570.
#1M, 266, 848.

#when  1000.000 , 26row=12fps(jit85) 126row=8fps(jit45)  31row 10,79. 15row_14,126fps.  26row_16,179 even noacc.



#when row =13.
#np: ([100, 1000, 10000, 100000], [87017, 20990, 2496, 226])
#np numba full core: ([100, 1000, 10000, 100000], [25468, 47121, 33785, 10249])

#21
#np: ([100, 1000, 10000, 100000], [84532, 20414, 2496, 220])
#np numba full core: ([100, 1000, 10000, 100000], [23369, 43370, 31865, 9106])

#25
#np: ([100, 1000, 10000, 100000], [84031, 20419, 2489, 202])
#np numba full core: ([100, 1000, 10000, 100000], [24062, 43746, 32498, 9659])

#27
#np: ([100, 1000, 10000, 100000], [83836, 20381, 2506, 208])
#np numba full core: ([100, 1000, 10000, 100000], [26942, 48120, 34872, 9795])

#30
#np: ([100, 1000, 10000, 100000], [84427, 20380, 2481, 214])
#np numba full core: ([100, 1000, 10000, 100000], [24051, 42229, 30810, 9345])

#32
#np: ([100, 1000, 10000, 100000], [85720, 20235, 2460, 197])
#np numba full core: ([100, 1000, 10000, 100000], [25883, 47131, 33147, 8913])

#35
#np: ([100, 1000, 10000, 100000], [84474, 20262, 2486, 173])
#np numba full core: ([100, 1000, 10000, 100000], [24188, 43407, 32383, 8162])

#37
#np: ([100, 1000, 10000, 100000], [83195, 20368, 2468, 176])
#np numba full core: ([100, 1000, 10000, 100000], [25157, 47445, 33990, 8189])

#39
#np: ([100, 1000, 10000, 100000], [84582, 19671, 2467, 171])
#np numba full core: ([100, 1000, 10000, 100000], [25459, 46858, 33096, 7340])

#40
#np: ([100, 1000, 10000, 100000], [85327, 20198, 2412, 162])
#np numba full core: ([100, 1000, 10000, 100000], [26037, 47515, 33873, 5239])

#50
#np: ([100, 1000, 10000, 100000], [84992, 19661, 2337, 150])
#np numba full core: ([100, 1000, 10000, 100000], [25877, 46372, 32181, 2733])

#when row = 103.
#np: ([100, 1000, 10000, 100000], [85377, 19246, 1965, 135])
#np numba full core: ([100, 1000, 10000, 100000], [23551, 43310, 27686, 1866])
