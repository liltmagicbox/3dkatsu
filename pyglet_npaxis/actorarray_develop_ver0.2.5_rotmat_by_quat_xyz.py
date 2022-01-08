import numpy as np

import numba as nb

from time import time, sleep


#since xyz rot, z up.. ..not thatmuch.

#naming rule:
#axis_input_output
#axis means its for np array axis parrelle.

#from numpy import sin,cos
#easy to remove np. but hard to add. so we use np.cos not cos.
#jit, compiled, same speed.

#jit in jit ok, as it know types. all compiled.

#vector rotated by quat result is not normalized.







#----------------------------------- model matrix



def axis_quat_rotmat(w,x,y,z):
    N = len(x)
    rotmat = np.zeros(16*N, dtype='float32').reshape(16,N)

    rotmat[0] = 1 - 2*y**2 - 2*z**2
    rotmat[1] = 2*x*y - 2*z*w
    rotmat[2] = 2*x*z + 2*y*w
    #rotmat[3] =  0    
    rotmat[4] = 2*x*y + 2*z*w
    rotmat[5] = 1 - 2*x**2 - 2*z**2
    rotmat[6] = 2*y*z - 2*x*w
    #rotmat[7] = 0
    rotmat[8] = 2*x*z - 2*y*w
    rotmat[9] = 2*y*z + 2*x*w
    rotmat[10] = 1 - 2*x**2 - 2*y**2
    #rotmat[11] = 0
    
    #rotmat[12] = 0
    #rotmat[13] = 0
    #rotmat[14] = 0
    rotmat[15] = 1
    return rotmat

NN = 3
x = np.random.rand(NN).astype('float32')
y = np.random.rand(NN).astype('float32')
z = np.random.rand(NN).astype('float32')
rotmat = axis_quat_rotmat(x,x,y,z)
print(rotmat)
print('booom')
exit(0)

@nb.jit(nopython=True , parallel = True)
def axis_xyz_rotmat(x,y,z):
    N = len(x)
    rotmat = np.zeros(16*N, dtype='float32').reshape(16,N)
    cx = np.cos(x)
    sx = np.sin(x)
    cy = np.cos(y)
    sy = np.sin(y)
    cz = np.cos(z)
    sz = np.sin(z)

    rotmat[0] = cy*cz
    rotmat[1] = -cx*sz+sx*sy*cz
    rotmat[2] = sx*sz+cx*sy*cz
    #rotmat[3] =  0    
    rotmat[4] = cy*sz
    rotmat[5] = cx*cz+sx*sy*sz
    rotmat[6] = -sx*cz+cx*sy*sz
    #rotmat[7] = 0
    rotmat[8] = -sy
    rotmat[9] = sx*cy
    rotmat[10] = cx*cy        
    #rotmat[11] = 0
    
    #rotmat[12] = 0
    #rotmat[13] = 0
    #rotmat[14] = 0
    rotmat[15] = 1
    return rotmat



#this returns tuple... so another name-group?.. no!yet.
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

#maybe it similler to lookat..
#its not for jit.  i did, and 24ms slower compared original 16ms.
def axis_Nxyzxyz_posrotmat(N, Tx,Ty,Tz, x,y,z):
    posrot = np.zeros(16*N, dtype='float32').reshape(16,N)
    posrot[15]=1
    rot3x3 = axis_xyz_rot3x3(x,y,z)
    posrot[0],posrot[1],posrot[2],\
    posrot[4],posrot[5],posrot[6],\
    posrot[8],posrot[9],posrot[10] = rot3x3
    posrot[3] =Tx
    posrot[7] =Ty
    posrot[11]=Tz
    return posrot


# those requires colmat
# because m=TRS, eachtime creating zeros inside of.. is terrorble.

@nb.jit(nopython=True , parallel = True)
def axis_matxyz_scalemat(colmat, Sx,Sy,Sz):
    """ use axis_Nxyzxyz_posrotmat
    if you don't need scale. 20->14ms at jit. 1core but do M=TRS.
    """
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

@nb.jit(nopython=True , parallel = True)
def axis_matxyz_rotmat(colmat, Rx,Ry,Rz):
    """ colmat = zeros(16,N).float32.  colmat[15]=1.
    """

    #col major matrix.. for gpu. Rx,Ry,Rz=R,P,Y
    cx = np.cos(Rx)
    sx = np.sin(Rx)
    cy = np.cos(Ry)
    sy = np.sin(Ry)
    cz = np.cos(Rz)
    sz = np.sin(Rz)

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

@nb.jit(nopython=True , parallel = False)#its too simple, cant compile multicore..
def axis_matxyz_posmat(colmat, Tx,Ty,Tz):
    colmat[3] = Tx    
    colmat[7] = Ty     
    colmat[11] = Tz
    return colmat





