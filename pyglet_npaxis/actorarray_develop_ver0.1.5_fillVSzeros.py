import numpy as np

import numba as nb

from time import time

#disable jit. how easy!
#from numba import jit, config
#config.DISABLE_JIT = True
#err! funcwithjit.py_func() instead..

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

#naming rule:
#axis_input_output
#axis means its for np array axis parrelle.

#easy to remove np. but hard to add. so we use np.cos not cos.
#jit, compiled, same speed.
def axis_axisangle_quat(x,y,z, r):
    """Create a new quaternion from a VRML-style rotation
    x,y,z are the axis of rotation
    r is the rotation in radians."""
    x,y,z = utilities.normalise( (x,y,z) )
    np.cos(r/2.0), x*(np.sin(r/2.0)), y*(np.sin(r/2.0)), z*(np.sin(r/2.0))

#all 4x4=16 matrix col.major, for gpuready.
def axis_quat_rotmat(x,y,z,w):
    rotmat = [
    1 - 2*y**2 - 2*z**2,   2*x*y - 2*z*w,   2*x*z + 2*y*w, 0,
    2*x*y + 2*z*w,   1 - 2*x**2 - 2*z**2,   2*y*z - 2*x*w, 0,
    2*x*z - 2*y*w,   2*y*z + 2*x*w,   1 - 2*x**2 - 2*y**2, 0,
    0,0,0,1
    ]
    return rotmat

def axis_xyz_quat(x,y,z):
    """ returns xyzw"""
    yaw = z
    pitch = y
    roll = x
    cy = np.cos(yaw * 0.5)
    sy = np.sin(yaw * 0.5)
    cp = np.cos(pitch * 0.5)
    sp = np.sin(pitch * 0.5)
    cr = np.cos(roll * 0.5)
    sr = np.sin(roll * 0.5)
    
    x = sr * cp * cy - cr * sp * sy
    y = cr * sp * cy + sr * cp * sy
    z = cr * cp * sy - sr * sp * cy
    w = cr * cp * cy + sr * sp * sy
    return [x,y,z,w]


def axis_v1v2_axisangle(v1,v2):
    """v1,v2 -> axis,th
    """
    front = normalize(v1)
    facing = normalize(v2)

    #---qv
    axis = cross(front, facing)#result not unit vector
    axis = normalize(axis)
    #---qs    
    th = acos( dot(front,facing) )
    return axis,th


def axis_xyz_axisangle(x,y,z):
    1
def axis_axisangle_quat(x,y,z):
    axis = normalize(axis)
    x,y,z = axis *sin(th/2)
    w = cos(th/2)
    return x,y,z,w

