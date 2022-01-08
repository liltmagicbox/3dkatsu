import numpy as np
from numpy import array, eye
from numpy import radians, sin,cos,arccos,tan
from numpy import cross
from numpy.linalg import multi_dot, norm

from argsparse import argsparse3

#FOR COLUMB MAJOR ONLY!!!!
# [Rx Ry Rz -Px] for 4x4 viewmat.
#pos4 only 1x4 for fast indexing.
#npmat3d is not used in online. i use it. haha.
#numpy matrix for 3d.
#------actually all 3d space. import 2d targeted .py instead!
# 3d location : npmat3d.pos = v4 x,y,z,w=1,  3d direction : position()
#---vec3 and quat__ named. for using v1v2,named ---v


import glm

result = glm.vec2(1) * (2, 3)

from glm import vec3,vec4
from glm import mat4
from glm import normalize as glmnormalize
#from glm import array, float32

from glm import cos,sin, radians,tan, acos
from glm import cross, dot

from glm import perspective, translate, rotate, scale

#glm.array(glm.float32, data


def vcopy3(vec):
    return vec3(vec)

def normalize(vec):
    """ vec /norm if norm not 0
    """
    if vec == vec3():
        return vec3()
    return glmnormalize(vec)
    



#=============internal variables.
#see eyetest
MAT_EYE = eye(4,dtype='float32')
AXIS_X = vec3(1,0,0)
AXIS_Y = vec3(0,1,0)
AXIS_Z = vec3(0,0,1)


#--- basic eye 4x4.
def eye4():
    return mat4()

#--- vector 4x1 for matrix calculation.
def vpos(*args):
    """ in:x, xy, xyz, (xyz) out:xyz1
    """
    x,y,z = argsparse3(args)
    return vec4(x,y,z,1)

def vdir(*args):
    """ in:x, xy, xyz, (xyz) out:xyz0
    """
    x,y,z = argsparse3(args)
    return vec4(x,y,z,0)


#===============================------------------- MVP matrix 

#--- matrix 4x4 returns
def mtrans(*args):
    """ in:x, xy, xyz, (xyz) out:mat4 translate 1,0,0,Tx
    """
    x,y,z = argsparse3(args)
    return translate(vec3(x,y,z))


def mscale(*args):
    """ in:x, xy, xyz, (xyz) out:mat4 scale 1,0,0,Sx
    """
    if len(args) == 1:#for scale only. it's temporal, not great way..
        Sx,Sy,Sz = args[0],args[0],args[0]        
    else:
        Sx,Sy,Sz = argsparse3(args)
    return scale(vec3(Sx,Sy,Sz))
    mat = eye4()
    mat[0][0] = Sx
    mat[1][1] = Sy
    mat[2][2] = Sz
    return mat


# pv = np.array((5,0,0))
# qv = np.array((2,0,0) )
# print( pv.dot(qv) )
# a = np.dot(np.array((5,0,0)), np.array((2,0,0) ))
# print(a)
# a = dot(vec3(5,0,0), vec3(2,0,0))
# print(a)


#==============all integrated in Q-.
# quat-- kinds.    input v1,v2 named ---v ex)quatv
class Quaternion:
    """
    input: x,y,z,w / axis,th /v1,v2
    output: tuple (vec3,scalar)
    """
    def __init__(self, *args):
        length = len(args)
        if length==4:
            x,y,z,w = args
        if length==2:
            #if len(args[1]) == 3:# means v2
            if type(args[1]) == type(args[0]):
            #if args[1].size == 1:# means th
                v1,v2 = args
                axis,th = quataxis(v1,v2)
            else:#means 
                axis = args[0]
                th = args[1]
                
            x,y,z,w = quatel(axis,th)

        self.v = vec3(x,y,z)
        self.s = w
        #just grab vetor componant..haha.. no q.x kinds.

    # def __repr__(self):
    #     return 'ham'
    def __str__(self):
         return f"Quaternion {self.v},{self.s}"

    #def grassman(self, another):
    def __mul__(self, another):
        """ p*q by grassmann  ..donno yet. not concajucated.
        """
        pv = self.v
        ps = self.s
        qv = another.v
        qs = another.s
        x,y,z = ps*qv+ qs*pv +cross(pv,qv)
        w = ps*qs - dot(pv,qv)
        return Quaternion(x, y, z, w)
    
    #@staticmethod
    #def vv(v1,v2): integrated to init