#----------------------------------- model matrix






#----------------------------------- quat

#xyz to quat
#xyz to vector --fpscam was, but seems to onlyway: rot(rot(rot))..
#vector->quat is sosimple.
#quat->vector inverse..?

@nb.jit(nopython=True , parallel = False)
def axis_xyz_quat(x,y,z):
    """returns w,x,y,z
    """
    #(yaw, pitch, roll) // yaw (Z), pitch (Y), roll (X)
    #https://en.wikipedia.org/wiki/Conversion_between_quaternions_and_Euler_angles
    #Euler angles to quaternion conversion
    cy = np.cos(z * 0.5)
    sy = np.sin(z * 0.5)
    cp = np.cos(y * 0.5)
    sp = np.sin(y * 0.5)
    cr = np.cos(x * 0.5)
    sr = np.sin(x * 0.5)

    w = cr * cp * cy + sr * sp * sy
    x = sr * cp * cy - cr * sp * sy
    y = cr * sp * cy + sr * cp * sy
    z = cr * cp * sy - sr * sp * cy
    return w,x,y,z




#https://personal.utdallas.edu/~sxb027100/dock/quaternion.html
@nb.jit(nopython=True , parallel = False)
def axis_quat_mul(w1,x1,y1,z1, w2,x2,y2,z2):
    w = w1*w2 - x1*x2 - y1*y2 - z1*z2
    x = w1*x2 + x1*w2 + y1*z2 - z1*y2
    y = w1*y2 - x1*z2 + y1*w2 + z1*x2
    z = w1*z2 + x1*y2 - y1*x2 + z1*w2
    return w,x,y,z

def axis_quat_rev(w,x,y,z):
    #conjugate means ..opposite kinds of. + >> -
    return w,-x,-y,-z


#----------------------------------- quat






#----------------------------------- front kinds

#======================front 1,0,0 to rotate by quat. works great!
@nb.jit(nopython=True , parallel = False)
def axis_vecquat_rotate_qpq(x,y,z, qw,qx,qy,qz):
    """ to p' = q*p*qr  / p rotated by quat. but we have 30% faster way.
    """
    pw,px,py,pz = 0,x,y,z #vector p(0,x,y,z) .. 0 but may ok..
    #qw qx qy qz quat
    #rw,rx,ry,rz = axis_quat_rev(qw,qx,qy,qz) #rev of quat
    rw,rx,ry,rz = qw,-qx,-qy,-qz

    tw,tx,ty,tz = axis_quat_mul(pw,px,py,pz, rw,rx,ry,rz) # p*qr
    pr = axis_quat_mul(qw,qx,qy,qz, tw,tx,ty,tz ) #q*tmp
    return pr

@nb.jit(nopython=True , parallel = False)
def axis_vec_cross(x1,y1,z1, x2,y2,z2):
    x= y1*z2-z1*y2
    y=-(x1*z2-z1*x2)
    z= x1*y2-y1*x2
    return x,y,z

@nb.jit(nopython=True , parallel = False)
def axis_vec_normalize(x,y,z):
    #one element is ambiguous. Use a.any() or a.all()
    #if 0==x==y==z:#faster check than x=y=z=0
        #return 0,0,0
    norm = (x**2+y**2+z**2)**0.5
    return x/norm,y/norm,z/norm#may return nan, but ok. fastway!

@nb.jit(nopython=True , parallel = False)
def axis_vecquat_rotate(x,y,z, qw,qx,qy,qz):
    """return not normalized.
    https://en.wikipedia.org/wiki/Conversion_between_quaternions_and_Euler_angles
    """
    # V = target_vector
    # qv,qw
    # v_tmp = cross( qv, V )
    # v_rotated =  V + qw* v_tmp + qv * v_tmp
    
    tx,ty,tz = axis_vec_cross( qx*2,qy*2,qz*2, x,y,z )
    #v + qw*tv +qv*tv
    rx = x + qw*tx +qx*tx
    ry = y + qw*ty +qy*ty
    rz = z + qw*tz +qz*tz
    return rx,ry,rz


@nb.jit(nopython=True , parallel = False)
def axis_quat_front(qw,qx,qy,qz):
    x=1
    y=0
    z=0
    tx,ty,tz = axis_vec_cross( qx*2,qy*2,qz*2, x,y,z )
    #v + qw*tv +qv*tv
    rx = x + qw*tx +qx*tx
    ry = y + qw*ty +qy*ty
    rz = z + qw*tz +qz*tz
    return axis_vec_normalize(rx,ry,rz)
#1Mspd test
# 0.04986882209777832
#----while of pure py. 2xspd! means it's so cpu-hard.
# 0.08377242088317871

#----------------------------------- front kinds



