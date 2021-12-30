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


class npVector(np.ndarray):
    def __new__(subtype, x,y,z ):
        obj = super().__new__(subtype, shape=(3,), dtype='float32', buffer=None, offset=0,
                strides=None, order=None)

        obj[0],obj[1],obj[2] = x,y,z
        obj.x, obj.y, obj.z = x,y,z
        return obj

    def __getattribute__(self,name):
        if name == 'x':
            return self[0]#finally!
            #return self.x max recur..
        elif name == 'y':
            return self[1]
        elif name == 'z':
            return self[2]
        return super().__getattribute__(name)

    def __setattr__(self, name, value):
        if name == 'x':
            self[0] = value
        elif name == 'y':
            self[1] = value
        elif name == 'z':
            self[2] = value
        super().__setattr__(name, value)




#----using npVector
def vec3(*args):
    """ in:x, xy, xyz, (xyz) out:xyz
    """
    x,y,z = argsparse3(args)
    #return array( [ x,y,z] , dtype = 'float32')
    return npVector(x,y,z)

def vpos3(*args):
    """deprecated use vec3
    """
    x,y,z = argsparse3(args)
    #return array( [ x,y,z] , dtype = 'float32')
    return npVector(x,y,z)

def vcopy3(vec3):
    return vec3.copy()

def normalize(vec):
    """ vec /norm if norm not 0
    """
    norms = norm(vec)
    if not norms == 0:
        return vec/norms
    return vec


#=============internal variables.
#see eyetest
MAT_EYE = eye(4,dtype='float32')
AXIS_X = vec3(1,0,0)
AXIS_Y = vec3(0,1,0)
AXIS_Z = vec3(0,0,1)


#--- basic eye 4x4.
def eye4():
    return MAT_EYE.copy()    

#--- vector 4x1 for matrix calculation.
def vpos(*args):
    """ in:x, xy, xyz, (xyz) out:xyz1
    """
    x,y,z = argsparse3(args)
    return array( [ x,y,z,1] , dtype = 'float32')

def vdir(*args):
    """ in:x, xy, xyz, (xyz) out:xyz0
    """
    x,y,z = argsparse3(args)
    return array( [ x,y,z,0] , dtype = 'float32')




#===============================------------------- MVP matrix 

#--- matrix 4x4 returns
def mtrans(*args):
    """ in:x, xy, xyz, (xyz) out:mat4 translate 1,0,0,Tx
    """
    Tx,Ty,Tz = argsparse3(args)
    mat = eye4()
    mat[0][3] = Tx
    mat[1][3] = Ty
    mat[2][3] = Tz
    return mat


def mscale(*args):
    """ in:x, xy, xyz, (xyz) out:mat4 scale 1,0,0,Sx
    """
    if len(args) == 1:#for scale only. it's temporal, not great way..
        Sx,Sy,Sz = args[0],args[0],args[0]        
    else:
        Sx,Sy,Sz = argsparse3(args)
    mat = eye4()
    mat[0][0] = Sx
    mat[1][1] = Sy
    mat[2][2] = Sz
    return mat




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
            if args[1].size == 1:# means th
                axis = args[0]
                th = args[1]
                v1,v2 = args
            else:#means v2
                axis,th = quataxis(v1,v2)
                
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
        w = ps*qs - pv.dot(qv)
        return Quaternion(x, y, z, w)
    
    #@staticmethod
    #def vv(v1,v2): integrated to init

#Quaternion(v1,v2)
#Quaternion(axis,th)
#Quaternion(1,2,3,4)


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
    th = arccos( front.dot(facing) )
    return axis,th

#def slerp(vec1,vec2,ratio): when using multi q.




#mrotv(v1,v2)#fastest
#mrot(axis,th)#simple or custom axis
#mrotq(quat) #fast
#mrotq(Quaternion(vec3(x,y,z),radians(30)))# use mrot instead..
#mrotq(Quaternion(x,y,z,w)) #usally not happens.

#mrotel(x,y,z,w)#most primitive way. we not use it, yeah.
#no, it's for internal. since q = Quaternion(x,y,z,w)    #return mrotq(q)

#----------mrot ations using quaternion.

def mrot(axis,th, t=1.0):#named mrot ,basically rot by q is axis,theta.
    """in:axis (x,y,z) ,th out:mat4 rotation [[Rx0,rx1,rx2,rx3]
    axis = vec3.. not normed. we use radians for th, not deg.
    """
    qx,qy,qz, qw = quatel(axis,th*t)
    return mrotel(qx,qy,qz,qw)

def mrotv(v1,v2, t=1.0):
    axis,th = quataxis(v1,v2)
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
    return array(mat,dtype='float32')

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




#--------view matrix.
#inverse of camera position.. rotate first.
# campos, target, upV?
# eye xyz, at xyz, up xyz.
#lookat means , world to view trans.
#...actually glulookat is for cam. maybe deprecated..ha.

#https://www.3dgep.com/understanding-the-view-matrix/
#optimize v@v

def mlookat(eye,target,upV):
    """input each vector..4! no tuple."""
    front = eye-target#donno why but this way.fine. we have lot to do.
    front = front/norm(front)

    right = cross(upV, front)
    right = right/norm(right)

    up = cross(front, right)
    up = up/norm(up)
    
    view1 = [
    [right[0],right[1],right[2],0],
    [up[0],up[1],up[2],0],
    [front[0],front[1],front[2],0],
    [0,0,0,1]]
    
    v1 =  array(view1,dtype='float32')

    view2 = eye4()    
    view2[0][3] = -eye[0]
    view2[1][3] = -eye[1]
    view2[2][3] = -eye[2]
    v2 = array( view2, dtype='float32')

    return v1@v2







#--------------orthogonal matrix.
#N = R*S*T.
# note: R -1 for z. S is scale, tondc, T is middle point to ndc.

#---left right bottom top near far. 6 attrs.

#https://stackoverflow.com/questions/42864623/glortho-equivalent-to-vbos
#---actguatly colmom !
def mortho(left, right, bottom, top, near, far):
    ortho = eye4()

    tx = -(right + left) / (right - left)
    ty = -(top + bottom) / (top - bottom)
    tz = -(far + near) / (far - near)

    ortho[0][0] = 2 / (right - left)
    ortho[1][1] = 2 / (top - bottom)
    ortho[2][2] = -2 / (far - near)
    ortho[0][3] = tx
    ortho[1][3] = ty
    ortho[2][3] = tz
    return ortho



def mperspective(fov, asfect, near, far):
    fov = radians(fov)
    ortho = eye4()

    f= 1/ tan(fov/2)
    
    head = f/asfect
    body = f
    mid = (far+near)/(near-far)
    east = (2*far*near)/(near-far)

    ortho[0][0] = head
    ortho[1][1] = body
    ortho[2][2] = mid
    ortho[2][3] = east

    ortho[3][2] = -1
    ortho[3][3] = 0
    return ortho

#ort = mperspective(1.0297, 800 / 600, 0.1, 100.0)
#print(ort)
#print(ort[0][0])


if __name__ == '__main__':
    target = vpos(5,0,0)
    P = mtrans(10,10)
    R = mrot((0,0,1), 30)
    S = mscale(3)    
    end = multi_dot( (P,R,S,target) )
    print(end)
    #[22.990381 17.5       0.        1.      ]






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