#def xxxaxis_rotmat_modelmat(rotmat, Tx,Ty,Tz, Sx,Sy,Sz):
#@nb.jit
@nb.jit(nopython=True , parallel = True)
def axis_xyzmat_rotmat(colmat,x,y,z):
    #colmat 16*N massive array. access by index
    # x,y,z means Rx,Ry,Rz. thats all.,not! yaw (Z), pitch (Y), roll (X)
    #https://en.wikipedia.org/wiki/Conversion_between_quaternions_and_Euler_angles
    cx = np.cos(x)
    sx = np.sin(x)
    cy = np.cos(y)
    sy = np.sin(y)
    cz = np.cos(z)
    sz = np.sin(z)

    #NOTE: we cannot return python list type. jit error!
    # rotmat = [
    # cy*cz, -cx*sz+sx*sy*cz, sx*sz+cx*sy*cz, 0,
    # cy*sz, cx*cz+sx*sy*sz, -sx*cz+cx*sy*sz, 0,
    # -sy,   sx*cy,       cx*cy, 0,
    # 0,0,0,1
    # ]

    #it still creates new tuple.
    # colmat = cy*cz, -cx*sz+sx*sy*cz, sx*sz+cx*sy*cz, 0,\
    # cy*sz, cx*cz+sx*sy*sz, -sx*cz+cx*sy*sz, 0,\
    # -sy,   sx*cy,       cx*cy, 0,\
    # 0,0,0,1

    #dimension err
    # print(x.shape)
    # colmat[:] = cy*cz, -cx*sz+sx*sy*cz, sx*sz+cx*sy*cz, 0,\
    # cy*sz, cx*cz+sx*sy*sz, -sx*cz+cx*sy*sz, 0,\
    # -sy,   sx*cy,       cx*cy, 0,\
    # 0,0,0,1

    #finally!

    #1M, py 78ms (of75ms calculation +3ms assign)
    #1M, jit 25ms (of0ms calculation +25ms assign)
    #so we skip assign, of which is 0.

    colmat[0] = cy*cz
    colmat[1] = -cx*sz+sx*sy*cz
    colmat[2] = sx*sz+cx*sy*cz
    #colmat[3] =  0    
    colmat[4] = cy*sz
    colmat[5] = cx*cz+sx*sy*sz
    colmat[6] = -sx*cz+cx*sy*sz
    #colmat[7] = 0     
    colmat[8] = -sy
    colmat[9] = sx*cy
    colmat[10] = cx*cy        
    #colmat[11] = 0

    #colmat[11:15] = 0 #samespeed. this not breaks dimension.
    #colmat[12] = 0
    #colmat[13] = 0
    #colmat[14] = 0
    colmat[15] = 1
    return colmat

    #90ms, compared 80ms. creating in axis_func, not good..
    # rotmat = np.array( (cy*cz,    -cx*sz+sx*sy*cz,    sx*sz+cx*sy*cz,    zs,
    # cy*sz,    cx*cz+sx*sy*sz,    -sx*cz+cx*sy*sz,    zs ,    
    # -sy,    sx*cy,    cx*cy        ,    zs,
    # zs,    zs,    zs,    os) ,dtype='float32')

    #return rotmat

@nb.jit(nopython=True , parallel = True)
def axis_xyz_rot3x3(x,y,z):
    #skip colmat, faster. input requires time.
    # x,y,z means Rx,Ry,Rz. thats all.,not! yaw (Z), pitch (Y), roll (X)
    #https://en.wikipedia.org/wiki/Conversion_between_quaternions_and_Euler_angles
    cx = np.cos(x)
    sx = np.sin(x)
    cy = np.cos(y)
    sy = np.sin(y)
    cz = np.cos(z)
    sz = np.sin(z)

    return cy*cz, -cx*sz+sx*sy*cz, sx*sz+cx*sy*cz,\
    cy*sz, cx*cz+sx*sy*sz, -sx*cz+cx*sy*sz,\
    -sy,   sx*cy,       cx*cy



#this returns f64, since m1=XX new assign.
#1M 25msvs 15ms,, but too dirty.
#@nb.jit(nopython=True , parallel = True)
#def xxxaxis_xyzmat_rotmat(m1,m2,m3,m4,m5,m6,m7,m8,m9,m10,m11,m12,m13,m14,m15,m16, x,y,z):

