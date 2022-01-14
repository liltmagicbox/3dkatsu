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
#when the pitch approaches ±90° (north/south pole). These cases must be handled specially

#those 2 don requires colmat. it's the only way to create rotmat by xyz..

def axis_N_colmat(N):
    """ col major order 4x4 matrix.
    for gpuready, need to be .T
    2ms to create of 1M
    """
    colmat = np.zeros(16*N, dtype='float32').reshape(16,N)
    return colmat

#--------basic transform to rotmat
@nb.jit(nopython=True , parallel = True)
def axis_xyz_rotmat(x,y,z):
    # err if x==1. but see axis_, it's for axis!
    #col major matrix.. for gpu. Rx,Ry,Rz=R,P,Y
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

#-fromt to rotmat moved front area..

@nb.jit(nopython=True , parallel = True)
def axis_quat_rotmat(w,x,y,z):
    """not check if quat unit quat
    """
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




# ---- to modelmat
# those requires colmat for faster, re-use.
# colmat = np.zeros(16*NN, dtype='float32').reshape(16,NN)
# because m=TRS, eachtime creating zeros inside of.. is terrorble.

@nb.jit(nopython=True , parallel = False)#its too simple, cant compile multicore..
def axis_matxyz_posmat(colmat, Tx,Ty,Tz):
    colmat[3] = Tx    
    colmat[7] = Ty     
    colmat[11] = Tz
    return colmat


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
    """ rotmat by xyz
    colmat = zeros(16,N).float32.  colmat[15]=1.
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





#==============22vs33 it defeated. 25vs33 defeated +colmat..
#very clever. rotmat can be easyly assumed 4x4 general form.
#this returns tuple... so another name-group?.. no!yet.
@nb.jit(nopython=True , parallel = True)
def xxxaxis_xyz_rot3x3(x,y,z):
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
def xxxaxis_Nxyzxyz_posrotmat(N, Tx,Ty,Tz, x,y,z):
    posrot = np.zeros(16*N, dtype='float32').reshape(16,N)
    posrot[15]=1
    rot3x3 = xxxaxis_xyz_rot3x3(x,y,z)
    posrot[0],posrot[1],posrot[2],\
    posrot[4],posrot[5],posrot[6],\
    posrot[8],posrot[9],posrot[10] = rot3x3
    posrot[3] =Tx
    posrot[7] =Ty
    posrot[11]=Tz
    return posrot



def test_TRmat_VS_TxR():
    # speed test T*R vs TR
    #axis_Nxyzxyz_posrotmat
    NN = 100_0000
    X = np.random.rand(NN)
    Y = np.random.rand(NN)
    Z = np.random.rand(NN)
    colmat = axis_N_colmat(NN)

    rotmat2 = xxxaxis_Nxyzxyz_posrotmat(NN,X,Y,Z,X,Y,Z)
    rotmat1 = axis_matxyz_rotmat(colmat, X,Y,Z)
    
    t = time()
    rotmat2 = xxxaxis_Nxyzxyz_posrotmat(NN,X,Y,Z,X,Y,Z)
    print(time()-t, 'posrotmat')
    t = time()
    colmat = axis_N_colmat(NN)
    rotmat1 = axis_matxyz_rotmat(colmat, X,Y,Z)
    print(time()-t, 'matxyz')

    t = time()
    rotmat1 = axis_matxyz_rotmat(colmat, X,Y,Z)
    print(time()-t, 'matxyz')
    t = time()
    rotmat2 = xxxaxis_Nxyzxyz_posrotmat(NN,X,Y,Z,X,Y,Z)
    print(time()-t, 'posrotmat')
    
    #22vs 33 posrotmat even slow! since it creates colmat inside..
    return 

test_TRmat_VS_TxR()



#===================== HOW SYSTEM WORKS
# >>> forward way
# <<< backward
# rotmat xyz front   axisangle quat
#[those 3 trigonal]
# quat-rotmat connected
# front departed roll, to upV. need upV for rotmat back.


# pos=   spd=    acc=   F=
#        pos+=   spd+=  acc+=  F+=
#up direct set value    >>>seems accurate >>>
#down add value,     >>> physcally simulated depth >>>

# xyz only can handle rspd, racc.
# if you want preserved r-spd, save xyz and use from it.

# 'xyz or front mode' ,
# imagine heavy switch both xyz(trigonal) VS front(game vector).
# not move so frequently, but you can do what you want



#-------------------------------


#boolean not. seems bestway..
# a = np.arange(10)
# TF = a>5
# FT = np.logical_not(TF)
# print(TF)
# print(FT)
# exit()
# FT = TF
# print(FT)



#---v0.2.8 added
#@nb.jit(nopython=True , parallel = True)
def axis_rotmat_xyz(rotmat):
    """ reversed, rotmat from xyz.
     y=90, ..
    """
    #https://stackoverflow.com/questions/15022630/how-to-calculate-the-angle-from-rotation-matrix
    #was bad x=y.
    #https://www.euclideanspace.com/maths/geometry/rotations/conversions/matrixToEuler/index.htm
    #all broken
    #http://eecs.qmul.ac.uk/~gslabaugh/publications/euler.pdf
    #finaylly! i use 1,3.

    r11= rotmat[0]
    #r12= rotmat[1]
    #r13= rotmat[2]

    r21= rotmat[4]
    #r22= rotmat[5]
    #r23= rotmat[6]
    
    r31= rotmat[8]
    r32= rotmat[9]
    r33= rotmat[10]

    x = np.arctan2(r32,r33)
    y = -np.arcsin( r31 )
    z = np.arctan2(r21,r11)
    return x,y,z

#radians 0-1 is 0-60. fine.
x = np.random.rand(5)
y = np.random.rand(5)
z = np.random.rand(5)
print(x)
print(y)
print(z)

print('===')
R = axis_xyz_rotmat(x,y,z)
rx,ry,rz = axis_rotmat_xyz(R)
#(array([0.], dtype=float32), array([0.], dtype=float32), array([0.5], dtype=float32))
print(rx)
print(ry)
print(rz)

exit()


#----------------------------------- model matrix










#----------------------------------- front kinds

@nb.jit(nopython=True , parallel = False)
def axis_vec_dot(x1,y1,z1, x2,y2,z2):
    return x1*x2+y1*y2+z1*z2    

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
    #norm = (x**2+y**2+z**2)**0.5 #but samespeed. feel free to use it..
    norm = np.sqrt(x**2+y**2+z**2)
    #or you can norm<0001, 1,0,0??no.as it already 0s.
    return x/norm,y/norm,z/norm#may return nan, but ok. fastway!



@nb.jit(nopython=True , parallel = True)
def axis_front_rotmat(x,y,z , upV =(0,1,0) ):
    """ rotmat by front.
    from my pymatrix
    """
    front = normalize(front)
    right = cross(upV, front)
    right = normalize(right)
    up = cross(front, right)
    up = normalize(up)
    rotmat = right[0],right[1],right[2],0,\
    up[0],up[1],up[2],0,\
    front[0],front[1],front[2],0,\
    0,0,0,1
    return rotmat


@nb.jit(nopython=True , parallel = False)
def axis_vecquat_rotate_qpq(x,y,z, qw,qx,qy,qz):    
    #this remains for reference. we can se how to multiply.
    #and vec->quat with w=0 is not proper quat. it's just for here!
    """ to p' = q*p*qr  / p rotated by quat. but we have 30% faster way.
    """
    pw,px,py,pz = 0,x,y,z #vector p(0,x,y,z) .. 0 but may ok..
    #qw qx qy qz quat
    #rw,rx,ry,rz = axis_quat_rev(qw,qx,qy,qz) #rev of quat
    rw,rx,ry,rz = qw,-qx,-qy,-qz

    tw,tx,ty,tz = axis_quat_mul(pw,px,py,pz, rw,rx,ry,rz) # p*qr
    w,x,y,z = axis_quat_mul(qw,qx,qy,qz, tw,tx,ty,tz ) #q*tmp
    #(array([0.]), array([0.]), array([1.]), array([0.])) #wxyz. we need to it xyz
    return x,y,z

@nb.jit(nopython=True , parallel = False)
def axis_vecquat_rotate(x,y,z, qw,qx,qy,qz):
    #since input is vector, we don't care it's roll.
    """return not normalized.
    #1.5-8x faster qpq way.
    https://en.wikipedia.org/wiki/Conversion_between_quaternions_and_Euler_angles
    """
    # V = target_vector
    # qv,qw
    # v_tmp = cross( qv, V )
    # v_rotated =  V + qw* v_tmp + qv * v_tmp
    
    tx,ty,tz = axis_vec_cross( qx*2,qy*2,qz*2, x,y,z )
    #v + qw*tv +qv*tv ..qvXtv!
    #rx = x + qw*tx +qx*tx
    #ry = y + qw*ty +qy*ty
    #rz = z + qw*tz +qz*tz
    cx,cy,cz = axis_vec_cross(qx,qy,qz, tx,ty,tz)
    rx = x + qw*tx +cx
    ry = y + qw*ty +cy
    rz = z + qw*tz +cz
    return rx,ry,rz


@nb.jit(nopython=True , parallel = False)
def axis_quat_front(qw,qx,qy,qz):
    x=1
    y=0
    z=0
    tx,ty,tz = axis_vec_cross( qx*2,qy*2,qz*2, x,y,z )
    #v + qw*tv +qvXtv
    cx,cy,cz = axis_vec_cross(qx,qy,qz, tx,ty,tz)
    rx = x + qw*tx +cx
    ry = y + qw*ty +cy
    rz = z + qw*tz +cz
    return axis_vec_normalize(rx,ry,rz)
#1Mspd test
# 0.04986882209777832
#----while of pure py. 2xspd! means it's so cpu-hard.
# 0.08377242088317871

#rotmat 4x4, good using colmat, not directly create 4x4.
#def axis_front_rotmat(x,y,z, upV = (0,1,0) ):

#----------------------------------- front kinds




def main():
    colmat = axis_N_colmat(5)
    X = np.random.rand(5)
    axis_quat_rotmat(X,X,X,X)
    axis_xyz_rotmat(X,X,X)
    axis_matxyz_posmat(colmat,X,X,X)
    axis_matxyz_rotmat(colmat,X,X,X)
    axis_matxyz_scalemat(colmat,X,X,X)

if __name__ == "__main__":
    main()









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

#BADSTATEOFME
#the one uses atan2
#https://en.wikipedia.org/wiki/Conversion_between_quaternions_and_Euler_angles
def axis_quat_xyzBAD(w,x,y,z):
    """ xyz rpy. 
    """
    #roll (x-axis rotation)
    sinr_cosp = 2 * (w * x + y * z)
    cosr_cosp = 1 - 2 * (x * x + y * y)
    roll = np.arctan2(sinr_cosp, cosr_cosp)

    #pitch (y-axis rotation)
    sinp = 2 * (w * y - z * x)
    #if (std::abs(sinp) >= 1)
    #    pitch = std::copysign(M_PI / 2, sinp) #use 90 degrees if out of range
    #else
    #    pitch = np.arcsin(sinp)

    #yaw (z-axis rotation)
    siny_cosp = 2 * (w * z + x * y)
    cosy_cosp = 1 - 2 * (y * y + z * z)
    yaw = np.arctan2(siny_cosp, cosy_cosp)
    return roll,pitch,yaw




#https://personal.utdallas.edu/~sxb027100/dock/quaternion.html
#seems Hamilton product r1->r2.
@nb.jit(nopython=True , parallel = False)
def axis_quat_mul(w1,x1,y1,z1, w2,x2,y2,z2):
    w = w1*w2 - x1*x2 - y1*y2 - z1*z2
    x = w1*x2 + x1*w2 + y1*z2 - z1*y2
    y = w1*y2 - x1*z2 + y1*w2 + z1*x2
    z = w1*z2 + x1*y2 - y1*x2 + z1*w2
    return w,x,y,z

def axis_quat_rev(w,x,y,z):
    #conjugate means ..opposite kinds of. + >> -
    #conjugation or means somewhat differ...
    #some inv codes do somethings..
    return w,-x,-y,-z

@nb.jit(nopython=True , parallel = False)
def axis_quat_grassman(pw,px,py,pz, qw,qx,qy,qz):
    """ seems it's slow. 52msvs613ms 1core/ 16vs24 jit
    p*q by grassmann  ..donno yet. not concajucated.
    """
    # pv = self.v
    # ps = self.s
    # qv = another.v
    # qs = another.s
    # x,y,z = ps*qv+ qs*pv +cross(pv,qv)
    # w = ps*qs - dot(pv,qv)
    #return Quaternion(x, y, z, w)

    cx,cy,cz = axis_vec_cross(px,py,pz, qx,qy,qz)
    x = pw*qx+ qw*px + cx #np.cross(px,qx)
    y = pw*qy+ qw*py + cy #np.cross(py,qy)
    z = pw*qz+ qw*pz + cz #np.cross(pz,qz)    
    w = pw*qw - axis_vec_dot(px,py,pz, qx,qy,qz)
    return w,x,y,z
#0.05285906791687012
#0.6139206886291504 yeah it's so sslow!
#0.016951799392700195
#0.024957656860351562 still slow with numba. donno when to use grassman.

@nb.jit(nopython=True , parallel = False)
def axis_quat_normalize(w,x,y,z):
    #q normalize i**2+=1.0. mag= sqrt(i**2+)
    sums = w**2+x**2+y**2+z**2
    #if (1-sums) < 0.001: #means near 1. no need to.. # 0.999 or 1.001?
        #return w,x,y,z
    mag = np.sqrt(sums)
    w = w/mag
    x = x/mag
    y = y/mag
    z = z/mag
    return w,x,y,z

@nb.jit(nopython=True , parallel = False)
def axis_quat_slerp(w1,x1,y1,z1, w2,x2,y2,z2, t):
    #http://codewee.com/view.php?idx=42
    dots = w1*w2 + x1*x2 + y1*y2 + z1*z2 #quat can be dotted? ..found not.
    theta = np.arccos(dots)
    sn = np.sin(theta)
    
    wa = np.sin((1-t) * theta)/sn
    wb = np.sin(t * theta)/sn
    w = wa*w1 + wb*w2
    x = wa*x1 + wb*x2
    y = wa*y1 + wb*y2
    z = wa*z1 + wb*z2
    return axis_quat_normalize(w,x,y,z)
    
#----------------------------------- quat


#--------------------------------------------axis-angle
# axis-angle via v1-v2.   aa->quat
# aa is most likely 'the rotation'. i want actor.rotate(axis,angle) kinds.. not by quat.
# actor.rotate_xyz actor.xyzrotate ... ..written oop section.


#vec we can assume need 2of it. not v1v2.
#axisa of axisangle. shorter! .. but axis and axisa too simillar.yeah.
@nb.jit(nopython=True , parallel = False)
def axis_vec_axisangle(x1,y1,z1, x2,y2,z2):
    #maybe angle/2 is not slerp, but lerp. directly across 1 to 2..
    #yeah, without roll.
    """v1,v2 -> axis,radians

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
    nx2,ny2,nz2 = axis_vec_normalize(x2,y2,z2)

    angle = np.arccos( nx1*ny1+nz1*nx2+ny2*nz2 )
    #r = np.arccos( np.dot(front,facing) )
    #return a[0]*b[0]+a[1]*b[1]+a[2]*b[2]

    x,y,z = axis_vec_cross(x1,y1,z1, x2,y2,z2)#what happens all 0??

    return x,y,z,angle
