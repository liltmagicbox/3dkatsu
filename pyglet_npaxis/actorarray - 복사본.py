import numpy as np

import numba as nb

#https://docs.scipy.org/doc/numpy-1.15.1/reference/ufuncs.html
#deg2rad arccos...


#ufunc=================================
#for not numba, uncomment @nb.jit manually.
#@nb.jit(nopython=True , parallel = True)
def ufunc_location_noacc(pos,speed,dt):
    #hope we not use it..
    pos += speed*dt
    return pos
@nb.jit(nopython=True , parallel = True)
def ufunc_posspeed(pos,speed,acc,dt):
    speed += acc*dt
    pos += speed*dt
    return pos,speed

#ufunc=================================

class Actorarray_with_comment:
    def __init__(self, modelN):
        attributes = 20
        #assert attributes >=10,"attrs more than 10."
        row = modelN
        column = attributes
        self.array = np.zeros(column*row).reshape(column,row).astype('float32')
        #shape = (attrs,N) it's fast ~10x.
        #id0 id1 id2 id3...
        #x0 x1 x2 x3...
        #y0 y1 y2 y3...
        #z0 z1 z2 z3...
        self.intarray = np.zeros(column*row).reshape(column,row).astype('int32')
        
        row = 16
        self.gpumodelmat = np.zeros(column*row).reshape(column,row).astype('float32')
        # col.major modelmat shape = (N,16) [ [x0,x4,x8,x12,x1,,,], [x0,x4,x8,x12,x1,,,] ,,, ]

        
        
        #index setting.
        #self.id= np.index_exp[0,:]
        #self.id= np.index_exp[0]
        #np.index_exp == (slice(1, 4, None),) <class 'tuple'> ,,, a[slice(4,7)] == a[4:7]
        #you can use simply: slice(a,b), for a[a:b], instead of :np.index_exp[a:b]
        
        self.posupdate = 0 #by doing so, it seems like attr, not idx.
        self.posx = 1 #by doing so, it seems like attr, not idx.
        self.posy = 2
        self.posz = 3
        self.pos = np.index_exp[1:4]
        self.speedx = 4
        self.speedy = 5
        self.speedz = 6
        self.speed = np.index_exp[4:7]
        self.accx = 7
        self.accy = 8
        self.accz = 9
        self.acc = np.index_exp[7:10]

        self.rposupdate = 10 #since a dot don't rotate..
        self.rposx = 11
        self.rposy = 12
        self.rposz = 13
        self.rpos = np.index_exp[11:14]
        self.rspeedx = 14
        self.rspeedy = 15
        self.rspeedz = 16
        self.rspeed = np.index_exp[14:17]
        self.raccx = 17
        self.raccy = 18
        self.raccz = 19
        self.racc = np.index_exp[17:20]

        #----post attr value setting.
        self.array[self.posupdate] = 1 #1 faster than 1.0
        self.array[self.rposupdate] = 0
        #self.intarray[self.posupdate] = 1 #float faster than int


    def update(self,dt):
        self.update_location(dt)
        self.update_rotation(dt)

    def update_location(self,dt):
        pos = self.array[self.pos]
        speed = self.array[self.speed]
        acc = self.array[self.acc]

        pos,speed = ufunc_posspeed(pos,speed,acc,dt)

    #@profile
    def update_rotation(self,dt):
        pos = self.array[self.rpos]
        speed = self.array[self.rspeed]
        acc = self.array[self.racc]

        pos,speed = ufunc_posspeed(pos,speed,acc,dt)

a=Actorarray_with_comment(100_0000)

NN = a.array.shape[1]
a.array[a.accx] = np.random.rand(NN)
a.array[a.posupdate] = np.random.rand(NN)>0.5
a.intarray[a.posupdate] = np.random.rand(NN)>0.5
a.array[a.raccx] = np.random.rand(NN)

a.update_location(0.1)
a.update_rotation(0.1)
print(a.array)

from time import time

t = time()
for i in range(99999999):
    a.update(0.01)
    if time()-t>1.0:
        break
print(i,NN,'complexed location') #62fps pos+rot 217withjit..huh? jit18fps 10M..slow!


t = time()
for i in range(200):
    a.update(0.01)
print(i,NN,'complexed xxx') #62fps pos+rot 217withjit..huh? jit18fps 10M..slow!
print(time()-t)



#-------------------------------------------------------------------

# 1M, pos 130fps. pos+rot 60fps maybe.fine.. //compared 100k of col.major took 200fps. x8 faster.

#see slicing takes so time..
#142 100000 complexed location
#1619 100000 rotation
#14 1000000 complexed location
#134 1000000 rotation
#huh. masking and get attr kinds are bad!
#=======================================

#reason for col.major array:
#1.speed
# when update = pos+=speed
# rowmajor 10xfaster than col.major.
# 100k 463 vs3100
# 1M 43 vs 278
# withjit,
# 100k 9600 vs13464
# 1M 697 vs 1389

# if items of70, defenitely 10x speed.
# 1M 22vs267
# jit
# 1M 95vs 1385.

# 10M row   25
# 10M row jit 76

#2. attr utility
# 2-1 we can skip [:]
# actors.array[actors.posx]
# actors.array[1]
# actors.array[actors.posx,55]
# actors.array[actors.posx][55]
# 2-2 even set new attr
# actors.newattr = 56
# actors.array[56] = np.random.rand( len(actors) )

#.. why another array for gpumodelmat, gpuready ?
# vbo where stores data requires col.major., not [x1,x2,x3,x4,,] but[x1 x5 x9 x14] of modelmat row1.