#----el, axis mid-function.
def quatel(axis,th):
    """ axis,th-> x y z w. preventing axis,cos things.
    """
    axis = normalize(axis)
    x,y,z = axis *sin(th/2) #v
    w = cos(th/2) #s
    return x,y,z,w

def quataxis(v1,v2):
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

#def slerp(vec1,vec2,ratio): when using multi q.






def mrot(axis,th, t=1.0):#named mrot ,basically rot by q is axis,theta.
    """in:axis (x,y,z) ,th out:mat4 rotation [[Rx0,rx1,rx2,rx3]
    axis = vec3.. not normed. we use radians for th, not deg.
    """
    qx,qy,qz, qw = quatel(axis,th*t)
    return mrotel(qx,qy,qz,qw)

def mrotv(v1,v2, t=1.0):
    #print(v1,v2)#nan occurs here!
    axis,th = quataxis(v1,v2)

    #return rotate(eye4(), th, axis)
    #glm.rotate(model, glm.radians(angle), glm.vec3(1.0, 0.3, 0.5))
    x,y,z,w = quatel(axis,th*t)
    return mrotel(x,y,z,w)


def mrotq(q):
    qx,qy,qz = q.v
    qw = q.s
    return mrotel(qx,qy,qz,qw)

def mrotel(qx,qy,qz,qw):    
    mat = [
    [1 - 2*qy**2 - 2*qz**2,   2*qx*qy - 2*qz*qw,   2*qx*qz + 2*qy*qw, 0],
    [2*qx*qy + 2*qz*qw,   1 - 2*qx**2 - 2*qz**2,   2*qy*qz - 2*qx*qw, 0],
    [2*qx*qz - 2*qy*qw,   2*qy*qz + 2*qx*qw,   1 - 2*qx**2 - 2*qy**2, 0],
    [0,0,0,1]
    ]
    return mat4(mat)


# matx = [
#     [1 - 2*qy**2 - 2*qz**2,   2*qx*qy + 2*qz*qw,   2*qx*qz - 2*qy*qw, 0],
#     [2*qx*qy - 2*qz*qw,   1 - 2*qx**2 - 2*qz**2,   2*qy*qz + 2*qx*qw, 0],
#     [2*qx*qz + 2*qy*qw,   2*qy*qz - 2*qx*qw,   1 - 2*qx**2 - 2*qy**2, 0],
#     [0,0,0,1]
#     ]


a = vec3(1,0,0)
b = vec3(1,0,0)
#print(mrotv(a,b), 'ham')








#--------------------------------xyz rotations
#we use q for fast speed. mat@mat slow!
def mrotxyz(xyztuple):
    """x-roll, y-pitch, z-yaw. imagine x-front plane.
    roll > pitch > yaw guarantees model.
    if yup, use instead mrotxZY,  using import mrotxzy as mrotxyz.
    """
    x,y,z = xyztuple
    if not (x and y and z):
        return eye4()
    q = qrot(z,AXIS_Z)*qrot(y,AXIS_Y)*qrot(x,AXIS_X) #see x y z
    return mrotq(q)

def mrotxzy(xyztuple):
    """ y up version. opengl-friendly.
    x-roll, y-pitch, z-yaw. imagine x-front plane.
    roll > pitch > yaw guarantees model.
    if yup, use instead mrotxZY,  using import mrotxzy as mrotxyz.
    """
    x,y,z = xyztuple
    if not (x or y or z):
        return eye4()
    q = qrot(y,AXIS_Y)*qrot(z,AXIS_Z)*qrot(x,AXIS_X) #see xzy
    return mrotq(q)

def qrot(deg, axis =AXIS_Z):
    """returns q rotated by axis"""
    #axis = Z
    th = radians(deg)
    return Quaternion(axis,th)



def mlookat(eye,target,upV):
    return glm.lookAt(eye, target, upV)