#print(axis_vec_axisangle(1,0,0, 0,0,-1))
#(0, 1, 0, 1.5707963267948966) #works great!

@nb.jit(nopython=True , parallel = False)
def axis_axisangle_quat(x,y,z,r):
    """ x,y,z, radians to quat
    axis can be long, so we normalize it."""
    x,y,z = axis_vec_normalize(x,y,z)
    w = np.cos(r/2)
    sinhalf = np.sin(r/2)
    x = x * sinhalf
    y = y * sinhalf
    z = z * sinhalf
    return w,x,y,z
#not tested


#====================BELOW 2 ARE NOT COMFIRNMED . BAD STATE OF ME..

#it liiks liek xyz->quat->aa./
#actually it means quite quat like situation..
#we do xyz_quat, quat_axisangle. fine...not fine. we needit.
#https://www.euclideanspace.com/maths/geometry/rotations/conversions/eulerToAngle/
def axis_xyz_axisangle_BAD(x,y,z): # wehave xyzquat xyzrotmat
    z = heading #sms way
    y = attitude #sems pitch
    x = bank #sms rolll
    c1 = np.cos(heading/2)
    s1 = np.sin(heading/2)
    c2 = np.cos(attitude/2)
    s2 = np.sin(attitude/2)
    c3 = np.cos(bank/2)
    s3 = np.sin(bank/2)
    c1c2 = c1*c2
    s1s2 = s1*s2
    w =c1c2*c3 - s1s2*s3
    x =c1c2*s3 + s1s2*c3
    y =s1*c2*c3 + c1*s2*s3
    z =c1*s2*c3 - s1*c2*s3
    angle = 2 * np.arccos(w)
    norm = x*x+y*y+z*z
    
    #when all euler angles are zero angle =0 so
    #we can set axis to anything to avoid divide by zero
    if norm < 0.001:
        x=1
        y=0
        z=0
    else:
        norm = np.sqrt(norm)
        x /= norm
        y /= norm
        z /= norm
    return x,y,z,angle


