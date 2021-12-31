import numpy as np
import numba as nb
import timeit

from time import time
import random

modelN = [100, 1000, 10000, 100000]


def calculate_location(pos,speed,acc,dt):
    speed += acc*dt
    pos += speed*dt    
    return pos,speed

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


from matplotlib import pyplot as plt
x = [13,25,30,32,        35,    40,50, 103]
y= [10249,9659,9345,8913,  8162,     5239,2733,1866]
#plt.plot(x,y,'*-')
#plt.show()
#exit()
class Actorarray:
    def __init__(self, modelN):
        #0 123 456 789  101112  not R.
        # id xyz spd acc front  
        row = 26
        column = modelN
        matrow = 16 # rot trans scale .. for 4x4= matA[i] gpuready.        
        
        self.array = np.zeros(row*column).reshape(column,row).astype('float32')#232 vs 170.wow.
        self.matarray = np.zeros(matrow*column).reshape(column,matrow).astype('float32')#gpuready.

        #wow, matarray written once, read once. perfect! all 4x4 is remains as quaternion, fast mul.
        #self.id = np.index_exp[:,0] # maybe we don need it

        #self.id = array[:,0] if you do this, its not clear to see, and init run once. it's set attr.
        #..do anyway. we have sumlime.
        self.id= np.index_exp[:,0]

        self.posx = np.index_exp[:,1]
        self.posy = np.index_exp[:,2]
        self.posz = np.index_exp[:,3]
        self.pos = np.index_exp[:,1:4]

        self.speedx = np.index_exp[:,4]
        self.speedy = np.index_exp[:,5]
        self.speedz = np.index_exp[:,6]
        self.speed = np.index_exp[:,4:7]

        self.accx = np.index_exp[:,7]
        self.accy = np.index_exp[:,8]
        self.accz = np.index_exp[:,9]        
        self.acc = np.index_exp[:,7:10]

        self.frontx = np.index_exp[:,10]
        self.fronty = np.index_exp[:,11]
        self.frontz = np.index_exp[:,12]        
        self.front = np.index_exp[:,10:13]


    def ididx(self): return  np.index_exp[:,0]
    def posxidx(self): return  np.index_exp[:,1]
    def posyidx(self): return  np.index_exp[:,2]
    def poszidx(self): return  np.index_exp[:,3]
    def posidx(self): return  np.index_exp[:,1:4]
    def speedxidx(self): return  np.index_exp[:,4]
    def speedyidx(self): return  np.index_exp[:,5]
    def speedzidx(self): return  np.index_exp[:,6]
    def speedidx(self): return  np.index_exp[:,4:7]
    def accxidx(self): return  np.index_exp[:,7]
    def accyidx(self): return  np.index_exp[:,8]
    def acczidx(self): return  np.index_exp[:,9]        
    def accidx(self): return  np.index_exp[:,7:10]
    def frontxidx(self): return  np.index_exp[:,10]
    def frontyidx(self): return  np.index_exp[:,11]
    def frontzidx(self): return  np.index_exp[:,12]        
    def frontidx(self): return  np.index_exp[:,10:13]

    #this cannot used like aa.get_pos()+=5
    #def get_id(self): return  self.array[ np.index_exp[:,0]]

    def update(self,dt):
        self.updateLocation(dt)
        #please never do like this again..
        #calculate_location(self.array[:,1:4],self.array[:,4:7],self.array[:,7:10],dt)

    def updateLocation(self,dt):
        acc = self.array[self.acc]
        speed = self.array[self.speed]
        pos = self.array[self.pos]

        #since array not copied, it works well. but remember acc is an array,
        #not a value. even it acts like. putit tu ufunc-like func.
        pos,speed = calculate_location(pos,speed,acc,dt)        

        #or thisway.
        #self.array[self.speed] += self.array[self.acc]*dt
        #self.array[self.pos] += self.array[self.speed]*dt
        #self.pos += self.speed*dt