@nb.jit(nopython=True , parallel = True)
def axis_trs_modelmat(colmat, Tx,Ty,Tz, Rx,Ry,Rz, Sx,Sy,Sz):
    #col major matrix.. for gpu. Rx,Ry,Rz=R,P,Y
    cx = np.cos(Rx)
    sx = np.sin(Rx)
    cy = np.cos(Ry)
    sy = np.sin(Ry)
    cz = np.cos(Rz)
    sz = np.sin(Rz)

    #TUPLE NO allows assign item.. so we integrate in it!
    # rotmat[0] *= Sx
    # rotmat[1] *= Sx
    # rotmat[2] *= Sx
    # rotmat[4] *= Sy
    # rotmat[5] *= Sy
    # rotmat[6] *= Sy
    # rotmat[8] *= Sz
    # rotmat[9] *= Sz
    # rotmat[10] *= Sz

    # rotmat[3] = Tx
    # rotmat[7] = Ty
    # rotmat[11] = Tz

    
    #this also rewrites colmat.
    #NOTE:[3]=Tx but it's col.major.remember. not [ [a,b,c,Tx],..]   
    # colmat =\
    # cy*cz*Sx, -cx*sz+sx*sy*cz*Sx, sx*sz+cx*sy*cz*Sx, Tx,\
    # cy*sz*Sy, cx*cz+sx*sy*sz*Sy, -sx*cz+cx*sy*sz*Sy, Ty,\
    # -sy*Sz,   sx*cy*Sz,       cx*cy*Sz, Tz,\
    # 0,0,0,1
    
    #thisway!
    colmat[0] = cy*cz *Sx
    colmat[1] = -cx*sz+sx*sy*cz *Sx
    colmat[2] = sx*sz+cx*sy*cz *Sx
    colmat[3] =  Tx    
    colmat[4] = cy*sz *Sy
    colmat[5] = cx*cz+sx*sy*sz *Sy
    colmat[6] = -sx*cz+cx*sy*sz *Sy
    colmat[7] = Ty     
    colmat[8] = -sy *Sz
    colmat[9] = sx*cy *Sz
    colmat[10] = cx*cy *Sz
    colmat[11] = Tz

    #colmat[11:15] = 0 #samespeed. this not breaks dimension.
    #colmat[12] = 0
    #colmat[13] = 0
    #colmat[14] = 0
    colmat[15] = 1
    return colmat

#https://llvm.org/docs/LangRef.html#fast-math-flags
#https://numba.pydata.org/numba-doc/dev/user/performance-tips.html
#@nb.jit(nopython=True , parallel = True, fastmath={'reassoc', 'nsz'})# 17ms
#@nb.jit(nopython=True , parallel = True, fastmath=True) #17ms
#fullcore too fast. 17ms is maybe just setuptime, mostof.. specially input values.
@nb.jit(nopython=True , parallel = True) #17ms.yeah.
def axis_scale4x4(colmat, Sx,Sy,Sz):
    #col major matrix.. for gpu. Rx,Ry,Rz=R,P,Y
    #thisway!
    colmat[0] *=Sx
    colmat[1] *=Sx
    colmat[2] *=Sx

    colmat[4] *=Sy
    colmat[5] *=Sy
    colmat[6] *=Sy

    colmat[8] *=Sz
    colmat[9] *=Sz
    colmat[10] *=Sz
    return colmat
@nb.jit(nopython=True , parallel = True) #17ms.yeah.
def axis_rot4x4(colmat, Rx,Ry,Rz):
    #col major matrix.. for gpu. Rx,Ry,Rz=R,P,Y
    cx = np.cos(Rx)
    sx = np.sin(Rx)
    cy = np.cos(Ry)
    sy = np.sin(Ry)
    cz = np.cos(Rz)
    sz = np.sin(Rz)
    #thisway!
    colmat[0] = cy*cz
    colmat[1] = -cx*sz+sx*sy*cz
    colmat[2] = sx*sz+cx*sy*cz

    colmat[4] = cy*sz
    colmat[5] = cx*cz+sx*sy*sz
    colmat[6] = -sx*cz+cx*sy*sz
    
    colmat[8] = -sy
    colmat[9] = sx*cy
    colmat[10] = cx*cy
    return colmat

#@nb.jit(nopython=True , parallel = True) #17ms.yeah.
#@nb.jit(nopython=True , parallel = False) #17ms.yeah.
@nb.jit
def axis_pos4x4(colmat, Tx,Ty,Tz):
    #col major matrix.. for gpu. Rx,Ry,Rz=R,P,Y
    colmat[3] = Tx    
    colmat[7] = Ty     
    colmat[11] = Tz
    return colmat

