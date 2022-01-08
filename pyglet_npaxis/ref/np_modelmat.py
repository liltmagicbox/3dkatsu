import numpy as np
from numpy import array, eye
from numpy import radians, sin,cos,arccos,tan
from numpy import cross
from numpy.linalg import multi_dot, norm

#FOR COLUMB MAJOR ONLY!!!!
# [Rx Ry Rz -Px] for 4x4 viewmat.

#pos4 only 1x4 for fast indexing.


#npmat3d is not used in online. i use it. haha.
#numpy matrix for 3d.


#------actually all 3d space. import 2d targeted .py instead!
# 3d location : npmat3d.pos = v4 x,y,z,w=1,  3d direction : position()

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


from argsparse import argsparse3

#--- basic eye 4x4.
def eye4():
    return eye(4,dtype='float32')

#--- vector 4x1 returns
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

#wonder but copy copys npV not ndarray..
# a = vec3(0,0,0)
# b = a.copy()
# a.x=55
# b.y=33
# print(a, type(a))
# print(b, type(b))
# print(' copy returns npVector, not ndarray! ')


def normalize(vec):
    norms = norm(vec)
    if not norms == 0:
        return vec/norms
    return vec



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

#----------is for the quaternion.
def mrot(axis,th):
    """ axis = vec3.. not normed. we use radians for th, not deg.
    in:axis (x,y,z) ,th out:mat4 rotation [[Rx0,rx1,rx2,rx3]
    q = [qv , qs]
    qv = a *sin(th/2)
    qs = cos(th/2)
    """
    #qx, qy, qz, qw = argsparse3(axis), th
    #if norm(axis) == 0:
        #return eye4()
    #try:#ASSUMES ONLY ERROR COMES FROM DIV/0. ---- gui collects all error !
    axis = normalize(axis)
    qx,qy,qz = axis *sin(th/2) #qv
    qw = cos(th/2) #qs
    #print( norm((qx,qy,qz,qw))) for unit quat.

    #https://www.euclideanspace.com/maths/geometry/rotations/conversions/quaternionToMatrix/index.htm
    quat = [
    [1 - 2*qy**2 - 2*qz**2,   2*qx*qy - 2*qz*qw,   2*qx*qz + 2*qy*qw, 0],
    [2*qx*qy + 2*qz*qw,   1 - 2*qx**2 - 2*qz**2,   2*qy*qz - 2*qx*qw, 0],
    [2*qx*qz - 2*qy*qw,   2*qy*qz + 2*qx*qw,   1 - 2*qx**2 - 2*qy**2, 0],
    [0,0,0,1]
    ]
    return array(quat,dtype='float32')

#print(0==norm(vec3(0,0,0)),'hm')
#a=mrot(vec3(0,0,0),1) #seems rh.fine. seems working.
#print(a)

#-----when Missile.. facing also requires normalized.
#print(axis,th)[nan nan nan] [0.        1.5707964 1.5707964]
#front =  vec3([-0.6113929  , 0.02094242  ,0.79105   ])
#facing = vec3([35.69067   , -0.30694106 , 8.406034  ] )
    
def mrotv(front,facing):
    """return 4x4 rot v1 to v2.
    """
    #---check if qv same dir front
    #if front == facing: #or use vec3same() kinds??
    #    return eye4()
    #we check at mrot.

    #---qv
    axis = cross(front, facing)    
    axis = normalize(axis)
    #---qs
    
    #front = normalize(front)
    facing = normalize(facing)
    th = arccos( front.dot(facing) )
    return mrot(axis,th)

#mrotv(front,facing)


# front = 
# pos
# target

# #---qv
# dist = target-pos
# facing = dist/norm(dist) #similier to front
# axis = cross(front, facing)
# axis = axis/norm(axis)
# #---qs
# th = arccos(front, facing)
# #---check if qv same dir front
# #...
# rotmat = mrot(axis,deg)
     


def mrotxyz(xyztuple):
    """x-roll, y-pitch, z-yaw. imagine x-front plane.
    roll > pitch > yaw guarantees model.
    if yup, use instead mrotxZY,  using import mrotxzy as mrotxyz.
    """
    x,y,z = xyztuple
    return mrotz(z)@mroty(y)@mrotx(x) #see x y z

def mrotxzy(xyztuple):
    """ y up version. opengl-friendly.
    x-roll, y-pitch, z-yaw. imagine x-front plane.
    roll > pitch > yaw guarantees model.
    if yup, use instead mrotxZY,  using import mrotxzy as mrotxyz.
    """
    x,y,z = xyztuple
    return mroty(y)@mrotz(z)@mrotx(x) #see x z y


