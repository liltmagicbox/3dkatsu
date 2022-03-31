#RULE
#1. to_line, fill default smd value if empty.
#2. BONE, VERTEX and all, slow data types. has no None, but default value. [0,0,0].
#3. POSE however, controlls from data, so None if no control data. NOT default value [0,0,0] kinds.
#4. draw_ready(). MESH() and mesh.VAO = VAO() for highspeed. VAO.to_smd for save.
#all line-componants can to_ and from_. and has upper class.

class MODEL:
    def __init__(self, filedir=None, sk=None,skam=None,meshes=None):
        self.filedir = filedir
        self.sk = sk
        self.skam = skam
        self.meshes = meshes
    @classmethod
    def load_smd(cls, filedir):1

class SMD:
    def __init__(self,filedir=None, sk=None,skam=None,meshes=None):
        """we not use it. smd is for in-out. fine."""
        self.filedir = filedir
        self.sk = sk
        self.skam = skam
        self.meshes = meshes
    def __repr__(self):
        string = f"SMD filedir:{self.filedir} \n sk:{self.sk},\n'skam':{self.skam},\n'meshes':{self.meshes}"
        return string
    
    @classmethod
    def load(cls, filedir):
        with open(filedir, 'r',encoding='utf-8') as f:
            lines = f.readlines()# read '1\n2\n3' , readlines ['1\n', '2\n', '3']       
        
        sk_list = []
        skam_list = []
        meshes_list = []

        stack = ['empty']
        for line in lines:
            line = line.strip()
            if line.startswith('nodes'):
                stack.append(line)
                continue
            elif line.startswith('skeleton'):
                stack.append(line)
                continue
            elif line.startswith('triangles'):
                stack.append(line)              
                continue
            elif line.startswith('end'):
                stack.pop()
                continue

            state = stack[-1]
            if state.startswith('nodes'):
                sk_list.append(line)                
            elif state.startswith('skeleton'):
                skam_list.append(line)              
            elif state.startswith('triangles'):
                meshes_list.append(line)
        #---end for. parse later.
        sk = SK.from_lines(sk_list)
        skam = SKAM.from_lines(skam_list)
        meshes = MESH.from_lines(meshes_list)
        #return sk,skam,meshes
        return cls(filedir, sk,skam,meshes)
        
    #def save(cls, filedir, sk=None,skam=None,meshes=None):
    def save(self, filedir):
        sk = self.sk
        skam = self.skam
        meshes = self.meshes

        if sk == None:
            sk = SK()
        if skam == None:
            skam = SKAM()
        
        lines = []
        line_ver = 'version 1'      

        line_sk_head = 'nodes'
        line_sk_body = sk.to_lines()
        line_sk_end = 'end'

        line_skam_head = 'skeleton'
        line_skam_body = skam.to_lines()
        line_skam_end = 'end'

        if meshes:          
            line_meshes_head = 'triangles'
            line_meshes_body = []
            for mesh in meshes:
                line_mesh = mesh.to_lines()
                line_meshes_body.extend(line_mesh)
            line_meshes_end = 'end'
        
        #---gether lines.
        lines.append(line_ver)

        lines.append(line_sk_head)
        lines.extend(line_sk_body)
        lines.append(line_sk_end)

        lines.append(line_skam_head)
        lines.extend(line_skam_body)
        lines.append(line_skam_end)

        if meshes:
            lines.append(line_meshes_head)
            lines.extend(line_meshes_body)
            lines.append(line_meshes_end)
        
        #---to smd file
        smdstr = '\n'.join(lines)# 'x'.join([1,2,3]) = 1x2x3
        with open(filedir, 'w',encoding='utf-8') as f:
            f.write(smdstr)#write str, writelines ['a','b','c'] -> 'abc'