NN = 1000000
#dummymat = np.zeros(16*NN).reshape(16,NN).astype('float32') #300x slower
dummymat = np.zeros(16*NN, dtype='float32').reshape(16,NN)
x = np.random.rand(NN).astype('float32')
y = np.random.rand(NN).astype('float32')
z = np.random.rand(NN).astype('float32')
#z = np.random.rand(NN,dtype='float32') #cant
print(x)
print(y)
print(z)


# print('=========================================astype speedtest')
# #X300 faster!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# #100k 7.2sec.
# t=time()
# for i in range(100000):
#     zs = np.zeros(NN,dtype='float32')
# print(time()-t,'pdddddddddddddat',NN)

# #1000 2.2sec. 1000!
# t=time()
# for i in range(1000):
#     zs = np.zeros(NN).astype('float32')
# print(time()-t,'aaaaaaaaaaaa',NN)


# print('=========================================reshape speedtest')
# #76ms. as you wish.fine.
# #84ms
# t=time()
# for i in range(100000):
#     dummymat = np.zeros( (16,NN), dtype='float32')
# print(time()-t,'shape tuple',NN)

# #1000 2.2sec. 1000!
# t=time()
# for i in range(100000):
#     dummymat = np.zeros(16*NN, dtype='float32').reshape(16,NN)
# print(time()-t,'after shaping',NN)

# print('=========================================T speedtest')
# #70ms
# #vs 71.4ms. fine. we can easyly do .T.
# t=time()
# for i in range(100000):
#     dummymat = np.zeros( (16,NN), dtype='float32')
# print(time()-t,'normal',NN)
# print(dummymat.shape)

# t=time()
# for i in range(100000):
#     dummymat = np.zeros( (16,NN), dtype='float32').T
# print(time()-t,'T',NN)
# print(dummymat.shape)

# exit()

#we can draw 4x4 1M, really. (forpos 2M numba 250fps. while 1M nojit 60fps
#=================================spedtest
#=rotmat took 78ms .. jit 14ms.
#0.07878923416137695 py_func rotmat 1000000
#0.013962984085083008 numba rotmat 1000000

#=modelmat 120ms. jit 16ms.
#0.11869192123413086 axis_trs_modelmat 1000000
#0.015957117080688477 axis_trs_modelmat 1000000
#modelmat was once 85ms, with list indexing. but cannot numba..

#with seedmat, per-item assign. +10ms of 1M. cant 1M 60fps..
#0.08876276016235352 py_func rotmat 1000000
#0.025444984436035156 numba rotmat 1000000

#not broadcasting 0. means we need seedmat of eyemat.
#0.08776521682739258 py_func rotmat 1000000
#0.02094411849975586 numba rotmat 1000000

#now we skip assign, of value=0. 6/16
#numba super fast calculation. all time came from assign item..
#0.07779240608215332 py_func rotmat 1000000
#0.0 numba rotmat 1000000

#cosremoved
#0.0882720947265625 py_func rotmat 1000000
#0.02094411849975586 numba rotmat 1000000
#ignore np.cos vs cos case. no more!

#creat modelmat by vstack.  80->100 singlecore, 20->45 jit. surely it's slow!
#0.10073065757751465 py_func rotmat 1000000
#0.04587721824645996 numba rotmat 1000000

#16 of inputs.. 1core, as youknow, most of is real calulation.
#----- rotmay xyz 1000000
#0.07982778549194336 py_func rotmat 1000000
#----- rotmay xyz  jit 1000000
#0.01296544075012207 numba rotmat 1000000
#while numba finally so fast.! bot just 2xtime!hahaha. 20ms VS 12ms, with this harsh way?

#92ms slow of rotmat, by zeros, ones. just give them dummymat.
#0.09179019927978516  1M, nojit, xyz_rotmat(zs,os,x,y,z)