if __name__ == '__main__':
    #a=array(float32, 1,2,3,4 ) is for gpu directly/
    #a = mat4( 1,1,1,1, 0,0,0,0, 2,2,2,2, 3,3,3,3 ) # vertical allined
    a = mat4( ((1,1,1,1), (0,0,0,0), (2,2,2,2), (3,3,3,3)) ) # vertical allined
    b = mat4( ((1,1,1,1), (0,0,0,0), (0,0,0,0), (0,0,0,0)) ) # vertical allined
    #print(a*b)
    #print(a)
    
    model = glm.mat4(1.0)
    angle = 20
    #model = glm.rotate(model, glm.radians(angle), glm.vec3(1.0, 0.3, 0.5))
    model = glm.rotate(model, glm.radians(angle), glm.vec3(0.0, 0.0, 1.0))
    print(model)
    #print(mrotq(qrot(20,AXIS_Z)))

    v4=vec4()
    v4.x=10
    model = mat4(1.0)
    model = translate(model, v4.xyz )
    model = scale(model, vec3(0.2)) # Make it a smaller cube

    vec3(1,2,3)
    vec3()
    vec3(vec3(1,2,3))
    normalize(vec3(1,2,3))
    mat4()#eye
    vdir(1,2,3)
    mscale(10,0,5)
    print(a)



    v1 = vec3(1,0,0)
    v2 = vec3(1,1,0)
    q = Quaternion(v1,v2)
    #q=Quaternion(axis,th)
    #q=Quaternion(1,2,3,4)

    a = mrotel(1,2,3,4)
    print(a)

    
    a = mrotxyz( (30,0,0) )
    print(a)
    mlookat(vec3(0,0,0), vec3(5,0,0), vec3(0,1,0))



def mortho(left, right, bottom, top, near, far):
    return eye4()
    
def mperspective(fov, asfect, near, far):
    return glm.perspective( radians(fov), asfect, near, far)




#----..the.. viewport matrix.
def mviewport(left,bottom,width,height):
    mat = [
    [width*0.5, 0, 0, left+(width*0.5)],
    [0, height*0.5, 0, bottom+(height*0.5)],
    [0, 0, 0.5, 0.5],#0.5 better 1/2
    [0, 0, 0, 1],
    ]
    array(mat,dtype='float32')
    return mat





from time import time
ITER = 1000
#===================ROTMAT TEST
#--------- 3ms for x1000 !
v1=(1,2,3)
v2=(3,2,5)
t = time()
for i in range(ITER):
    axis,th = quataxis(v1,v2)
    x,y,z,w = quatel(axis,th)
    R = mrotel(x,y,z,w)
print(time()-t)

#===================TRANSMAT TEST
#--------- 1ms for 1000 times.
t = time()
for i in range(ITER):
    mtrans(10,5,5)
print(time()-t)

#===================TRANSMAT TEST
#--------- 1ms for 1000 times.
t = time()
for i in range(ITER):
    mscale(2)
print(time()-t)

#===================model mat TEST
#--------- 5ms for 1000times.
v1=(1,2,3)
v2=(3,2,5)
t = time()
for i in range(ITER):
    axis,th = quataxis(v1,v2)
    x,y,z,w = quatel(axis,th)
    R = mrotel(x,y,z,w)
    T = mtrans(10,5,5)
    S = mscale(2)
    mmodel = T@R@S
print(time()-t)


#===================model mat TEST
#--------- 4ms for 1000times. not that differs. anyway rotmat too, tooslow.
v1=(1,2,3)
v2=(3,2,5)
t = time()
T = mtrans(10,5,5)
S = mscale(2)
for i in range(ITER):
    axis,th = quataxis(v1,v2)
    x,y,z,w = quatel(axis,th)    
    R = mrotel(x,y,z,w)    
    mmodel = T@R@S
print(time()-t)

#===================model mat TEST
#60, 4ms.


v1=(1,2,3)
v2=(3,2,5)
t = time()
for i in range(ITER):
    axis,th = quataxis(v1,v2)
    #x,y,z,w = quatel(axis,th)
print(time()-t,'qataxis')

ITER = 100000

vec31=vec3(1,2,3)
t = time()
for i in range(ITER):
    #normalize(v1)#30ms for 100,000
    #glmnormalize(v1)#13ms for 100,000 ..when v1=(1,2,3)
    glmnormalize(vec31) #7ms. fine.
print(time()-t,'normalize')

t = time()
for i in range(ITER):
    cross(v1,v2)
print(time()-t)

t = time()
for i in range(ITER):
    acos( dot(v1,v2) )
print(time()-t)

def quataxis(v1,v2):
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
