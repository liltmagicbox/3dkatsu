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

def ufunc_posspeed(pos,speed,acc,dt):
    speed += acc*dt
    pos += speed*dt
    return pos,speed

#ufunc=================================

class Actorarray_with_comment:
    def __init__(self, modelN):
        attributes = 20
        #assert attributes >=10,"attrs more than 10."
        row = attributes
        column = modelN
        self.array = np.zeros(column*row).reshape(column,row).astype('float32')
        #shape = (attrs,N) it's fast ~10x.
        #id0 id1 id2 id3...
        #x0 x1 x2 x3...
        #y0 y1 y2 y3...
        #z0 z1 z2 z3...
        
        row = 16
        self.gpumodelmat = np.zeros(column*row).reshape(column,row).astype('float32')
        # col.major modelmat shape = (N,16) [ [x0,x4,x8,x12,x1,,,], [x0,x4,x8,x12,x1,,,] ,,, ]
        
        
        #index setting.
        #self.id= np.index_exp[0,:]
        #self.id= np.index_exp[0]
        #np.index_exp == (slice(1, 4, None),) <class 'tuple'> ,,, a[slice(4,7)] == a[4:7]
        #you can use simply: slice(a,b), for a[a:b], instead of :np.index_exp[a:b]
        
        self.posupdate = np.index_exp[:,0] #by doing so, it seems like attr, not idx.
        self.posx = np.index_exp[:,1] #by doing so, it seems like attr, not idx.
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

        self.rposupdate = np.index_exp[:,10]
        self.rposx = np.index_exp[:,11]
        self.rposy = np.index_exp[:,12]
        self.rposz = np.index_exp[:,13]
        self.rpos = np.index_exp[:,11:14]
        self.rspeedx = np.index_exp[:,14]
        self.rspeedy = np.index_exp[:,15]
        self.rspeedz = np.index_exp[:,16]
        self.rspeed = np.index_exp[:,14:17]
        self.raccx = np.index_exp[:,17]
        self.raccy = np.index_exp[:,18]
        self.raccz = np.index_exp[:,19]
        self.racc = np.index_exp[:,17:20]

        self.array[self.posupdate] = 1.0
        self.array[self.rposupdate] = 0

    def update(self,dt):
        self.update_location(dt)
        self.update_rotation(dt)

    @profile
    def update_location(self,dt):
        need_update = self.array[self.posupdate]==1
        
        pos = self.array[need_update][self.pos]
        speed = self.array[need_update][self.speed]
        acc = self.array[need_update][self.acc]
        pos,speed = ufunc_posspeed(pos,speed,acc,dt)

        # posx = self.array[need_update][self.posx]
        # posy = self.array[need_update][self.posy]
        # posz = self.array[need_update][self.posz]
        # speedx = self.array[need_update][self.speedx]
        # speedy = self.array[need_update][self.speedy]
        # speedz = self.array[need_update][self.speedz]
        # accx = self.array[need_update][self.accx]
        # accy = self.array[need_update][self.accy]
        # accz = self.array[need_update][self.accz]

        # posx,speedx = ufunc_posspeed(posx,speedx,accx,dt)
        # posy,speedy = ufunc_posspeed(posy,speedy,accx,dt)
        # posz,speedz = ufunc_posspeed(posz,speedz,accx,dt)


        

    def update_rotation(self,dt):
        pos = self.array[:][self.rpos]
        speed = self.array[:][self.rspeed]
        acc = self.array[:][self.racc]

        pos,speed = ufunc_posspeed(pos,speed,acc,dt)

a=Actorarray_with_comment(100_0000)

NN = a.array.shape[0]
a.array[a.accx] = np.random.rand(NN)
a.array[a.posupdate] = np.random.rand(NN)>0.5
a.array[a.raccx] = np.random.rand(NN)

a.update_location(0.1)
a.update_rotation(0.1)
print(a.array)

from time import time

t = time()
for i in range(9999999):
    a.update_location(0.01)
    if time()-t>1.0:
        break
print(i,NN,'complexed location')


t = time()
for i in range(9999999):
    a.update_rotation(0.01)
    if time()-t>1.0:
        break
print(i,NN,'rotation')

#142 100000 complexed location
#1619 100000 rotation
#14 1000000 complexed location
#134 1000000 rotation
#huh. masking and get attr kinds are bad!
#=======================================

#SLICING TAKES TIME!
# if x y,z 9times calculation:
#5 1000000 complexed location
#18 1000000 rotation

#... while col.major array took times:
#11 1000000 complexed location
#18 1000000 rotation


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