#float= 32bit. was before 80,20. now 58,12.
# ----- rotmay xyz 1000000
# 0.05884289741516113 py_func rotmat 1000000
# ----- rotmay xyz  jit 1000000
# 0.011967658996582031 numba rotmat 1000000

#WE need to USE X,Y,Z not XYZ !!!!!! ..when single core specially.
#x = static_getitem(value=rpos, index=0, index_var=$const4.1, fn=<built-in function getitem>)  :: array(float32, 1d, C)
#means, if a 3Darray given, it creates 3 of new 1Darray. bia getitem function.
# ----- rotmay xyz 1000000
# 0.05983996391296387 py_func rotmat 1000000
# ----- rotmay xyz  jit 1000000
# 0.012965202331542969 numba rotmat 1000000
# float32
# ----- rotmay rpos 1000000
# 0.07081055641174316 py_func rotmat 1000000
# ----- rotmay rpos  jit 1000000
#0.011967897415161133 numba rotmat 1000000
#10ms 18% slow at single core!

#------------------------------------------ver0.1
#highspeed : 60ms /13ms(jit) of 1M, rotmat.
#83ms / 26ms of modelmat.

#4x4 reasonable for atleast R matrix.
#if you want just posxyz, change shader, using x,y,z, not4x4!


#-----------------------------------ver 0.1.4
# dummy rotmat 57/13
# 3x3 rotmat  75/10

# trs modelmat 82/28
# tr posrotmat 70/18  skip SxSySz. this is enough speed.
# 3x3 posrotmat 75+/13ms jit ..but too complexed. even 30% speedup..
#0.07480072975158691 py_func rotmat 1000000 ..samespeed?
#0.06682133674621582 py_func rotmat 1000000 no assign. assign of 1M is 1ms. x12, +12ms.
# rotmat by xyz only test.(not giving dummy)
# numba input slow, so assign outside is faster.
#but not in singlecore. so keep the code as simple.


# ver0.1.5----------------- model= T R S
# ----- rotmay xyz 1000000
# 0.06186199188232422 py_func rotmat 1000000
# ----- rotmay xyz  jit 1000000
# 0.032883405685424805 numba rotmat 1000000
# without scale=====
# ----- rotmay xyz 1000000
# 0.07081055641174316 py_func rotmat 1000000
# ----- rotmay xyz  jit 1000000
# 0.01795220375061035 numba rotmat 1000000

#NOW modelmat 62/33
#now posrot  70/18
#vs previous:
#trs modelmat 82/28
#tr posrotmat 70/18
#3x3 posrotmat 75+/13ms

#--------------when modelmat = dummy.copy()
# ver0.1.5-----------------
# ----- axis_scale4x4 1000000
# 0.07283353805541992 py_func triples 1000000
# ----- axis_scale4x4 xyz  jit 1000000
# 0.04288625717163086 numba triples 1000000
# ========without scale=====
# ----- axis_rot4x4  1000000
# 0.08179259300231934 py_func axis_rot4x4 1000000
# ----- axis_rot4x4  jit 1000000
# 0.026928186416625977 numba axis_rot4x4 1000000

#--------------when dommy = zeros(). 1M copy requires 10ms while zeros 1ms.
# ver0.1.5-----------------
# ----- axis_scale4x4 1000000
# 0.06186199188232422 py_func triples 1000000
# ----- axis_scale4x4 xyz  jit 1000000
# 0.03487849235534668 numba triples 1000000
# ========without scale=====
# ----- axis_rot4x4  1000000
# 0.07579755783081055 py_func axis_rot4x4 1000000
# ----- axis_rot4x4  jit 1000000
# 0.019959449768066406 numba axis_rot4x4 1000000

#===============================rotmat by xyz 0.1.5 post confirm ver.
# modelmat 62/35 --with reset dummy.
# posrot 75/20
#vs previous:
#trs modelmat 82/28
#tr posrotmat 70/18
#3x3 posrotmat 75+/13ms

