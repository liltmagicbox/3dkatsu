import numpy as np

import numba as nb

#https://docs.scipy.org/doc/numpy-1.15.1/reference/ufuncs.html
#deg2rad arccos...


#================vector, quat
def normalise( vectors ):
    """Get normalised versions of the vectors.
    
    vectors -- sequence object with 1 or more
        3-item vector values.
    
    returns a float array with x 3-element vectors,
    where x is the number of 3-element vectors in "vectors"

    Will raise ZeroDivisionError if there are 0-magnitude
    vectors in the set.
    """
    vectors = asarray( vectors, _aformat(vectors))
    vectors = reshape( vectors, (-1,3)) # Numpy 23.7 and 64-bit machines fail here, upgrade to 23.8
    mags = reshape( magnitude( vectors ), (-1, 1))
    mags = where( mags, mags, 1.0)
    return divide_safe( vectors, mags)


from numpy import sin,cos

def ufunc_quatmul(x1,y1,z1,w1, x2,y2,z2,w2):
    return x,y,z,w

def axis_aaquat(x,y,z, r):
    """Create a new quaternion from a VRML-style rotation
    x,y,z are the axis of rotation
    r is the rotation in radians."""
    x,y,z = utilities.normalise( (x,y,z) )
    cos(r/2.0), x*(sin(r/2.0)), y*(sin(r/2.0)), z*(sin(r/2.0))
    

def axis_quatrotmat(x,y,z,w):
    rotmat = [
    1 - 2*y**2 - 2*z**2,   2*x*y - 2*z*w,   2*x*z + 2*y*w, 0,
    2*x*y + 2*z*w,   1 - 2*x**2 - 2*z**2,   2*y*z - 2*x*w, 0,
    2*x*z - 2*y*w,   2*y*z + 2*x*w,   1 - 2*x**2 - 2*y**2, 0,
    0,0,0,1
    ]
    return rotmat

def axis_xyzquat(x,y,z):
    """ returns xyzw"""
    yaw = z
    pitch = y
    roll = x
    cy = cos(yaw * 0.5)
    sy = sin(yaw * 0.5)
    cp = cos(pitch * 0.5)
    sp = sin(pitch * 0.5)
    cr = cos(roll * 0.5)
    sr = sin(roll * 0.5)
    
    x = sr * cp * cy - cr * sp * sy
    y = cr * sp * cy + sr * cp * sy
    z = cr * cp * sy - sr * sp * cy
    w = cr * cp * cy + sr * sp * sy
    return [x,y,z,w]

@nb.jit(nopython=True , parallel = True)
def cosspd(x,y):
    #return np.cos(x)*np.sin(y)
    return cos(x)*sin(y)
    #return x*y
x = np.random.rand(10000000)
y = np.random.rand(10000000)
from time import time

cosspd(x,y)
t = time()
cosspd(x,y)
print(time()-t)
#0.438385009765625 np.cos
#0.4290180206298828 cos
#..was by jit compile.
#print(cosspd.inspect_types())

#0.001993894577026367 x*y
#0.001994609832763672 cosx*siny
#0.001994609832763672 np.cosx *np.cosy
#0.015957355499267578 10M cos
#0.015957355499267578 10M npcos
#jit compile 420ms, np.cos +10ms.
#after compile, nomore load np module. fastest speed.

exit()
def axis_xyzrotmat(x,y,z): 
    #https://en.wikipedia.org/wiki/Conversion_between_quaternions_and_Euler_angles
    # x,y,z means Rx,Ry,Rz. thats all.,not! yaw (Z), pitch (Y), roll (X)
    cx = cos(x)
    sx = sin(x)
    cy = cos(y)
    sy = sin(y)
    cz = cos(z)
    sz = sin(z)

    rotmat = [
    cy*cz, -cx*sz+sx*sy*cz, sx*sz+cx*sy*cz, 0,
    cy*sz, cx*cz+sx*sy*sz, -sx*cz+cx*sy*sz, 0,
    -sy,   sx*cy,       cx*cy, 0,
    0,0,0,1
    ]
    return rotmat

def axis_rotmatmodelmat(pos,rotmat,scale):
    #col major matrix.. for gpu.
    rotmat[0] *= scalex
    rotmat[1] *= scalex
    rotmat[2] *= scalex
    rotmat[4] *= scaley
    rotmat[5] *= scaley
    rotmat[6] *= scaley
    rotmat[8] *= scalez
    rotmat[9] *= scalez
    rotmat[10] *= scalez

    rotmat[3] = posx
    rotmat[7] = posy
    rotmat[11] = posz
    return rotmat