#https://en.wikipedia.org/wiki/Quaternions_and_spatial_rotation
#https://www.euclideanspace.com/maths/geometry/rotations/conversions/quaternionToAngle/index.htm
# it's backward! some says: recovering.
def xxaxis_quat_axisangle_BAD(w,x,y,z):
    #angle = 2 * acos(qw)
    #diver = sqrt(1-qw*qw)
    diver = np.sqrt(qx**2+qy**2+qz**2)
    x = qx / diver
    y = qy / diver
    z = qz / diver
    angle = 2*np.arctan2(diver,w)
    return x,y,z,angle

#the place where already axis_xyz_quat was..rip.


def axis_axisangle_xyz_BAD(x,y,z,r):
    3
#--------------------------------------------axis-angle


#--------------------------------------------utility

#axis3_majorinput_output . axis3 means, axis with 3attrs. input too long, so just major.
#output assumes what the funcion does, it's name.
#def axis_pos_lookat(ex,ey,ez, tx,ty,tz): here axis3_func created.

#def axis3_frontpospos_frontlookat(ex,ey,ez, tx,ty,tz): too long name, too much inputs.
#def axis3_front_quatlookat.. is not the way. see qpq, returns rotated vector, not quat.
def axis3_front_lookat(front, pos, targetpos, ratio = 1.0):    
    """ ratio 0~1. object to lookat target. front-in, front-out.
    even we have v1v2->aa, target-eye order confusing.
    you may need to lerp or set or pereserve upV , manually.
    """
    #front = eye-target#donno why but this way.fine. we have lot to do.

    # v1=front, v2=direction.
    # v1v2 aa ->quat
    # v1->quat2 ,  quatquat -> newquat
    # newquat ->front
    # mostly we do something with front(like fire..). so not quat.
    #..but if you just want lookat and draw,, we don't need front.
    #since front again changed to xyz or quat..
    #quat is the last form before 4x4rotmat..yeah.
    
    directon = targetpos-pos
    #x,y,z,r = axis_vec_axisangle(front, directon)
    x,y,z,r = axis_vec_axisangle(front[0],front[1],front[2], directon[0],directon[1],directon[2],)
    #good naming structure. i could recall it without look.
    #print(directon, x,y,z,r)# [0.] [-0.] [1.] [1.57079633] 1,0,0 to target0,1,0
    w,x,y,z = axis_axisangle_quat(x,y,z, r*(1-ratio) )
    #print(w, x,y,z) #[0.70710678] [0.] [-0.] [0.70710678] fine 1,0,0 to target0,1,0

    #w,x,y,z = axis_quat_slerp(w,x,y,z, ratio)
    #axis_quat_slerp(w1,x1,y1,z1, w2,x2,y2,z2, t)
    #slerp no meaning since aa roll_info broken.
    #but it returns front!
    #use r/N instead for smaller angle.

    #axis_vecquat_rotate(front, w,x,y,z) input x,y,z as vector
    #print(rx,ry,rz)#[1.] [1.] [0.]
    #rx,ry,rz = axis_vecquat_rotate_qpq(front[0],front[1],front[2], w,x,y,z)
    rx,ry,rz = axis_vecquat_rotate(front[0],front[1],front[2], w,x,y,z)
    fx,fy,fz = axis_vec_normalize(rx,ry,rz)#since it is front
    return fx,fy,fz