#---------------0.1.5 confirm ver.
# test3, 63-> 72 found, (see without sleep.) maybe internal post processing??

#model        trsmdl 82/28 pos rpos scale->
#model        triple 63/33 pos->rot->scale->

#withoutscale tr rot 70/18
#withoutscale 3x3    75/13 (rotmat 10ms + assign 1ms*3)
#withoutscale triple 60/20

#rotmat        3x3   75/10

#----modelmat
#dummy 9input 66/33 final report.
#model triple 63/33 pos->rot->scale->. same speed.yeah.
#***we have advantage of easy-to-see

#----without scale
#withoutscale tr rot 70/18 --seems we need sleep(1) before use..
#withoutscale 3x3    75/13 (rotmat 10ms + assign 1ms*3)
#withoutscale triple 60/20
# those may not contain dummy reset. so .. not bad, but triple so fast!
#anyway, it's very 30~ difference. we use triples. convient, not slow, glm logic.
#anyway we need blank dummymat, haha! i think better set to 0..


#-----------------copy vs zeros spd test
# dummy = np.zeros(16*NN, dtype='float32').reshape(16,NN)
# t=time()
# for i in range(10):
#     modelmat = dummy.copy()
# print(time()-t,'1m crate',NN)

# t=time()
# for i in range(1000):# it's super fast.
#     modelmat = np.zeros(16*NN, dtype='float32').reshape(16,NN)
# print(time()-t,'1m crate',NN)
# exit()

#0.11170172691345215 1m crate 1000000
#0.001994609832763672 1m crate 1000000
#huh.. not use copy as possible..
#---------------------------------

zs = np.zeros(NN).astype('float32')
os = np.ones(len(x),dtype='float32')




print('ver0.1.5-----------------')
print('===test1')
dummy = np.zeros(16*NN, dtype='float32').reshape(16,NN)
print('----- axis_scale4x4',NN)
t=time()
modelmat = np.zeros(16*NN, dtype='float32').reshape(16,NN)
modelmat = axis_scale4x4.py_func(modelmat, os,os,os)
modelmat = axis_rot4x4.py_func(modelmat, x,y,z)
modelmat = axis_pos4x4.py_func(modelmat, os,zs,zs)
#print(rotmat)
print(time()-t,'py_func triples',NN)

t=time()
modelmat = np.zeros(16*NN, dtype='float32').reshape(16,NN)
#modelmat = axis_scale4x4.py_func(modelmat, os,os,os)
modelmat = axis_rot4x4.py_func(modelmat, x,y,z)
modelmat = axis_pos4x4.py_func(modelmat, os,zs,zs)
#print(rotmat)
print(time()-t,'py_func without scale',NN)



#2ms for fill 0. quite slow!!
t = time()
for i in range(1000): #2.1274900436401367
    modelmat.fill(0)
print(time()-t)
print(modelmat)
print(modelmat.shape)


#2ms for fill 0. quite slow!!
t = time()
for i in range(1000): #0.007962226867675781
    dummy = np.zeros(16*NN, dtype='float32').reshape(16,NN)
print(time()-t)
print(modelmat)
print(modelmat.shape)

exit()

print('===test2')
print('----- axis_scale4x4 xyz  jit',NN)
modelmat = np.zeros(16*NN, dtype='float32').reshape(16,NN)
modelmat = axis_scale4x4(modelmat, os,os,os)
modelmat = axis_rot4x4(modelmat, x,y,z)
modelmat = axis_pos4x4(modelmat, os,zs,zs)
t=time()
modelmat = np.zeros(16*NN, dtype='float32').reshape(16,NN)
modelmat = axis_scale4x4(modelmat, os,os,os)
modelmat = axis_rot4x4(modelmat, x,y,z)
modelmat = axis_pos4x4(modelmat, os,zs,zs)
#print(rotmat)
#print(rotmat.shape)
print(time()-t,'numba triples',NN)