# aa.xyz +=3 fancy but looks like it's not ndarray..
# aa.array.xyz= i hope, but too complex structure.
# aa.array[aa.xyz] = #this directly tells everything.
# gpuready = aa.matarray.flatten()
# gpuready0 = aa.matarray.flatten()[aa.matrow0]
# gpuready1 = aa.matarray.flatten()[aa.matrow1]
# gpuready2 = aa.matarray.flatten()[aa.matrow2]
# gpuready3 = aa.matarray.flatten()[aa.matrow3]

def xxxnpupdate(carA):
    x=self.x
    A = self.A
    A[speed]+=A[acc]*dt
    A[pos]+=A[speed]*dt


#======================2 ways of access array.
aa=Actorarray(10)

#=== assign and add value
aa.array[aa.posx] =6
aa.array[aa.posx] +=1
#print(aa.array[aa.pos])

# assign random values
aa.array[aa.accx] = np.random.rand( len(aa.array) ) # but no more!!!!
#aa.updateLocation(5)
#print(aa.array[aa.pos])

# idx as variable,. very satisfying.
pp = aa.posidx()
aa.array[pp]+=3
#print(aa.array[pp])



# discussion record: posidx  not getpos.
# confusing getpos will return value.
#pos = aa.getpos()
#print( aa.array[pos] )


# discussion record: how to accessing array..
#aa.array[aa.x]
#aa[aa.x]
#aa[aa.pos] =5 #yeah
#aa.pos=5 #nonono
#we noticed: a.pos=5 is also a __setattr inner method.

#aa.accx = np.random.rand( len(aa.array) )
#aa.array[aa.acc] = np.random.random()
#aa.acc = np.random.random()# than, you lost a way to accces of it.






def do(modelN,maxframe=1000000):
    xxx,yyy=[],[]

    for model in modelN:
        xxx.append(model)
        A = Actorarray(model)

        A.array[A.accx]= np.random.rand( len(A.array) ) #thats since indexed is a row. ====>
        A.array[A.accy]= np.random.rand( len(A.array) ) #thats since indexed is a row. ====>
        #A.accz= np.random.rand( len(A.array) ) #thats since indexed is a row. ====>

        dts=[]
        for i in range(maxframe):
            dts.append( random.random()*0.01 )

        dts = np.random.rand(maxframe).astype('float')*0.01 #not that changeed. since not much loop...
        #A.update(dts[0])
        #print(calculate_location.signatures)
        #[(array(float64, 2d, A), array(float64, 2d, A), array(float64, 2d, A), int64), (array(float64, 2d, A), array(float64, 2d, A), array(float64, 2d, A), float64)]
        #--------------------loop on
        t = time()
        for i, dt in enumerate(dts):
        #for i in range(maxframe):
            #dt = dts[i]
            A.update(dt)
            if time()-t>1.0:
                break
        yyy.append(i)
    return xxx,yyy

print( 'np:', do(modelN) )







#===================== numba

import numba as nb
# ~32bit~   /jit 435  / nogil 441  nopy 441/ fastmath 433 / parallel 9632


#@nb.jit #435.. i think,,
#@nb.jit(nopython=True, nogil=True) #441! new record
#@nb.jit(nogil=True) #441! new record
#@nb.jit(fastmath=True) #little fast.


#@nb.jit(nopython=True , parallel = True)
#([100, 1000, 10000, 100000], [34302, 48582, 35608, 10413])
#800,0000 30fps, 400,0000 60fps, only pos-speed.yeah.


#=====not worked
#UniTuple(float64 x 2) cannot be represented as a Numpy dtype
#orrors by
#@nb.vectorize(target='cpu')

#import numexpr as ne
#pos = ne.evaluate("pos + speed*dt + acc*dt*dt")# 184 or 1322 vs numba parallel 9233. not useit.

#@nb.vectorize(nopython=True, target='cuda') https://thedatafrog.com/en/articles/boost-python-gpu/
#=====not worked

@nb.jit(nopython=True , parallel = True)
def calculate_location(pos,speed,acc,dt):
    speed += acc*dt
    pos += speed*dt    
    return pos,speed


print( 'np numba full core:', do(modelN) )