class BONE:
    """basic component. has default"""
    @classmethod
    def from_line(cls, line):
        ID, name, parent = line.split()
        ID = int(ID)
        name = name.replace('"','').replace("'",'')
        parent = int(parent)
        return cls(ID,name,parent)
    def to_line(self):
        #0 "root"  -1
        line = f'{self.ID} "{self.name}" {self.parent}'
        return line
    def __init__(self, ID,name='bone',parent=-1, pos=[0,0,0],rot=[1,0,0,0],scale=[1,1,1]):
        self.ID = ID
        self.name = name
        self.parent = parent
        
        self.pos = pos
        self.rot = rot
        self.scale = scale#not for SMD, but useful.

        #---for recursive
        self.safe=False

    def set(self, pos=None,rot=None,scale=None):#rot quat
        if pos:
            parent = self.parent
            self.pos = parent.pos + pos
            #we need recursive. if order not ordered..


class SK:
    @classmethod
    def from_lines(cls, lines):
        bones = []
        for line in lines:
            bone = BONE.from_line(line)
            bones.append( bone )
        return cls(bones)
    def to_lines(self):
        sk_dict = self.sk_dict
        if sk_dict=={}:
            sk_dict[0]=BONE(0,'root')
        lines = []
        #sort
        for bone in sk_dict.values():
            line = bone.to_line()
            lines.append(line)
        return lines
    
    def __init__(self, bones=None, name='skeleton'):        
        sk_dict = {}
        for bone in bones:
            sk_dict[bone.ID] = bone
        self.sk_dict = sk_dict
        self.name = name
    def __repr__(self):
        bonlen = len(self.sk_dict)
        return f"SKeleton name:{self.name} bones:{bonlen}"

    #def set(self, ID, pose):# if sensor got data, move SK, make each pose is too bad..
    def set(self, ID, pos=None,rot=None,scale=None):
        bone = self.sk_dict[ID]#thats why we choose dict.
        bone.set(pos,rot,scale)
    

class POSE:
    @classmethod
    def from_line(cls,line):        
        ID, x,y,z,a,b,c = map(float, line.split() )
        ID = int(ID)
        pos = x,y,z
        rot = QUAT.from_euler(a,b,c)
        return cls(ID, pos,rot)
    def to_line(self):
        #0 0.000000 0.000000 0.000000 0.000000 -0.000000 0.000000
        ID = self.ID
        pos = self.pos
        rot = self.rot
        if pos==None:pos=[0,0,0]
        if rot==None:rot=[1,0,0,0]
        x,y,z = pos
        a,b,c = QUAT.to_euler(rot)
        line = f"{ID} {x} {y} {z} {a:.5f} {b:.5f} {c:.5f}"
        return line
    def __init__(self, ID, pos=None,rot=None,scale=None):
        #pos relative , rot local tait-bryan,radians.
        self.ID = ID
        self.pos = pos
        self.rot = rot
        self.scale = scale

#---not frames, but frame? can easyly swapped. but skam.frame how strange..? keep remained.
class SKAM:
    @classmethod
    def from_lines(cls, lines):
        frame = 0
        skam_dict = {}
        for line in lines:
            if line.startswith('time'):#time 0
                frame = line.split()[1]
                frame = int(frame)
                if not frame in skam_dict:
                    skam_dict[frame] = []
            else:
                pose = POSE.from_line(line)
                skam_dict[frame].append(pose)
        return cls(skam_dict)
    def to_lines(self):
        lines = []
        for frame,poses in self.skam_dict.items():
            timestr = f"time {frame}"
            lines.append(timestr)

            for pose in poses:
                line = pose.to_line()           
                lines.append(line)
        return lines
    def __init__(self, skam_dict=None, name='skam'):
        if skam_dict==None:
            pose = POSE(ID=0)
            skam_dict = {0:[pose]}
        self.skam_dict = skam_dict
    def __repr__(self):
        return f"skam frames:{len(self.skam_dict)}"

    def set(self,frame,SK):
        poses = self.skam_dict[frame]
        for pose in poses:
            ID = pose.ID
            pos = pose.pos
            rot = pose.rot
            scale = pose.scale
            SK.set(ID, pos,rot,scale)