#cc=axis_xyzmat_rotmat.inspect_types()
#print(cc) #you wanna see jit inside?


modelmat = np.zeros(16*NN, dtype='float32').reshape(16,NN)
#modelmat = axis_scale4x4(modelmat, os,os,os)
modelmat = axis_rot4x4(modelmat, x,y,z)
modelmat = axis_pos4x4(modelmat, os,zs,zs)
t=time()
modelmat = np.zeros(16*NN, dtype='float32').reshape(16,NN)
#modelmat = axis_scale4x4(modelmat, os,os,os)
modelmat = axis_rot4x4(modelmat, x,y,z)
modelmat = axis_pos4x4(modelmat, os,zs,zs)
#print(rotmat)
#print(rotmat.shape)
print(time()-t,'numba without scale',NN)

from time import sleep
sleep(5.3)
#===
print('===test3')
t=time()
modelmat = np.zeros(16*NN, dtype='float32').reshape(16,NN)
#modelmat = axis_scale4x4.py_func(modelmat, os,os,os)
modelmat = axis_rot4x4.py_func(modelmat, x,y,z)
modelmat = axis_pos4x4.py_func(modelmat, os,zs,zs)
print(time()-t,'py_func withoutscale 79ms not 59ms..',NN)

t=time()
modelmat = np.zeros(16*NN, dtype='float32').reshape(16,NN)
modelmat = axis_scale4x4.py_func(modelmat, os,os,os)
modelmat = axis_rot4x4.py_func(modelmat, x,y,z)
modelmat = axis_pos4x4.py_func(modelmat, os,zs,zs)
print(time()-t,'py_func triples',NN)



exit()



#=========== it's too, too bad to look, dont' do this. even 30% speedup of:
# 18vs13 withoutscale jit.  but  slow at 1core: 60vs70. so we not use it 1core first rule.
#even this is the onlyway to draw 1M 60fps.. not 700k..

#-------------------=ver0.1.4 minumal input
dummymat = np.zeros(16*NN, dtype='float32').reshape(16,NN)
print('----- axis_xyz_rot3x3 xyz',NN)
t=time()
rot3x3 = axis_xyz_rot3x3.py_func( x,y,z) #0.06682133674621582 this calc takes most!
dummymat[0],dummymat[1],dummymat[2],\
dummymat[3],dummymat[4],dummymat[5],\
dummymat[6],dummymat[7],dummymat[8] = rot3x3
# dummymat[3] = 0
# dummymat[7] = 0
# dummymat[11] = 1 #0.07480072975158691 py_func rotmat 1000000
#print(rotmat)
print(time()-t,'py_func rotmat',NN)


print('----- axis_xyz_rot3x3 xyz  jit',NN)
rot3x3 = axis_xyz_rot3x3( x,y,z)
dummymat[0],dummymat[1],dummymat[2],\
dummymat[3],dummymat[4],dummymat[5],\
dummymat[6],dummymat[7],dummymat[8] = rot3x3

t=time()
rot3x3 = axis_xyz_rot3x3( x,y,z)
dummymat[0],dummymat[1],dummymat[2],\
dummymat[3],dummymat[4],dummymat[5],\
dummymat[6],dummymat[7],dummymat[8] = rot3x3
print(time()-t,'numba axis_xyz_rot3x3',NN)

t=time()
rot3x3 = axis_xyz_rot3x3( x,y,z)
dummymat[0],dummymat[1],dummymat[2],\
dummymat[4],dummymat[5],dummymat[6],\
dummymat[7],dummymat[8],dummymat[9] = rot3x3
#dummymat[3] = zs faster than 0, outside of numba.
dummymat[3] = 0
dummymat[7] = 0
dummymat[11] = 1
print(time()-t,'TX numba axis_xyz_pos4x4',NN)

