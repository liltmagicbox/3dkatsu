import numpy as np
from numpy.linalg import multi_dot

#npmat3d is not used in online. i use it. haha.
#numpy matrix for 3d.


#------actually all 3d space. import 2d targeted .py instead!
# 3d location : npmat3d.pos = v4 x,y,z,w=1,  3d direction : position()

from argsparse import argsparse3

#--- basic eye 4x4.
def eye4():
    return np.eye(4,dtype='float32')

#--- vector 4x1 returns
def vpos(*args):
    """ in:x, xy, xyz, (xyz) out:xyz1
    """
    x,y,z = argsparse3(args)
    return np.array( [ x,y,z,1] , dtype = 'float32')

def vdir(*args):
    """ in:x, xy, xyz, (xyz) out:xyz0
    """
    x,y,z = argsparse3(args)
    return np.array( [ x,y,z,0] , dtype = 'float32')

def vpos3(*args):
    """ in:x, xy, xyz, (xyz) out:xyz
    """
    x,y,z = argsparse3(args)
    return np.array( [ x,y,z] , dtype = 'float32')

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
    Sx,Sy,Sz = argsparse3(args)
    mat = eye4()
    mat[0][0] = Sx
    mat[1][1] = Sy
    mat[2][2] = Sz
    return mat


def mrot(axis,deg):
    """ in:axis (x,y,z) ,deg out:mat4 rotation [[Rx0,rx1,rx2,rx3]
    """
    xyz = argsparse3(axis)
    if xyz == (0,0,1):#z axis
        return mrotz(deg)
    elif xyz == (0,1,0):#y axis
        return mroty(deg)
    elif xyz == (1,0,0):#x axis
        return mrotx(deg)

    else:#means custom-axis : quaternion!
        return mrotz(deg)#for now..hehe


#---rotation for Z, Y, Z axis.
def mrotz(deg):
    """turn. rh, in:deg.
    """
    mat = eye4()
    deg = np.radians(deg)
    C = np.cos(deg)
    S = np.sin(deg)
    mat[0][0] = C
    mat[0][1] = -S
    mat[1][0] = S
    mat[1][1] = C
    return mat
def mroty(deg):
    """yaw. head up or down..
    """
    mat = eye4()
    deg = np.radians(deg)
    C = np.cos(deg)
    S = np.sin(deg)    
    mat[0][0] = C
    mat[0][2] = S
    mat[2][0] = -S#-
    mat[2][2] = C
    return mat
def mrotx(deg):
    """roll
    """
    mat = eye4()
    deg = np.radians(deg)
    C = np.cos(deg)
    S = np.sin(deg)
    mat[1][1] = C
    mat[1][2] = -S
    mat[2][1] = S
    mat[2][2] = C
    return mat


if __name__ == '__main__':
    target = vpos(5,0,0)
    P = mtrans(10,10)
    R = mrot((0,0,1), 30)
    S = mscale(3)    
    end = multi_dot( (P,R,S,target) )
    print(end)
    #[22.990381 17.5       0.        1.      ]


#--------view matrix.
#inverse of camera position.. rotate first.
# campos, target, upV?
# eye xyz, at xyz, up xyz.
#lookat means , world to view trans.
#...actually glulookat is for cam. maybe deprecated..ha.




def mview(eye,target,upV):
    """input each vector..4! no tuple."""
    #vpos3()
    #we need up right front.
    #front ,fine. up,up. right = cross front,up
    front = target - eye
    right = np.cross( front, upV)
    up = upV
    front = front/np.linalg.norm(front)
    right = right/np.linalg.norm(right)
    up = up/np.linalg.norm(up)
    
    view1 = [[right[0],right[1],right[2],0],
    [up[0],up[1],up[2],0],
    [front[0],front[1],front[2],0],
    [0,0,0,1]]
    
    view2 = [[1,0,0,-eye[0]],
    [0,1,0,-eye[1]],
    [0,0,1,-eye[2]],
    [0,0,0,1]]

    view1 = np.array(view1,dtype='float32')
    view2 = np.array(view2,dtype='float32')
    #print(view1,'v1')
    #print(view2,'v2')
    return view1@view2

def mview_rotation(eye,target,upV):
    """input each vector..4! no tuple."""
    front = target - eye
    front = front/np.linalg.norm(front)

    right = np.cross(front, upV)
    right = right/np.linalg.norm(right)

    up = np.cross(right , front)
    
    #print(front,right,up,'isnorm')

    #slower 30% since /norm.
    #front = front/np.linalg.norm(front)
    #right = right/np.linalg.norm(right)
    #up = up/np.linalg.norm(up)
    
    
    view1 = [[right[0],right[1],right[2],0],
    [up[0],up[1],up[2],0],
    [front[0],front[1],front[2],0],
    [0,0,0,1]]

    # view1 = [
    # [right[0],up[1],front[2],0],
    # [right[0],up[1],front[2],0],
    # [right[0],up[1],front[2],0],
    # [0,0,0,1]] 
    
    return np.array(view1,dtype='float32')
#https://www.3dgep.com/understanding-the-view-matrix/
#optimize v@v


def mview_col(eye,target,upV):
    """input each vector..4! no tuple."""
    front = target - eye
    front = front/np.linalg.norm(front)

    right = np.cross(upV, front)
    right = right/np.linalg.norm(right)

    up = np.cross(front, right)
    up = up/np.linalg.norm(up)
    
    view1 = [
    [right[0],right[1],right[2],0],
    [up[0],up[1],up[2],0],
    [front[0],front[1],front[2],0],
    [0,0,0,1]]
    
    return np.array(view1,dtype='float32')

def mview_translate(eye,target,upV):
    """input each vector..4! no tuple."""   
    view2 = eye4()    
    view2[0][3] = -eye[0]
    view2[1][3] = -eye[1]
    view2[2][3] = -eye[2]
    return np.array( view2, dtype='float32')


eye = vpos3(3,0,1)
target = vpos3(0,0,0)
upV = vpos3(0,1,0)


eye = vpos3(2,0,0)
#eye = vpos3(cam.x,cam.y,cam.z)
target = vpos3(0,0,0)
upV = vpos3(0,1,0)


#rotv = mview_rotation(eye,target,upV)
rotv = mview_col(eye,target,upV)
transv = mview_translate(eye,target,upV)
print('rototo')
print(eye,target,upV)

print(rotv,'rot')
print(transv,'tr')


#print(mview_rotation(eye,target,upV))
#print(mview_translate(eye,target,upV))


#vv = mview(eye,target,upV)
#print(vv)
#po = vpos(1,0,0)
#print(vv.dot(po))



#--------------orthogonal matrix.
#N = R*S*T.
# note: R -1 for z. S is scale, tondc, T is middle point to ndc.

#---left right bottom top near far. 6 attrs.

#https://stackoverflow.com/questions/42864623/glortho-equivalent-to-vbos

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




def mperspective(left, right, bottom, top, near, far):
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


#----..the.. viewport matrix.
def mviewport(left,bottom,width,height):
    mat = [
    [width*0.5, 0, 0, left+(width*0.5)],
    [0, height*0.5, 0, bottom+(height*0.5)],
    [0, 0, 0.5, 0.5],#0.5 better 1/2
    [0, 0, 0, 1],
    ]
    np.array(mat,dtype='float32')
    return mat



#-----------------------below is history
#list : tests /  naming,define /  3.old concept





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