#---rotation for Z, Y, Z axis. .. since we want 3d.. zup
def mrotz(deg):
    """turn. rh, in:deg.
    """
    mat = eye4()
    deg = radians(deg)
    C = cos(deg)
    S = sin(deg)
    mat[0][0] = C
    mat[0][1] = -S
    mat[1][0] = S
    mat[1][1] = C
    return mat
def mroty(deg):
    """yaw. head up or down..
    """
    mat = eye4()
    deg = radians(deg)
    C = cos(deg)
    S = sin(deg)    
    mat[0][0] = C
    mat[0][2] = S
    mat[2][0] = -S#-
    mat[2][2] = C
    return mat
def mrotx(deg):
    """roll
    """
    mat = eye4()
    deg = radians(deg)
    C = cos(deg)
    S = sin(deg)
    mat[1][1] = C
    mat[1][2] = -S
    mat[2][1] = S
    mat[2][2] = C
    return mat


def rotate_z(vector,degree):
    if len(vector) == 3:
        mat4 = mrotz(degree)
        v4 = vpos( vector )
        v4 = mat4 @ v4
        return vec3( v4[0],v4[1],v4[2] )
    elif len(vector) == 4:
        mat4 = mrotz(degree)
        return mat4 @ vector

def rotate_y(vector,degree):
    if len(vector) == 3:
        mat4 = mroty(degree)
        v4 = vpos( vector )
        v4 = mat4 @ v4
        return vec3( v4[0],v4[1],v4[2] )
    elif len(vector) == 4:
        mat4 = mroty(degree)
        return mat4 @ vector


#------------------- MVP matrix 


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

    eee = vec3(0,0,2)
    ttt = vec3(0,0,0)
    uuu = vec3(0,1,0)
    mat = mlookat(eee,ttt,uuu)
    print(mat)






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






#---------------------------test
#----------------------ref

#row major 
#when camera : [2. 0. 0.] [0. 0. 0.] [0. 1. 0.]

# [[ 0. -0.  1.  0.]
#  [ 0.  1.  0.  0.]
#  [-1.  0.  0.  0.]
#  [ 0.  0.  0.  1.]] rot
# [[ 1.  0.  0. -2.]
#  [ 0.  1.  0. -0.]
#  [ 0.  0.  1. -0.]
#  [ 0.  0.  0.  1.]] tr
#=================================

# eye = vec3(0,0,2)
# target = vec3(0,0,0)
# upV = vec3(0,1,0)
# vvv  = mview(eye,target,upV)
#print(vvv)

# eye = vec3(2,0,0)
# target = vec3(0,0,0)
# upV = vec3(0,1,0)
# rotv = mview_rotation(eye,target,upV)
# transv = mview_translate(eye,target,upV)
# print('rototo')
# print(eye,target,upV)
# print(rotv,'rot')
# print(transv,'tr')











#-----------------------below is history
#list : npVector /  battle / tests /  naming,define /  3.old concept



#npvector old version. close, but i want full function of ndarray, need init()anyawy.
#found new, that's the one. it passes object and holds as self!7
# class npVector(object):
#     def __init__(self,x,y,z):
#         self.array = np.array( [ x,y,z] , dtype = 'float32')

#     def __repr__(self):
#         return self.array.__repr__()#lovely!

#     def __setattr__(self, name, value):
#         if name == 'x':
#             self.array[0] = value
#         elif name == 'y':
#             self.array[1] = value
#         elif name == 'z':
#             self.array[2] = value
#         super().__setattr__(name, value)

#     def __getattribute__(self,name):
#         if name == 'x':
#             return self.array[0]
#         elif name == 'y':
#             return self.array[1]
#         elif name == 'z':
#             return self.array[2]
#         return super().__getattribute__(name)#prevents recur..


#view mat parts.
# #---------------------oonly for history.
# def mview_rotation(eye,target,upV):
#     """input each vector..4! no tuple."""
#     front = target - eye
#     front = front/norm(front)

#     right = cross(upV, front)
#     right = right/norm(right)

#     up = cross(front, right)
#     up = up/norm(up)
    
#     view1 = [
#     [right[0],right[1],right[2],0],
#     [up[0],up[1],up[2],0],
#     [front[0],front[1],front[2],0],
#     [0,0,0,1]]
    
#     return np.array(view1,dtype='float32')

# def mview_translate(eye,target,upV):
#     """input each vector..4! no tuple."""   
#     view2 = eye4()    
#     view2[0][3] = -eye[0]
#     view2[1][3] = -eye[1]
#     view2[2][3] = -eye[2]
#     return np.array( view2, dtype='float32')


# 2021.11.30.am1:47. there were 4hrs fight for col-row major.
# col won.
# and found perspective mat was an enermy also.
#     view1 = [
#     [right[0],right[1],right[2],0],
#     [up[0],up[1],up[2],0],
#     [front[0],front[1],front[2],0],
#     [0,0,0,1]]
#     VS
#     view1 = [
#     [front[0],up[1],right[2],0],
#     [front[0],up[1],right[2],0],
#     [front[0],up[1],right[2],0],
#     [0,0,0,1]]