#mesh with no indices. fast, fine, easy to_from smd. indices actually for VAO, mostly. was not data-friendly.
#we choose major format smd,, no obj. nor gltf. just for smd. blender loads smd and to fbx for skanim. fine.
#all attrs fixed. for smd. fine. we fix, we go stronger, we do boldly.

#mesh has name, which is material name. or simply texture name without ext.fine.
#smd can hold many mesh(with diffrent name == material.)

#assume parent is 0, always.


class VERTEX:
    @classmethod
    def from_line(cls, line):
        parent, x,y,z, nx,ny,nz, u,v, links, *weights = line.split()#x,y,z, *c = [1,2,3, 4,5]
        
        pos = [x,y,z]
        normal = [nx,ny,nz]
        uv = [u,v]
        links
        weights
        return cls(pos,normal,uv,weights, parent)
    def to_line(self):
        #0 -0.348687 0.003982 0.113621 -0.004933 0.003593 0.006796 0.160109 0.605452 1 0 1.000000
        #4 84 1.00 61 0.00 61 0.00 61 0.00
        parent = self.parent
        pos = self.pos
        normal = self.normal
        uv = self.uv
        weights = self.weights

        x,y,z = pos
        nx,ny,nz = normal
        u,v = uv
        
        links = len(weights)//2
        line = f"{parent} {x} {y} {z} {nx} {ny} {nz} {u} {v} {links}"
        for i in range(links):
            b = weights[i*2]
            w = weights[i*2+1]
            line += f" {b} {w}"
        return line

    def __init__(self, pos=[0,0,0], normal=[0,0,0], uv=[0,0], weights=[0,1], parent=0):
        """hopefully parent always 0."""
        self.pos = pos
        self.normal = normal
        self.uv = uv
        self.weights = weights
        self.parent = parent
    def __repr__(self):
        return f"vertex pos:{self.pos},normal:{self.normal}.."


