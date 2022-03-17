from PIL import Image
from OpenGL.GL import *
from common import get_namekey

class Texture:
    last=-1
    last_unit = 0

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
       cls(1,1,name='default')

    @classmethod #enables using method without instancing.
    def byimg(cls,imgname):
        try:
            img = Image.open(imgname)
            npimg = np.asarray(img)
            img.close()
        except:
            print('fail to load img')
            return 0
        height,width,depth = npimg.shape
        #cls.__init__(cls,width,height)
        texture = cls(width,height)
        texture.update(npimg)
        return texture


    @classmethod #enables using method without instancing.
    def bynp(cls,npimg):
        height,width,depth = npimg.shape
        cls.__init__(cls,width,height)
        cls.update(cls,npimg)
        return cls

    def __repr__(self):
        return f"Texture name:{self.name}"

    def __init__(self,width,height, MIPMAP = False, FORMAT = GL_RGB, name='texture'):
        """FORMAT DEFAULT NP DEPTH3, MIPMAP CREATES MIPMAP"""
        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture) # all upcoming GL_TEXTURE_2D operations now have effect on this texture object
        
        #https://www.khronos.org/registry/OpenGL-Refpages/gl4/html/glTexParameter.xhtml
        # set the texture wrapping parameters
        #glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP_TO_EDGE)
        #glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP_TO_EDGE) datault GL_REPEAT

        # set texture filtering parameters
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)#GL_NEAREST
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)#GL_LINEAR
        if MIPMAP:
            #glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST_MIPMAP_LINEAR)#line effect??
            #glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_NEAREST)#quite blur
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_NEAREST_MIPMAP_NEAREST)#not bad
            #glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)#triple linear...too blur
        
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA8, width, height, 0, FORMAT, GL_UNSIGNED_BYTE, None)#level, border=0
        #gpu internally stores BGRA way, even 3rd format is GL_RGBA8. internally.
        #note last 3 format, type, data is of data.
        
        self.MIPMAP = MIPMAP
        self.FORMAT = FORMAT
        self.ID = texture
        self.width = width
        self.height = height

        self.unitdict = {
            0:GL_TEXTURE0,
            1:GL_TEXTURE1,
            2:GL_TEXTURE2,
            3:GL_TEXTURE3,
            4:GL_TEXTURE4,
            5:GL_TEXTURE5,
            6:GL_TEXTURE6,
            }
        glBindTexture(GL_TEXTURE_2D, 0)

        name = self.__class__.set(name,self)
        self.name = name



    def update(self,data):
        """img fliped internally."""
        tmpdata = np.empty_like(data)
        np.copyto(tmpdata,data[::-1,:])#fliped.fine.

        glBindTexture(GL_TEXTURE_2D, self.ID)
        #level mipmap.
        glTexSubImage2D(GL_TEXTURE_2D, 0, 0, 0, self.width, self.height, self.FORMAT, GL_UNSIGNED_BYTE, tmpdata )
        if self.MIPMAP:
            glGenerateMipmap(GL_TEXTURE_2D)#dont forget it! we need this here, if use mipmap.
        #https://www.khronos.org/opengl/wiki/Common_Mistakes#Automatic_mipmap_generation
        #https://stackoverflow.com/questions/16165963/updating-opengl-mipmapped-texture
        glBindTexture(GL_TEXTURE_2D, 0)

    def bind(self, unit=0):
        cls = self.__class__
        #https://www.khronos.org/registry/OpenGL-Refpages/gl4/html/glActiveTexture.xhtml
        if cls.last_unit != unit:
            glActiveTexture(self.unitdict[unit])
            cls.last_unit = unit
        if cls.last != self.ID:
            glBindTexture(GL_TEXTURE_2D, self.ID)
            cls.last = self.ID
    def unbind(self):
        glBindTexture(GL_TEXTURE_2D, 0)
        cls.last = -1

    def get_np(self):
        """returns fliped, directly save to img."""
        self.bind()
        width = self.width
        height = self.height
        #c_void_p(2035528935616),fine.
        data = np.empty(width*height*4).reshape(height,width,4).astype('uint8')#hope it's fast enough.
        glGetTexImage(GL_TEXTURE_2D, 0, GL_RGBA, GL_UNSIGNED_BYTE, data)#RGBA8 errors. RGBA instread. 
        #data 000.. why?? -beacuase not bind texture!hahaha.

        #err anyway. i don want this.
        ###glGetTextureSubImage(GL_TEXTURE_2D, 0, 0,0,0,   width,height,0, GL_RGBA, GL_UNSIGNED_BYTE, data.nbytes, data)
        return data[::-1]

    @classmethod
    def save_png(self,npimg,filename):
        im = Image.fromarray(npimg)
        im.save(f"{filename}.png")#it's texture,dude! not jpg!
        #im.save(filename, quality=95)# q 95 fine. default 75. jpg/bmp:5ms PNG:50ms
        #im.save('q100sub0.jpg', quality=100, subsampling=0)#for jpg (maybe) uncompressed.