#----row major trator!    
# def mortho(left, right, bottom, top, near, far):
#     ortho = eye4()

#     tx = -(right + left) / (right - left)
#     ty = -(top + bottom) / (top - bottom)
#     tz = -(far + near) / (far - near)

#     ortho[0][0] = 2 / (right - left)
#     ortho[1][1] = 2 / (top - bottom)
#     ortho[2][2] = -2 / (far - near)
#     ortho[0][3] = tx
#     ortho[1][3] = ty
#     ortho[2][3] = tz
#     return ortho



#---speed test for scale.
# def scale( scale):
#     scalemat = eye4()
#     scalemat = scalemat*scale
#     scalemat[3][3] = 1
#     return scalemat

#import time
# a= time.time()
# for i in range(1000000):
#     scale(3)
# print(time.time()-a,'scale')
#2.5 s for 1M

# a= time.time()
# for i in range(1000000):
#     mscale(3)
# print(time.time()-a,'mscale')
#1.9 s for 1M. win!







#---for if 0,0,1 == worldZ.
#donno but seems ok,,alteast..
# normZ = np.array( [0,0,1] )
# if np.array((0,0,1),dtype='uint32').all() == normZ.all():
#     print('ham')
#     print(np.array((0,0,1),dtype='uint32'))
#     print(normZ)



#---we tested all xyz rotation!works great RH.
# xx = vdir(1,1,0)
# rr = mroty(5)
# print( xx)
# print( rr )
# #print( rr*xx ) not thisway.
# print( rr.dot(xx) )
# #print( multi_dot( (xx,rr))) inversed.
# print( multi_dot( (rr,xx)))

#--- z axis rotation- righthanded works great!
# xx = vdir(1,0,0)
# rr = mrotz(3)
# print( xx)
# print( rr )
# #print( rr*xx ) not thisway.
# print( rr.dot(xx) )
# #print( multi_dot( (xx,rr))) inversed.
# print( multi_dot( (rr,xx)))

#print( tt.dot(rr).dot(ss).dot(xx) )
#print( multi_dot( (tt,rr,ss,xx)))











#----- define words:
#position vector vs displacement vector direction
# position v vs direction v.
#position ~= location. 3d pos= 3dloc.
#3d dir is fine. but py uses dir..
#displaycement => translate.

#3d coordinate and direction.
#coordinate = location = position = displacement    position is fine.
#direction = rotation..? looking? look?       direction is fine.

#so:

#----3d location:position and looking-angle: direction.
#position : v4 with w=1. (x,y,z,1) (isit called row vector)
#direction : v4 with w=0. (x,y,z,0)

#---transform matrix
#translate : mat4 for translate. 1,0,0,Tx kinds.
#rotate : mat4 for rotation. axis-theta. axis: x,y,z and q for more..
#scale : mat4 for scale. Sx..

#----- define functions:
#pos may can be variable name, not function name.
# whatif mat_pos : but i want 4xmat called mat only..
# matpos() posmat() matxxx is fine. mxxx seems not good.. m_pos ..bad..
# matpos(10,5,0) matrot('x',) #i want matrot(x,30) but x too weak. matrotx(30).. not bad?!
# matrotq( (1,0,0), 30) is really good.
# or just matrot( axis, deg)...
# i think, matrotx goes too bad to ..manage all functions related with a module.
#matrot(axis, degree) axis, if upv, can be.. and even local or global! fine.