class MESH:
    @classmethod
    def from_lines(cls, lines):
        meshes_dict = {}
        for line in lines:
            splits = line.split()
            if len(splits)<2:
                mat_name = line             
                if not mat_name in meshes_dict:
                    meshes_dict[mat_name] = []
            else:               
                vertex = VERTEX.from_line(line)
                vertices = meshes_dict[mat_name]
                vertices.append(vertex)

        meshes = []
        for matname, vertices in meshes_dict.items():
            mesh = cls(matname, vertices)
            meshes.append(mesh)
        return meshes

    def to_lines(self):
        #vert: 0 -0.348687 0.003982 0.113621 -0.004933 0.003593 0.006796 0.160109 0.605452 1 0 1.000000
        lines = []
        mat_name = self.name
        for idx, vertex in enumerate(self.vertices):
            if idx%3==0:
                lines.append(mat_name)
            lines.append(vertex.to_line())
        return lines
    
    def __init__(self, name='mesh', vertices=None):
        self.name = name
        self.vertices = vertices
        self.vao = None
    def __repr__(self):
        return f"mesh name:{self.name},len:{len(self.vertices)}"

    def draw(self):
        vao = self.vao
        if vao == None:
            attrdict = self.to_dict()
            vao = VAO.from_dict(attrdict)
            self.vao = vao
        vao.draw()

    def to_dict(self):      
        vertices = self.vertices
        pos = []
        normal = []
        uv = []
        weights = []
        for vertex in vertices:
            pos.extend(vertex.pos)
            normal.extend(vertex.normal)
            uv.extend(vertex.uv)
            weights.extend(vertex.weights)

        attr_dict = {
        'pos': pos,
        'normal': normal,
        'uv': uv,
        'weights': weights,
        }
        return attr_dict
    
    @classmethod
    def from_dict(cls, name, attr_dict):
        vertices = []
        pos = attr_dict['pos']
        normal = attr_dict['normal']
        uv = attr_dict['uv']
        weights = attr_dict['weights']# [0,1,0,1,0,1,0,1] of4  OR [11,0.5,12,0.5,13,0,14,0 11,0.5,12,0.5,0,0,13,0,14,0 ] of2

        points = len(pos)//3
        wwidth = len(weights)//points #if 8, //4, 2.
        for i in range(points):
            pp = pos[i*3:i*3+3]
            nn = normal[i*3:i*3+3]
            uu = uv[i*2:i*2+2]
            ww=[]
            w = weights[i*wwidth:i*wwidth+wwidth]
            for j in range(wwidth//2):
                bone = w[j*2]
                weight = w[j*2+1]
                ww.extend([bone,weight])
            vertex = VERTEX(pos =pp,normal =nn,uv=uu,weights=ww)
            vertices.append(vertex)
        return cls(name, vertices)

class VAO:
    @classmethod
    def from_dict(cls, attrdict):1

from math import cos,sin, atan2,asin, copysign


class QUAT:
    @classmethod
    def from_euler(cls, x,y,z):
        #yaw (Z), pitch (Y), roll (X)
        #NOTE: value changed if xyz to quat to xyz.
        yaw = z
        pitch = y
        roll = x        
        cy = cos(yaw * 0.5)
        sy = sin(yaw * 0.5)
        cp = cos(pitch * 0.5)
        sp = sin(pitch * 0.5)
        cr = cos(roll * 0.5)
        sr = sin(roll * 0.5)

        qw = cr * cp * cy + sr * sp * sy
        qx = sr * cp * cy - cr * sp * sy
        qy = cr * sp * cy + sr * cp * sy
        qz = cr * cp * sy - sr * sp * cy
        return qw,qx,qy,qz
    @classmethod
    def to_euler(cls, quat):
        qw,qx,qy,qz = quat
        #// roll (x-axis rotation)
        sinr_cosp = 2 * (qw * qx + qy * qz)
        cosr_cosp = 1 - 2 * (qx * qx + qy * qy)
        angles_roll = atan2(sinr_cosp, cosr_cosp)

        #// pitch (y-axis rotation)
        sinp = 2 * (qw * qy - qz * qx)
        if (abs(sinp) >= 1):
            angles_pitch = copysign(M_PI / 2, sinp) #use 90 degrees if out of range
        else:
            angles_pitch = asin(sinp)

        #// yaw (z-axis rotation)
        siny_cosp = 2 * (qw * qz + qx * qy)
        cosy_cosp = 1 - 2 * (qy * qy + qz * qz)
        angles_yaw = atan2(siny_cosp, cosy_cosp)

        x = angles_roll
        y = angles_pitch
        z = angles_yaw
        return x,y,z

    def __init__(self,w=1,x=0,y=0,z=0):
        self.w = w
        self.x = x
        self.y = y
        self.z = z

def test():
    fname = 'DEFAULT_TOP.smd'
    smd = SMD.load(fname)
    print(smd)
    smd.save('uhaha.smd')
    


def uni():
    T='uu/DR_P00_CUN01_T.smd'
    B='uu/DR_P00_CUN01_B.smd'
    S='uu/DR_P00_CUN01_S.smd'
    t=SMD.load(T)
    b=SMD.load(B)
    s=SMD.load(S)
    win=SMD.load('win_cool_B.smd')
    n=SMD()
    #n.meshes.extend( t.meshes)
    n.meshes=t.meshes
    n.meshes.extend( b.meshes)
    n.meshes.extend( s.meshes)
    n.sk = win.sk

    #frame0 = win.skam.skam_dict[0] #linked but not default pos.
    #n.skam = SKAM( {0:frame0} )

    n.skam = t.skam
    n.save('merged.smd')

if __name__=='__main__':    
    #test()
    #uni()
    print('fine')
