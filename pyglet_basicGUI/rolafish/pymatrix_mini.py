from math import radians, tan, sqrt

def eye4():
    mat = [0.0]*16
    mat[0]=1.0 #00
    mat[5]=1.0 #11
    mat[10]=1.0 #22
    mat[15]=1.0 #33
    return mat

#seems it WAS colmajor.
def mortho(left, right, bottom, top, near, far):
    #note: if you use fov,ratio, we need change some,,
    #by cam.pos.. not. use area kinds. attr for ortho.
    mat = [0.0]*16

    a = right - left
    b = top - bottom
    c = far - near
    mat[0] = 2 / a #00
    mat[5] = 2 / b #11
    mat[10] = -2 / c #22
    
    mat[3] = -(right + left) / a #03
    mat[7] = -(top + bottom) / b #13
    mat[11] = -(far + near) / c #23
    mat[15] = 1.0
    return mat


def mperspective(fov, ratio, near, far):
    fov = radians(fov)
    
    f= 1/ tan(fov/2)

    mat = [0.0]*16

    mat[0] = f/ratio
    mat[5] = f #11 4*1+1 = 5
    mat[10] = (far+near)/(near-far) #22 4*2+2=10
    
    mat[11] = -1 #23, COL MAJOR.
    mat[14] = (2*far*near)/(near-far) #32
    mat[15] = 0 #33 4*3+3= 15
    return mat






class vec3(list):
    def __init__(self, *args):
        le = len(args)
        if le == 0:
            super().__init__( (0.0,0.0,0.0) )
            self.x = 0.0
            self.y = 0.0
            self.z = 0.0
        elif le == 1:
            x,y,z = args[0]
            super().__init__( (x,y,z) )
            self.x = x
            self.y = y
            self.z = z

        else:
            x,y,z = args
            super().__init__( (x,y,z) )
            self.x = x
            self.y = y
            self.z = z            

    def __str__(self):
        return "Vector "+super().__str__()
 
    def __add__(self,other):
        return vec3( self[0]+other[0], self[1]+other[1] ,self[2]+other[2] )
    def __sub__(self,other):
        return vec3( self[0]-other[0], self[1]-other[1] ,self[2]-other[2] )
    
    def __iadd__(self,other):
        return vec3( self[0]+other[0], self[1]+other[1] ,self[2]+other[2] )
    def __isub__(self,other):
        return vec3( self[0]-other[0], self[1]-other[1] ,self[2]-other[2] )

    def __mul__(self,x):
        return vec3( self[0]*x, self[1]*x ,self[2]*x)
    def __truediv__(self,x):#unsupported operand type(s) for /: 'list' and 'vec3'
        return vec3( self[0]/x, self[1]/x ,self[2]/x)
    #def __getattribute__(self,name):
    def __getattr__(self,name):
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


def dot(a,b):
    return a[0]*b[0]+a[1]*b[1]+a[2]*b[2]


def cross(v1,v2):
    d,e,f = v1
    g,h,i = v2
    x= (e*i-f*h)
    y=-(d*i-f*g)
    z= (d*h-e*g)
    return vec3(x,y,z)

def normalize(v):
    x,y,z = v
    if not x==y==z==0:
        dem = sqrt( x**2+y**2+z**2 )
        return vec3( x/dem, y/dem, z/dem )    
    return vec3(0,0,0)





def mlookat(eye,target,upV):
    front = eye-target#donno why but this way.fine. we have lot to do.
    #front = front/norm(front) #orrurs div/0
    front = normalize(front)

    right = cross(upV, front)
    right = normalize(right)

    up = cross(front, right)#donno why 2.
    up = normalize(up)
    
    minus_eye = eye*-1
    v1 = [
    right[0],up[0],front[0],0,
    right[1],up[1],front[1],0,
    right[2],up[2],front[2],0,
    dot(right , minus_eye),dot(up , minus_eye),dot(front , minus_eye),1]
    return v1










def dot4(A,B):
    return A[0]*B[0]+A[1]*B[1]+A[2]*B[2]+A[3]*B[3]


def mul4x4(A,B):
    row0 = A[0:4]
    row1 = A[4:8]
    row2 = A[8:12]
    row3 = A[12:16]
    
    col0 = B[0],B[4],B[8],B[12]
    col1 = B[1],B[5],B[9],B[13]
    col2 = B[2],B[6],B[10],B[14]
    col3 = B[3],B[7],B[11],B[15]

    mat = [0.0]*16
    mat[0] = dot4(row0,col0)
    mat[1] = dot4(row0,col1)
    mat[2] = dot4(row0,col2)
    mat[3] = dot4(row0,col3)
    
    mat[4] = dot4(row1,col0)
    mat[5] = dot4(row1,col1)
    mat[6] = dot4(row1,col2)
    mat[7] = dot4(row1,col3)
    
    mat[8] = dot4(row2,col0)
    mat[9] = dot4(row2,col1)
    mat[10] = dot4(row2,col2)
    mat[11] = dot4(row2,col3)
    
    mat[12] = dot4(row3,col0)
    mat[13] = dot4(row3,col1)
    mat[14] = dot4(row3,col2)
    mat[15] = dot4(row3,col3)
    
    return mat







def mortho_row(left, right, bottom, top, near, far):
    #note: if you use fov,ratio, we need change some,,
    #by cam.pos.. not. use area kinds. attr for ortho.
    mat = [0.0]*16

    a = right - left
    b = top - bottom
    c = far - near
    mat[0] = 2 / a #00
    mat[5] = 2 / b #11
    mat[10] = -2 / c #22
    mat[3] = -(right + left) / a #03
    mat[7] = -(top + bottom) / b #13
    mat[11] = -(far + near) / c #23
    mat[15] = 1.0
    return mat

def mperspective_row(fov, ratio, near, far):
    fov = radians(fov)
    
    f= 1/ tan(fov/2)

    mat = [0.0]*16

    mat[0] = f/ratio
    mat[5] = f #11 4*1+1 = 5
    mat[10] = (far+near)/(near-far) #22 4*2+2=10
    mat[11] = (2*far*near)/(near-far) #23 8+3=11    
    mat[14] = -1 #32 3*4+2=14
    mat[15] = 0 #33 4*3+3= 15
    return mat




def mlookat_row(eye,target,upV):
    front = eye-target#donno why but this way.fine. we have lot to do.
    #front = front/norm(front) #orrurs div/0
    front = normalize(front)

    right = cross(upV, front)
    right = normalize(right)

    up = cross(front, right)#donno why 2.
    up = normalize(up)
    
    minus_eye = eye*-1
    v1 = [
    right[0],right[1],right[2], dot(right , minus_eye),
    up[0],up[1],up[2], dot(up , minus_eye),
    front[0],front[1],front[2], dot(front , minus_eye),
    0,0,0,1]
    return v1

    # v1 = [
    # right[0],right[1],right[2],0,
    # up[0],up[1],up[2],0,
    # front[0],front[1],front[2],0,
    # 0,0,0,1]
    
    # #isthis just ..tx ty tz?
    # v2 = eye4()
    # v2[3] = -eye[0] #03
    # v2[7] = -eye[1] #13
    # v2[11] = -eye[2] #23
    # return mul4x4(v1,v2)