"""
#--- position and direction:
pos(x,y,z) if pos(x,y), just do..? no!! ..but i think it can be very easy to change 2d to 3d.. ..fine. i will do so then.

#---trans matrix:
mattrans( x,y,z ) or mattrans( (x,y,z))
matrot(axis, deg). use upV or worldZ kinds.. if you want rot by z.
matscale(x,y,z) or matscale(S)

#- for 2d,  or you can not use z.. yeah. imagine robot soccor game..
#those are actually will used in npmat2d.
#ah, you can use it for sprite, 2d-hud also! wonderful. "sprite is just 2 of tris with texture."
matscale(10,10) .. you want pressed one? use instead: matscale(1,1,0.1)  or matscale(10). directional scale is very speciall.
mattrans(x,y) fine.
matrot(30) for z.. not bad but.. not bad really.

mat requires 3 words, while m only 1 word.
mrot(30) mrot(upV,30) mtrans(1,0,0) mtrans(5,5) mscale(3)
... seems good. so fast.
m_rot requires _ , which is bad.
vpos(x,y,z) ! fine,fine,fine.
#---------------------------
#-----final functions define

#---vec4, 3d-position and 3d-direction.
#vpos(x,y,z) or vpos((x,y,z)) and for 2d: vpos(x,y) vpos((x,y))------------we do it later! ha!
#my head gonna break, if this now..
vpos(x,y,z) or vpos((x,y,z))
vdir(x,y,z) or vdir((x,y,z))
#--- transform matrix, 4x.
mscale(S) or mscale(Sx,Sy,Sz)
mtrans(x,y,z) or mtrans((x,y,z))
#mrot(30) for 2d. not now!!
mrot(upV,30) fine.

#what about vpos.x ? --if you allow it, vpos.x may break the system..

#----------------what if, use just ( (x,y,z) ) ?? -for np, we need ( (,,) ). if you just use: mtrans((1,0,0)).
# if len(input) ==3 requires cost. i don wannait.
the problem: classify: (1,0,0) vs 1,0,0.
#or just use if if if .

def solver(*arg):
    if len(arg) == 1:
        print('one')
    elif len(arg) == 2:
        print('two')
    elif len(arg) == 3:
        print('three')


    

vpos((x,y,z))
vdir((x,y,z))
mscale(3)
mtrans((1,0,0))
mrot((0,0,1),30)

"""









#----------------------old concept

"""
#-------------gen 2.
#pos in v3, xyz,  out v4 xyz1 fine.
#

#move--so bad naming..
transpose
trans


rotz
rot
rotate
#what if, rot(z,30) => rot( (0,0,1), 30) , and so, we can quaternion!
rot_q( (1,0,0), 30) fine.


scale
scalex..this seems bad.. use scale(30,'z') instead..?

pos = 

pos = [
[1. 0. 0. X],
 [0. 1. 0. Y.],
 [0. 0. 1. Z.],
 [0. 0. 0. 1.],]

rot.. for x,y,z axis.. not i want. yeah.
i want qt.. even xyz rot, translate.
if you lookat anim, interpolate..

c -s
s c
kinds.
[[1. 0. 0. 0.]
 [0. 1. 0. 0.]
 [0. 0. 1. 0.]
 [0. 0. 0. 1.]]


scale
[[Sx. 0. 0. 0.]
 [0. Sy. 0. 0.]
 [0. 0. Sz. 0.]
 [0. 0. 0. 1.]]


matt= eye4()
matt[1][1] = 5
print(matt * np.array([1,2,3,4]))
print(matt * np.array([[1],[2],[3],[4]]))




#-------------gen 2.
robot_pos = pos4()

pos = eye4()
rot = eye4()
scale = eye4()
#scale = np.eye(4)

#rot.dtype
#dtype('float32')

#------------add value..
#pos_mat[0][3] +=1 not this.. ..ithink it's better. since index-pointing is O(0)..
#pos_mat[0] += 0,0,0,1	better..
#....?

#robot_pos = pos*rot*scale*robot_pos broadcasting!!

robot_pos = multi_dot( (pos,rot,scale,robot_pos) )

print(robot_pos)

# matmul - * is ..broadcasting. 4x4 * 4x1 => 4x4. i don't want it!
#use dot or .. multi_dot. a.dot(b).dot(c)...




pos
[[1. 0. 0. X.]
 [0. 1. 0. Y.]
 [0. 0. 1. Z.]
 [0. 0. 0. 1.]]

rot.. for x,y,z axis.. not i want. yeah.
i want qt.. even xyz rot, translate.
if you lookat anim, interpolate..

c -s
s c
kinds.
[[1. 0. 0. 0.]
 [0. 1. 0. 0.]
 [0. 0. 1. 0.]
 [0. 0. 0. 1.]]


scale
[[Sx. 0. 0. 0.]
 [0. Sy. 0. 0.]
 [0. 0. Sz. 0.]
 [0. 0. 0. 1.]]



def scale( scale):
	scalemat = eye4()
	scalemat = scalemat*scale
	scalemat[3][3] = 1
	return scalemat

#robot_scale = scale(4) vs
#robot_scale *=2 vs
#robot_scale +=2 ..bad i think.

#robot_pos+(1,0,0,0) array([6., 0., 0., 1.])

#robot.pos.x+=3 this is the one!
#robot.pos += (5,3,0) or this..  ..we know w one, ofcourse.
#robot.pos = (5,3,0) or this..
#robot.pos.xyz = 1,3,0 what if?

#robot.scale=3 i think this is!
#robot.scale.z =0.3 fine.
#scale absolute or additive..?
#robot.scale = robot.scale*0.9 not bad this.yeah. ..actually this is required..maybe.
#you can then directly set the value also.

#robot.rot.z = 30
#robot.rot
#----- we rotate, by give axis and deg. if for z, self.up.fine.

"""