modelmat = axis_tr_posrotmat(dummymat, 0,0,0,x,y,z)#pre-compile
modelmat = axis_tr_posrotmat(dummymat, zs,zs,zs,x,y,z)
print('----- axis_tr_posrotmat, jit',NN)
t=time()
#modelmat = axis_trs_posrotmat(0,0,0,x,y,z,1,1,1)
modelmat = axis_tr_posrotmat(dummymat, zs,zs,zs,x,y,z)
print(time()-t,'axis_tr_posrotmat', NN)


#exit()





#===============================modelmat by tttrrrsss
print('======= MODELMAT')
zs = np.zeros(1000000).astype('float32')
os = np.ones(1000000).astype('float32')

print('----- modelmat trs,',NN)
t=time()
modelmat = axis_trs_modelmat.py_func(dummymat, zs,zs,zs,x,y,z,os,os,os)
#modelmat = axis_trs_modelmat.py_func(0,0,0,x,y,z,1,1,1)
#print(modelmat)
print(time()-t,'axis_trs_modelmat', NN)


modelmat = axis_trs_modelmat(dummymat, 0,0,0,x,y,z,1,1,1)#pre-compile
modelmat = axis_trs_modelmat(dummymat, zs,zs,zs,x,y,z,os,os,os)
print('----- modelmat trs, jit',NN)
t=time()
#modelmat = axis_trs_modelmat(0,0,0,x,y,z,1,1,1)
modelmat = axis_trs_modelmat(dummymat, zs,zs,zs,x,y,z,os,os,os)
print(time()-t,'axis_trs_modelmat', NN)

#----modelmat without dummymat
print(type(modelmat)) #<class 'tuple'>
#print(modelmat)
print(modelmat.shape)

#]), array([0., 0., 0., ..., 0., 0., 0.], dtype=float32), 0, 0, 0, 1)
#ugly shape!



#==================================step3, without Rx,Ry,Rz. skip 9x multiply and 3 inputs!
print('----- modelmat trs,',NN)
t=time()
modelmat = axis_tr_posrotmat.py_func(dummymat, zs,zs,zs,x,y,z)
#modelmat = axis_trs_modelmat.py_func(0,0,0,x,y,z,1,1,1)
#print(modelmat)
print(time()-t,'axis_tr_posrotmat', NN)


modelmat = axis_tr_posrotmat(dummymat, 0,0,0,x,y,z)#pre-compile
modelmat = axis_tr_posrotmat(dummymat, zs,zs,zs,x,y,z)
print('----- axis_tr_posrotmat, jit',NN)
t=time()
#modelmat = axis_trs_posrotmat(0,0,0,x,y,z,1,1,1)
modelmat = axis_tr_posrotmat(dummymat, zs,zs,zs,x,y,z)
print(time()-t,'axis_tr_posrotmat', NN)



exit()

#0.11981916427612305 axis_trs_modelmat 1000000 zs,zs,zs
#0.1156914234161377 axis_trs_modelmat 1000000 0,0,0
#you can use 0 and 1 instead of zeros. yeah.
#rotmat = axis_trs_modelmat(0,0,0,x,y,z,1,1,1)



quat = axis_xyz_quat(x,y,z)
#print(quat,'quat')
x,y,z,w = quat
rot2 = axis_quat_rotmat(x,y,z,w)
#print(rot2)

exit()

def axis_xyz_front(x,y,z):
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

#@nb.jit(nopython=True , parallel = True)
def ufunc_posspeed(pos,speed,acc,dt):
    speed += acc*dt
    pos += speed*dt
    return pos,speed
#pos rpos 65, 255(jit)

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


# col.major x,y,z we saw 220fps  100k. jit 10000fps.
# row.major x1,x2,x3 we can 1400 same,
# 1M pos 130fps. pos+rot 60fps. without jit. since no slice maybe.
# 2M jit 110fps. not that fast but can handle..

#and now, 1M modelmat took 80ms. wow. 12.5fps. whatever! it's not 100k!

#below too complex detail and messy data
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