#--------------------------------------------utility

x = np.random.rand(1000000).astype('float32')
y = np.random.rand(1000000).astype('float32')
z = np.random.rand(1000000).astype('float32')
axis_vecquat_rotate(x,y,z, z,x,y,z)
axis_vecquat_rotate_qpq(x,y,z, z,x,y,z)

x = np.random.rand(1000000).astype('float32')
y = np.random.rand(1000000).astype('float32')
z = np.random.rand(1000000).astype('float32')
t=time()
axis_vecquat_rotate.py_func(x,y,z, z,x,y,z)
print(time()-t,'30faster')

x = np.random.rand(1000000).astype('float32')
y = np.random.rand(1000000).astype('float32')
z = np.random.rand(1000000).astype('float32')
t=time()
axis_vecquat_rotate_qpq.py_func(x,y,z, z,x,y,z)
print(time()-t,'qpq')
#numba
#0.01799750328063965 30faster
#0.034018516540527344 qpq

#1core
#0.022938966751098633 30faster
#0.36916160583496094 qpq


#-----------rotated front test
front = np.zeros(3).reshape(3,1)
front[0]=1
pos = np.zeros(3).reshape(3,1)
target = np.zeros(3).reshape(3,1)
target[0]=0
target[1]=1
print('rotated front 1,0,0 by target 0,1,0',axis3_front_lookat( front,pos,target,0.9999) )
#(array([0.70710678]), array([0.70710678]), array([0.]))
#(array([-2.22044605e-16]), array([1.]), array([0.]))
#--------------------------------------------vector

def colinear( points ):
    """Given 3 points, determine if they are colinear

    Uses the definition which says that points are collinear
    iff the distance from the line for point c to line a-b
    is non-0 (that is, point c does not lie on a-b).

    returns None or the first 
    """
    if len(points) >= 3:
        a,b,c = points[:3]
        cp = crossProduct(
            (b-a),
            (a-c),
        )
        if magnitude( cp )[0] < 1e-6:
            return (a,b,c)
    return None

#--------------------------------------------vector


exit()

#--------------------------------------------oop
#from skim
#rotater = Rotater(30,0,0)
#actor1.rotate( rotater )

#arrived here
#aa = xyz_aa(30,0,0)
#aa = oop_xyz_aa(30,0,0) #not axis_xyz_aa !
#aa = oop_vec_aa(v1,v2)
#actor1.set_rpos_aa(aa)

#actor1.set_rpos_quat(w,x,y,z)
#--------------------------------------------oop


#------------------------------------actorarray
#------------------------------------actorarray

#----its not (1,N)D. calc?? input not posx,posy,posz... it's not axis-by function.
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

