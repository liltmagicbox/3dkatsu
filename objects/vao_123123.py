from OpenGL.GL import *
from common import get_namekey
import numpy as np
import pyglet

# #---badway
# vaoidx = VAO( {0:3,1:2},
#     #np.array([0,0,0, 0,0,  0.5,0,0, 1,0,  0.5,0.5,0, 1,1,  0,0.5,0, 0,1, ]).astype('float32'),
#     #np.array([0,0,0, 0,0,  1,0,0, 1,0,  1,1,0, 1,1,  0,1,0, 0,1, ]).astype('float32'),
#     np.array([ [0,0,0, 0,0],  [1,0,0, 1,0],  [1,1,0, 1,1],  [0,1,0, 0,1] ]).astype('float32'),
#     np.array([0,1,2,0,2,3,]).astype('uint')
#     )

#hard to parse. we take thisway.
# vaoidx = VAO(
#     {
#     'position' : [ 0,0,0, 1,0,0, 1,1,0, 0,1,0,],
#     'uv' : [ 0,0,  1,0,  1,1,  0,1 ],
#     },
#     indices = [0,1,2,0,2,3,]    
#     )#name

#hard to parse.
# vaoidx = VAO(
#     position= [ 0,0,0, 1,0,0, 1,1,0, 0,1,0,],
#     uv = [ 0,0,  1,0,  1,1,  0,1 ],    
#     indices = [0,1,2,0,2,3,]
#     )#name

vao_attrs={
    'position' : np.array([ 0,0,0, 1,0,0, 1,1,0, 0,1,0,]).astype('float32'),
    'uv' : np.array([ 0,0,  1,0,  1,1,  0,1 ]).astype('float32'),
    }
vao_indices = np.array([0,1,2,0,2,3,]).astype('uint')

# for i,nparr in vao_attrs.items():
#     a = len(nparr)
#     print(a)

class VAO:
    """indexed actually. hope we not use vao_notindexed."""
    last = -1

    #---namedict ver 0.2
    namedict = {}
    @classmethod
    def get(cls, name):
        if not 'default' in cls.namedict:            
            cls.default()
        return cls.namedict.get(name)
    @classmethod
    def set(cls, name: str, item) -> str:
        name = get_namekey(cls.namedict,name)
        cls.namedict[name]=item
        return name
    @classmethod
    def default(cls):
        cls(vao_attrs,vao_indices,name='default')

    def __repr__(self):
        return f"vao name:{self.name}"

    def __init__(self, attrdict,indices, name='vao'):
        """we need attrdict{'position':ndarr(f32)} !"""
        #attrlist=[]
        #for attrname, nparr in attrdict.items():
        #    attrlist.append(nparr)
        #vertices = np.concatenate( attrlist ).astype('float32')
        assert list(attrdict.keys())[0]=='position'
        
        vert_count = len(attrdict['position'])//3
        
        #attr_size_dict = {0:3,1:2}
        attr_size_dict = {}
        attridx = -1
        for attrname, nparr in attrdict.items():
            attridx+=1
            attrN = len(nparr)//vert_count
            attr_size_dict[attridx] = attrN            
        stride = sum(attr_size_dict.values())#5, of 3+2

        vertices = []        
        for idx, nparr in enumerate(attrdict.values()):
            vertlen = attr_size_dict[idx]
            verted = nparr.reshape(-1,vertlen)                
            vertices.append(verted)
        vertices = np.hstack(vertices).flatten().astype('float32')        

        #---old way
        #vertices = np.array([ [0,0,0, 0,0],  [1,0,0, 1,0],  [1,1,0, 1,1],  [0,1,0, 0,1] ]).astype('float32')
        #indices = np.array([0,1,2,0,2,3,]).astype('uint')
        #attr_size_dict = {0:3,1:2}
        #stride = sum(attr_size_dict.values())#5, of 3+2
        
        #pos 12, indices,,
        #vert_count = len(indices)


        datatype = GL_FLOAT
        normalized = GL_FALSE #GL_TRUE
        fsize = np.float32(0.0).nbytes #to ensure namespace-safe.
        
        VAO = glGenVertexArrays(1) # create a VA. if 3, 3of VA got. #errs if no window.
        VBO = glGenBuffers(1) #it's buffer, for data of vao.fine.
        EBO = glGenBuffers(1) #indexed, so EBO also. yeah.

        glBindVertexArray(VAO) #gpu bind VAO

        glBindBuffer(GL_ARRAY_BUFFER, VBO) #gpu bind VBO in VAO
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

        pre_offset = 0
        for attr_index, size in attr_size_dict.items():
            if pre_offset==0:
                offset = None
                offset = ctypes.c_void_p(0)#maybe it seems works.
                glVertexAttribPointer(attr_index, size, datatype, normalized, stride * fsize, offset)
                glEnableVertexAttribArray(attr_index)
                pre_offset = size    
            else:
                offset = ctypes.c_void_p( pre_offset *fsize)
                glVertexAttribPointer(attr_index, size, datatype, normalized, stride * fsize, offset)
                glEnableVertexAttribArray(attr_index)
                pre_offset +=size


        self.ID = VAO
        self.ID_VBO = VBO
        self.ID_EBO = EBO
        self.stride = stride        
        self.points = len(indices)
        self.vertices = vertices
        self.name = self.__class__.set(name,self)

    def update_position(self,position):
        vertices = self.vertices
        
        #assume 0,1,2 is posxyz.
        vertices[0::self.stride] = position[0::3]
        vertices[1::self.stride] = position[1::3]
        vertices[2::self.stride] = position[2::3]

        VAO = self.ID
        VBO = self.ID_VBO
        glBindVertexArray(VAO)
        glBindBuffer(GL_ARRAY_BUFFER, VBO) #gpu bind VBO in VAO
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        #GL_STREAM_DRAW for little change, if you want someday..
        self.vertices = vertices

    def update(self,vertices):
        """requires same shape kinds.."""
        VAO = self.ID
        VBO = self.ID_VBO
        glBindVertexArray(VAO)
        glBindBuffer(GL_ARRAY_BUFFER, VBO) #gpu bind VBO in VAO
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        #GL_STREAM_DRAW for little change, if you want someday..
        #self.points = len(vertices)//self.stride #donno why do this..

    def update_indices(self,vertices, indices):
        """hope we not use this.."""
        VAO = self.ID
        VBO = self.ID_VBO
        EBO = self.ID_EBO
        glBindVertexArray(VAO)
        glBindBuffer(GL_ARRAY_BUFFER, VBO) #gpu bind VBO in VAO
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)
        self.points = len(indices)#now we can really change it..

    def bind(self):
        if VAO.last != self.ID:
            glBindVertexArray(self.ID)
            VAO.last = self.ID
    def unbind(self):
        glBindVertexArray(0)
        VAO.last = -1

    def draw(self, MODE = 'triangles'):
        """requires bind first. it just draw command of VAO bound gpu."""
        #simple mode changeable draw. we not prefer partial draw which is slow.        
        draw_dict = {'points':GL_POINTS,
        'lines':GL_LINE_STRIP,
        'triangles':GL_TRIANGLES,
        }
        MODE = draw_dict[MODE]
        glDrawElements(MODE, self.points, GL_UNSIGNED_INT, None)

if __name__ == "__main__":
    window = pyglet.window.Window()
    VAO.default()
    a = VAO.get('default')
    print(a)