#--------------------------------------------axis-angle
# axis-angle via v1-v2.   aa->quat
# aa is most likely 'the rotation'. i want actor.rotate(axis,angle) kinds.. not by quat.
# actor.rotate_xyz actor.xyzrotate ...

#vec we can assume need 2of it.
def axis_vec_axisangle(x1,y1,z1, x2,y2,z2):
    """v1,v2 -> axis,r

    1 an,bn = normalize
    2 angle = arccos(dot(an,bn))
    3 cross(a,b) --not an,bn since axis->quat normalizes.
    
    from vectorutilites.py openglcontext
    an,bn = normalise( (a,b) )
    angle = arccos(dot(an,bn))
    x,y,z = crossProduct( a, b )[0]
    if allclose( (x,y,z), 0.0):
        y = 1.0
    return (x,y,z,angle)

    """
    nx1,ny1,nz1 = axis_vec_normalize(x1,y1,z1)
    front = normalize(v1)
    facing = normalize(v2)

    #---qv
    axis = cross(front, facing)#result not unit vector
    axis = normalize(axis)
    #---qs    
    r = acos( dot(front,facing) )
    return axis,r

def axis_xyz_axisangle(x,y,z): # wehave xyz quat xyzrotmat
    1

def axis_axisangle_quat(x,y,z,r):
    """x,y,z, radians to quat"""
    x,y,z = axis_vec_normalize(x,y,z)
    w = np.cos(r/2)
    sinhalf = np.sin(r/2)
    x = x * sinhalf
    return x,y,z,w



#the place where already axis_xyz_quat was..rip.




#--------------------------------------------axis-angle










exit()


#------------------------------------actorarray
#------------------------------------actorarray

#seems actually just axis_func..
#def ufunc_posspeed(pos,speed,acc,dt): is the prince with no nation..
#naming via return type.  ..can assume what input should be.
@nb.jit(nopython=True , parallel = True)

def axis_pos(pos,speed,dt):
    #hope we not use it..
    #we needit, since slicing takes littletime, but giving value to ufunc takes time.!
    pos += speed*dt
    return pos

@nb.jit(nopython=True , parallel = True)
def axis_posspeed(pos,speed,acc,dt):
    speed += acc*dt
    pos += speed*dt
    return pos,speed


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
        pos,speed = ufunc_posspeed#c_posspeed(pos,speed,acc,dt)
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


#===================tips and testdata. remained.
#test data deleted ver m.n.0 of m.n.b.


#disable jit. how easy!
#from numba import jit, config
#config.DISABLE_JIT = True
#err! funcwithjit.py_func() instead..


#https://docs.scipy.org/doc/numpy-1.15.1/reference/ufuncs.html
#deg2rad arccos...


#https://llvm.org/docs/LangRef.html#fast-math-flags
#https://numba.pydata.org/numba-doc/dev/user/performance-tips.html
#@nb.jit(nopython=True , parallel = True, fastmath={'reassoc', 'nsz'})# 17ms
#but normally fullcore too fast. we dont needit


#dummymat = np.zeros(16*NN).reshape(16,NN).astype('float32') #300x slower
#dummymat = np.zeros(16*NN, dtype='float32').reshape(16,NN)



#https://stackoverflow.com/questions/53947836/numba-how-to-turn-on-off-just-in-time-compilation-programmatically-setting-num
#from numba import jit, config
#config.DISABLE_JIT = True
#not working

#http://numba.pydata.org/numba-doc/0.34.0/reference/envvars.html#envvar-NUMBA_DISABLE_JIT
#NUMBA_DISABLE_JIT

#https://stackoverflow.com/questions/57282101/flag-to-enable-disable-numba-jit-compilation
#https://numba.pydata.org/numba-doc/dev/reference/envvars.html
#pip install pyyaml
#fname = ".numba_config.yaml"
#within the yaml file, put the key "DISABLE_JIT" equal to the value you wish (true/false).
#UserWarning: A Numba config file is found but YAML parsing capabilities appear 
#to be missing. To use this feature please install `pyyaml`. e.g. `conda install pyyaml`.
#finally itworks
#DISABLE_JIT : 1
#NUMBA_DISABLE_JIT : 1



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

#modelmat = np.zeros(16*NN, dtype='float32').reshape(16,NN) #? i moved it from below
# #2ms for fill 0. quite slow!!
# t = time()
# for i in range(1000): #2.1274900436401367
#     modelmat.fill(0)
# print(time()-t)
# print(modelmat)
# print(modelmat.shape)


# #2ms for fill 0. quite slow!!
# t = time()
# for i in range(1000): #0.007962226867675781
#     dummy = np.zeros(16*NN, dtype='float32').reshape(16,NN)
# print(time()-t)
# print(modelmat)
# print(modelmat.shape)

# exit()











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