def axis_xyzfront(x,y,z):
    321

# def ufunc_modelmat(qx,qy,qz,qw):
#     mat = [
#     1 - 2*qy**2 - 2*qz**2,   2*qx*qy - 2*qz*qw,   2*qx*qz + 2*qy*qw, 0,
#     2*qx*qy + 2*qz*qw,   1 - 2*qx**2 - 2*qz**2,   2*qy*qz - 2*qx*qw, 0,
#     2*qx*qz - 2*qy*qw,   2*qy*qz + 2*qx*qw,   1 - 2*qx**2 - 2*qy**2, 0,
#     0,0,0,                                                           1
#     ]
#     return mat
    #return np.array(mat,dtype='float32')

#go simple way! pos is rotmat+ tx,tx,tz. thats all. we dont need 4x4 mat mul.
#def ufunc_rotmat(qx,qy,qz,qw):
#def ufunc_transmat(pos):

#ufunc=================================\
#naming via return type.  ..can assume what input should be.
#for not numba, uncomment @nb.jit manually.
@nb.jit(nopython=True , parallel = True)
def ufunc_pos(pos,speed,dt):
    #hope we not use it..
    #we needit, since slicing takes littletime, but giving value to ufunc takes time.!
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
        attributes = 30
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

        #----post attr value setting. this,,slice slower, since row major grabs all continueous memory.
        self.array[self.posupdate] = 1 #1 faster than 1.0
        self.array[self.rposupdate] = 0
        #self.intarray[self.posupdate] = 1 #float faster than int

        #self.scale = 20
        self.scalex = 21
        self.scaley = 22
        self.scalez = 23
        self.scale = np.index_exp[21:24]

        #finally quat!
        self.quatx = 24
        self.quaty = 25
        self.quatz = 26
        self.quatw = 27
        self.quat = np.index_exp[24:28]

        #front. c++ style oop. update with your intention.
        self.frontx = 31
        self.fronty = 32
        self.frontz = 33
        self.front = np.index_exp[31:34]
        self.upx = 34
        self.upy = 35
        self.upz = 36
        self.up = np.index_exp[34:37]
        self.rightx = 37
        self.righty = 38
        self.rightz = 39
        self.right = np.index_exp[37:40]
        


    def update(self,dt):
        self.update_location(dt)
        self.update_rotation(dt)

    def update_location(self,dt):
        pos = self.array[self.pos]
        speed = self.array[self.speed]
        acc = self.array[self.acc]
        pos,speed = ufunc_posspeed(pos,speed,acc,dt)
        #pos = ufunc_pos(pos,speed,dt)        

    #@profile
    def update_rotation(self,dt):
        pos = self.array[self.rpos]
        speed = self.array[self.rspeed]
        acc = self.array[self.racc]        
        pos,speed = ufunc_posspeed(pos,speed,acc,dt)
        #pos = ufunc_pos(pos,speed,dt)

    def calc_quat(self):
        pos = self.array[self.pos]
        rot = self.array[self.rpos]
        scale = self.array[self.scale]
        self.array[self.quat] = ufunc_quat(pos,rot,scale) #input 3,3,1. output 4.

    def calc_modelmat(self):
        quatx = self.array[self.quatx]
        quaty = self.array[self.quaty]
        quatz = self.array[self.quatz]
        quatw = self.array[self.quatw]        
        self.gpumodelmat = ufunc_modelmat(quatx,quaty,quatz,quatw) #input 4 output 16..of row.


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
# 3x for .. rom maxsleed,already..

#-------------------------------------------------------------------
# we have past dta: 100k, 200, 10000(jit) pos only. with col.major.
# now with rowmajor, jit,
# 1M, 1400 pos only. with row major.
# 1M, 241  pos+rot+acc. 4x+ slower.

#row major already fast. numba slow x.
# 10M 80fps pos only, noacc, norot (1M 1400fps)
# 2M 110fps pos+rot with acc. x4 slow. (1M 241fps)

# since 2x pos+rot calculation, 100k, 746 4661numba  ..row fastet 4x , when single core.
# 62 / 210 numba 3X. ..maybe memory max..

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

