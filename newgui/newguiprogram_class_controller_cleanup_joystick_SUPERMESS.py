import uuid

from time import time, sleep
import numpy as np


import pyglet
#from pyglet.gl import * #we don't use it!

from OpenGL.GL import *
from OpenGL.GL import shaders

from collections import deque


def clamp(target, low,high):
    if low<=target<=high:
        return target
    else:
        return 'ham'
#https://stackoverflow.com/questions/4092528/how-to-clamp-an-integer-to-some-range
def clamp(n, smallest, largest):return max(smallest, min(n, largest))


#-rules
#texture.TEXTURE. long but fine. since VAO VBO..
#update usually changes data. note VAO.update_indices means +indices.

#ID UI all capital
#is_() get_() set_() ,,,not direct self.isValue = True
# oop_ axis_
#def set_position_xy(self, value, mousex,mousey)


#=============================== WINDOW
#window setting must be first, later gl settings.

#Win32Window
class Window(pyglet.window.Window):
    def __init__(self, width=800,height=600):
        self.__width = width
        self.__height = height        
        super().__init__(width,height) #0-799, 1-600
        #self.set_size(500, 300)#need init resizable=True
        #self.get_framebuffer_size()
        #print(self.width,self.height)
        #print(window.get_size())
        #self.set_exclusive_mouse(True)
        self.set_vsync(False)  #for maximum fps      
        self.keymap = {'T': 'lock_mouse(1)', 'ESCAPE': 'close'}
        self.ismouselock = False
        
        def on_key_press(symbol,modifiers):
            #print(symbol)
            #print(pyglet.window.key.symbol_string(symbol))
            pass
        self.on_key_press = on_key_press

    def close(self,value=False):#alt f4 error fixed.
        super().close()
        return True

    def lock_mouse(self,value=False):
        if not value:return True#works great. True for escape        
        self.ismouselock = not self.ismouselock
        self.set_exclusive_mouse(self.ismouselock)#lock mouse x,y 0, hold. use dxdy then!         
        return True #escape



window = Window()

[
 '_windowed_size',
 '_ws_style',
 'activate',
 'canvas',
 'caption',
 'clear',
 'close',
 'config',
 'context',
 'dispatch_event',
 'dispatch_events',
 'dispatch_pending_events',
 'display',
 'draw_mouse_cursor',
 'event',
 'event_types',
 'flip',
 'fullscreen',
 'get_framebuffer_size',
 'get_location',
 'get_pixel_ratio',
 'get_size',
 'get_system_mouse_cursor',
 'get_viewport_size',
 'has_exit',
 'height',
 'invalid',
 'maximize',
 'minimize',
 'on_close',
 'on_key_press',
 'on_resize',
 'pop_handlers',
 'projection',
 'push_handlers',
 'register_event_type',
 'remove_handler',
 'remove_handlers',
 'resizeable',
 'screen',
 'set_caption',
 'set_exclusive_keyboard',
 'set_exclusive_mouse',
 'set_fullscreen',
 'set_handler',
 'set_handlers',
 'set_icon',
 'set_location',
 'set_maximum_size',
 'set_minimum_size',
 'set_mouse_cursor',
 'set_mouse_platform_visible',
 'set_mouse_position',
 'set_mouse_visible',
 'set_size',
 'set_visible',
 'set_vsync',
 'style',
 'switch_to',
 'update_transparency',
 'visible',
 'vsync',
 'width']
#===============================gl settings
glEnable(GL_DEPTH_TEST) #--skip depth less kinds.. default fine.
#glClearColor(0.0, 0.24, 0.5, 1.0) #moved from draw loop.. #..why it here??
glPointSize(5) #good for debug




#=============================== SHADER
vertn = """
#version 410 core

layout (location = 0) in vec3 pos;
layout (location = 1) in vec2 uv;

out vec2 uvcord;

//gl_VertexID
//uniform int idx;
//uniform mat4 Model[252]; //253 max.. why not 255? 250 to remember easy
uniform mat4 Model;
uniform mat4 View;
uniform mat4 Projection;

void main() 
{
    //gl_Position = Projection * View * Model[gl_InstanceID] * vec4(pos,1);
    //gl_Position = Projection * View * Model * vec4(pos * ,1);
    gl_Position = Projection * View * Model * vec4(pos, 1);
    uvcord = uv;
}
"""

fragn = """
#version 410 core

in vec2 uvcord;

out vec4 outcolor;

uniform sampler2D tex0;
//uniform sampler2D tex1;

void main()
{
    outcolor = texture2D(tex0, uvcord);
    //outcolor = vec4(uvcord,1,1 );
    //outcolor = mix(texture(tex0, uvcord), texture(tex1, uvcord), 0.4);
}
"""

class Shader:
    def __init__(self, vertstr, fragstr):
        assert bool(glCreateShader)#sometimes compile error occurs, before window() 
        vshader = shaders.compileShader( vertn, GL_VERTEX_SHADER)
        fshader = shaders.compileShader( fragn, GL_FRAGMENT_SHADER)
        program = shaders.compileProgram( vshader,fshader)
        glDeleteShader(vshader)
        glDeleteShader(fshader)
        self.SHADER= program

        #----Locations. no need to bind the program.
        self.ProjectionLoc = glGetUniformLocation(program, "Projection")
        self.ViewLoc = glGetUniformLocation(program, "View")
        self.ModelLoc = glGetUniformLocation(program, "Model")
        #self.ViewProjectionLoc = glGetUniformLocation(program, "ViewProjection")#ithink 4x4*4x4 not slow.
        #-1 if not exist. or 0..1..2..kinds.
        assert -1 not in (self.ProjectionLoc,self.ViewLoc,self.ModelLoc)

    def bind(self):
        glUseProgram(self.SHADER)
    def unbind(self):
        glUseProgram(0)

    def set_Model(self,modelmat):
        """we need bind the shader first!"""
        glUniformMatrix4fv(self.ModelLoc,1,False, modelmat)# True for row major.ha.[1,2,3,4, ,]
        #location count transpose data
    def set_Projection(self,projectionmat):
        glUniformMatrix4fv(self.ProjectionLoc,1,False, projectionmat)
    def set_View(self,viewmat):
        glUniformMatrix4fv(self.ViewLoc,1,False, viewmat)

    #def set_Camera(self,camera): #we think, if (view,projedtion) or viewXprojection , but we don't so.
        #if len(camera) == 1:#VP            ViewProjectionLoc        



#=============================== SHADER

shader = Shader(vertn,fragn)
#print(s.ViewLoc)
#s.bind()
#s.set_Model(modelmat)
#s.unbind()


#=============================== MESH DATA
# --data area
# meshdata = xyz,uv,,kinds.
# VAO = VAO,VBO created, attr connects data.


class VAO:
    def __init__(self, attr_size_dict,  vertices):
        #{0:3,1:2}
        stride = sum(attr_size_dict.values())

        datatype = GL_FLOAT
        normalized = GL_FALSE #GL_TRUE
        fsize = np.float32(0.0).nbytes #to ensure namespace-safe.
        
        VAO = glGenVertexArrays(1) # create a VA. if 3, 3of VA got.
        VBO = glGenBuffers(1) #it's buffer, for data of vao.fine.

        glBindVertexArray(VAO) #gpu bind VAO
        glBindBuffer(GL_ARRAY_BUFFER, VBO) #gpu bind VBO in VAO
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

        pre_offset = 0
        #attr_len = len(attr_size_tuple)//2
        #for i in range(attr_len):
        #    attr_index = attr_size_tuple[i*2]
        #    size = attr_size_tuple[i*2+1]
        
        for attr_index, size in attr_size_dict.items():
            if pre_offset==0:
                offset = None
                glVertexAttribPointer(attr_index, size, datatype, normalized, stride * fsize, offset)
                glEnableVertexAttribArray(attr_index)
                pre_offset = size    
            else:
                offset = ctypes.c_void_p( pre_offset *fsize)
                glVertexAttribPointer(attr_index, size, datatype, normalized, stride * fsize, offset)
                glEnableVertexAttribArray(attr_index)
                pre_offset +=size
            
        self.VAO = VAO
        self.VBO = VBO
        #self.mode = GL_TRIANGLES some model drawn lines kind thing requires not use it.
        self.stride = stride
        self.points = len(vertices)//stride

    def update(self,vertices):
        """requires same shape, same attr .. ..not that much.?"""
        #assert self.points == len(vertices)//self.stride
        VAO = self.VAO
        VBO = self.VBO
        glBindVertexArray(VAO)
        glBindBuffer(GL_ARRAY_BUFFER, VBO) #gpu bind VBO in VAO
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        #GL_STREAM_DRAW for little change, if you want someday..
    
    def bind(self):
        glBindVertexArray(self.VAO)
    def unbind(self):
        glBindVertexArray(0)

    def draw(self, MODE = GL_TRIANGLES):
        """requires bind first. it just draw command of VAO bound gpu."""
        #simple mode changeable draw. we not prefer partial draw which is slow.
        #glBindVertexArray(self.VAO)
        glDrawArrays(MODE, 0, self.points) #mode first count


vao = VAO( {0:3,1:2},
    np.array([0,0,0, 0,0,  1,0,0, 1,0,  1,1,0, 1,1,  0,1,0, 0,1, ]).astype('float32')
    )
vao.update( np.array([0,0,0, 0,0,  1,0,0, 1,0,  1,1,0, 1,1, ]).astype('float32') )
#vao.draw()


class VAO_Indexed:
    def __init__(self, attr_size_dict,  vertices, indices):
        stride = sum(attr_size_dict.values())

        datatype = GL_FLOAT
        normalized = GL_FALSE #GL_TRUE
        fsize = np.float32(0.0).nbytes #to ensure namespace-safe.
        
        VAO = glGenVertexArrays(1) # create a VA. if 3, 3of VA got.
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
                glVertexAttribPointer(attr_index, size, datatype, normalized, stride * fsize, offset)
                glEnableVertexAttribArray(attr_index)
                pre_offset = size    
            else:
                offset = ctypes.c_void_p( pre_offset *fsize)
                glVertexAttribPointer(attr_index, size, datatype, normalized, stride * fsize, offset)
                glEnableVertexAttribArray(attr_index)
                pre_offset +=size
            
        self.VAO = VAO
        self.VBO = VBO
        self.EBO = EBO
        #self.mode = GL_TRIANGLES some model drawn lines kind thing requires not use it.
        self.stride = stride
        self.points = len(indices)
    def update(self,vertices):
        """requires same shape kinds.."""
        #assert self.points == len(vertices)//self.stride
        VAO = self.VAO
        VBO = self.VBO
        glBindVertexArray(VAO)
        glBindBuffer(GL_ARRAY_BUFFER, VBO) #gpu bind VBO in VAO
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        #GL_STREAM_DRAW for little change, if you want someday..
        self.points = len(vertices)//self.stride

    def update_indices(self,vertices, indices):
        """hope we not use this.."""
        VAO = self.VAO
        VBO = self.VBO
        EBO = self.EBO
        glBindVertexArray(VAO)
        glBindBuffer(GL_ARRAY_BUFFER, VBO) #gpu bind VBO in VAO
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)
        self.points = len(indices)#now we can really change it..

    def bind(self):
        glBindVertexArray(self.VAO)
    def unbind(self):
        glBindVertexArray(0)

    def draw(self, MODE = GL_TRIANGLES):
        """requires bind first. it just draw command of VAO bound gpu."""
        #simple mode changeable draw. we not prefer partial draw which is slow.
        glBindVertexArray(self.VAO)
        glDrawElements(MODE, self.points, GL_UNSIGNED_INT, None)


vaoidx = VAO_Indexed( {0:3,1:2},
    #np.array([0,0,0, 0,0,  0.5,0,0, 1,0,  0.5,0.5,0, 1,1,  0,0.5,0, 0,1, ]).astype('float32'),
    #np.array([0,0,0, 0,0,  1,0,0, 1,0,  1,1,0, 1,1,  0,1,0, 0,1, ]).astype('float32'),
    np.array([ [0,0,0, 0,0],  [1,0,0, 1,0],  [1,1,0, 1,1],  [0,1,0, 0,1] ]).astype('float32'),
    np.array([0,1,2,0,2,3,]).astype('uint')
    )


vaoidx.draw()
#print( vaoidx.points )
vaoidx.update( np.array([ [0,0,0, 0,0],  [1,0,0, 1,0],  [1,1,0, 1,1],  [0,1,0, 0,1] ]).astype('float32') )
vaoidx.update_indices(
    np.array([ [0,0,0, 0,0],  [1,0,0, 1,0],  [1,1,0, 1,1],  [0,1,0, 0,1] ]).astype('float32') ,
    np.array([0,1,2,0,2,3,]).astype('uint')
    )



#=============================== MESH DATA




#=============================== TEXTURE
from PIL import Image

class Texture:
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

    def __init__(self,width,height, MIPMAP = False, FORMAT = GL_RGB):
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
        self.TEXTURE = texture
        self.width = width
        self.height = height

        glBindTexture(GL_TEXTURE_2D, 0)

    def update(self,data):
        """img fliped internally."""
        tmpdata = np.empty_like(data)
        np.copyto(tmpdata,data[::-1,:])#fliped.fine.

        glBindTexture(GL_TEXTURE_2D, self.TEXTURE)
        #level mipmap.
        glTexSubImage2D(GL_TEXTURE_2D, 0, 0, 0, self.width, self.height, self.FORMAT, GL_UNSIGNED_BYTE, tmpdata )
        if self.MIPMAP:
            glGenerateMipmap(GL_TEXTURE_2D)#dont forget it! we need this here, if use mipmap.
        #https://www.khronos.org/opengl/wiki/Common_Mistakes#Automatic_mipmap_generation
        #https://stackoverflow.com/questions/16165963/updating-opengl-mipmapped-texture
        glBindTexture(GL_TEXTURE_2D, 0)

    def bind(self):
        glBindTexture(GL_TEXTURE_2D, self.TEXTURE)
    def unbind(self):
        glBindTexture(GL_TEXTURE_2D, 0)

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
        im.save(f"{filename}.png")
        #im.save(filename, quality=95)# q 95 fine. default 75. jpg/bmp:5ms PNG:50ms
        #im.save('q100sub0.jpg', quality=100, subsampling=0)#for jpg (maybe) uncompressed.



texture =  Texture.byimg('texture2.jpg')
#print(texture)

npimg = texture.get_np()
#print(npimg.shape)
#Texture.save_png(npimg,'hahaha')


texture2 =  Texture(512,512)
dat = (np.random.rand(512*512*3)*255).reshape(512,512,3).astype('uint8')
texture2.update(dat)

texture3 = Texture.bynp(dat)


# texture =  Texture.byimg('texture2.jpg')
# texture =  Texture.bynp(npimg)
# texture =  Texture(width,height)

# texture =  Texture.load('texture2.jpg')

# npimg =  Texture.load('texture2.jpg')
# texture = Texture(npimg)

# npimg =  Texture.load('texture2.jpg')
# height,width,depth = npimg.shape
# texture = Texture(width,height)
# texture.update(npimg)

#=============================== TEXTURE



class FBO:
    @classmethod
    def save_img(self,filename):
        data = self.get_np()
        h,w,d = data.shape
        if d==4:
            data = data[:,:,0:3]
        im = Image.fromarray(data[::-1])
        im.save(filename, quality=95)# q 95 fine. default 75. jpg/bmp:5ms PNG:50ms
        #im.save('q100sub0.jpg', quality=100, subsampling=0)#for jpg (maybe) uncompressed.
        print(f"img saved {filename}")

    @classmethod
    def get_np(self):
        width,height = window.get_size()#hope window is the only window.. ...what if to another window's save??
        data = np.empty(width*height*4).reshape(height,width,4).astype('uint8')#hope it's fast enough.
        glReadPixels(0,0,width,height,GL_RGBA,GL_UNSIGNED_BYTE, data)#see it's for depth=4.
        #read a block of pixels from the frame buffer
        return data

    def __init__(self):
        1


#FBO.save_img('ham2.jpg')






import math
from pymatrix_mini import vec3,eye4, normalize,  mperspective,mortho,mlookat


class Camera:
    def __init__(self):
        self.pos = vec3(0,0,1)#little back from screen

        self.front = vec3(0,0,-1)#toward screen
        self.up = vec3(0,1,0)#usually always up.
        
        #self.yaw = -90# means LH, ..fine.
        self.yaw = math.degrees(math.asin(self.front.z))
        self.pitch = 0

        self.fov = 50
        self.fov_min = 4
        self.fov_max = 114
        
        self.window_ratio = window.width/window.height
        self.near = 0.1
        self.far = 1000

        self.sensitivity = 0.1

    def get_Projection(self):#was set_..
        fov = self.fov
        window_ratio = self.window_ratio
        near = self.near
        far = self.far            
        mprojection = mperspective(fov, window_ratio, near,far)
        return mprojection

    def get_View(self):
        eye = self.pos
        target = self.pos+self.front
        upV = self.up
        mview = mlookat(eye,target,upV)
        return mview
    
    #--------general input method
    def set_fov(self,value):
        if not value:return
        self.fov = clamp( self.fov+value, self.fov_min,self.fov_max)
    def move_forward(self, value):
        if not value:return
        self.pos += vec3(0,value,0)
    def move_right(self, value):
        if not value:return
        self.pos += vec3(value,0,0)

    def mouse_moveDXDY(self, dx,dy):
        #yaw LH rule, but works as we expect. use front, not yaw directly.
        yaw = self.yaw
        pitch = self.pitch

        dx *= self.sensitivity
        dy *= self.sensitivity        

        yaw += dx
        pitch += dy
        if (pitch > 89.0): #not pitch = max kinds.
            pitch = 89.0
        if (pitch < -89.0):
            pitch = -89.0
        
        #----------- fpscam, by yaw & pitch.
        #---note we do not use up-vector. it's just done by yaw,pitch.
        #since in view mat: target = cam.pos+cam.front
        front = vec3(0,0,0)
        front.x = math.cos(math.radians(yaw)) * math.cos(math.radians(pitch))
        front.y = math.sin(math.radians(pitch))
        front.z = math.sin(math.radians(yaw)) * math.cos(math.radians(pitch)) 
        
        #ssems normalized but do again..
        self.front = normalize(front)
        self.yaw = yaw
        self.pitch = pitch
        


class Camera_Ortho:
    def __init__(self):
        self.pos = vec3(0,0,1)#little back from screen

        self.front = vec3(0,0,-1)#toward screen
        self.up = vec3(0,1,0)
        
        self.ortho_scale = 1
        self.window_ratio = window.width/window.height
        self.near = 0.1
        self.far = 1000
    
    def get_Projection(self):#was set_..
        ortho_scale = self.ortho_scale
        width = self.window_ratio *ortho_scale
        height = ortho_scale
        near = self.near
        far = self.far        
        mprojection = mortho(-width,width,-height,height,near,far)
        #(left, right, bottom, top, near, far)
        return mprojection

    def get_View(self):
        eye = self.pos
        target = self.pos+self.front
        upV = self.up
        mview = mlookat(eye,target,upV)
        return mview


cam = Camera()
cam2 = Camera_Ortho()

#symbol to modifier,
#500ms for 1M, 100k, 50ms, 100, 0.05ms took. 0.005ms for each frames, maybe.
#30ms 1M raw loop, str in , 50ms.
# t=time()
# for i in range(1000_000):
#     modifiers = 272
#     #MODSTRING = pyglet.window.key.modifiers_string(modifiers)
#     #5 in (1,2,3,4,5,6,7,8) this also faster than a=(1,2,3,4,5,6,7,8)
#     #'aero' in 'aerighjeroihjeorthjareor'#this faster than a='aergareg'.wow..
# print(time()-t)
# exit()

def symbol_to_key(symbol, modifiers):
    """ translate keyboard,mouse input, to use directly keymap={'W':do_func}.


    :param symbol: keyboard,mouse button (not for the state of drag 1+4=5.)
    :param modifiers: CTRL(1st), LSHIFT only.
    :returns: key. W W+CTRL M_LEFT...
    """
    
    #======================symbol
    key = pyglet.window.key.symbol_string(symbol)
    #'1' if mouse button 1.  key.symbol_string(49) > "_1"
    
    #-----mouse buttons int 1,2,4    
    if symbol == 1:
        key = "M_LEFT"
    elif symbol == 2:
        key = "M_MIDDLE"
    elif symbol == 4:
        key = "M_RIGHT"
    
    #------keyboard number 48 0 57 9  
    elif 48 <= symbol <=57:            
        key = key[1]# '_0' to '0'
        #print(key,'seenumberkeyboard')

    #======================modifiers
    #simple mod. ctrl advantaged.
    #key.modifiers_string(65505)
    #'MOD_SHIFT|MOD_SCROLLLOCK|MOD_COMMAND|MOD_OPTION|MOD_FUNCTION'
    #MOD_SCROLLLOCK
    #print( pyglet.window.key.modifiers_string(modifiers) )

    #print('MOD_SCROLLLOCK' in pyglet.window.key.modifiers_string(modifiers) )
    #MOD_SHIFT|MOD_CTRL|MOD_ALT|MOD_NUMLOCK|MOD_SCROLLLOCK
    mod = ''
    #if modifiers & pyglet.window.key.LCTRL:
    #elif modifiers & pyglet.window.key.LSHIFT:
    MODSTRING = pyglet.window.key.modifiers_string(modifiers)#takes 50ms for 100k
    if "MOD_CTRL" in MODSTRING:
        mod = 'CTRL'
    elif "MOD_SHIFT" in MODSTRING:
        mod = 'SHIFT'
    if mod:
        #if not key in ("ESCAPE", ):
        key = f"{key}+{mod}"
    return key
    #we not use mouse drag. too complex. deal it as ordinary motion.
    #if buttons & pyglet.window.mouse.LEFT:
    #pass
    #pyglet.window.mouse.buttons_string(1)
    #'LEFT'
    # pyglet.window.mouse.LEFT

#--we use complex device class using threading, occurs event maybe. (or atleast holding values)
#xboxRstick = AxisDevice(2)
#phoneGyro = AxisDevice(3)


#badkeymap = {        'W': ('move_forward',1),
#OFF INV -1!
#juse all method, if value: . a line, fine.
keymap = {
        'W': 'move_forward(0.2)',
        'S': 'move_forward(-0.2)',
        #'S': 'move_forward-1',
        'D': 'move_right(0.2)',
        'A': 'move_right(-0.2)',
        'F': 'fire',
        'M_DXDY': 'mouse_moveDXDY(1)',

        'M_SCROLL_UP': 'set_fov(-5)',
        'M_SCROLL_DOWN': 'set_fov(5)',

        'J_LSTICK_Y': 'move_forward(0.1)',
        'J_LSTICK_X': 'move_right(-0.1)',
         }

#mouse_moveDXDY(1) is 2D input. 
#1. (ratio), delivers value.  if not value:return  if you want pressed only
#2. funcDXDY(1) specifys no a value value.
#func
#func(2.5)
#funcDXDY(1)


class InputLayer:
    """has window check. sends packed events to  Controller (2d,3d) """
    def __init__(self, controller):

        self.events = [] #eventList ..fast but not PEP8.  (list)-s (dict)_dict fine.
        
        #self.window_controller = Controller(target = window)
        self.controller = controller #controller for detecting event hit.
    
    def cast(self, key, value):
        event = (key,value)
        self.events.append(event)
        #+ J_X
        #+ J_X_MOTION can be here.fine.

    def cast_axis(self, x,y, z=None, key="M_XY"): #M_DXDY_MOTION if locked.
        """ axis: means ,,axis related inputs. +2 axis.
        _MOTION:occurs lots of time. we gether and occur once a frame.

        mouse key default = M_XY
        mouse key manytime = M_XY_MOTION
        mouse key manytime(locked)= M_DXDY_MOTION

        2axis,z=None. if 3axis, z=0 atleast."""
        # DEVICE_AXIS(_IFMOTION)
        # M_XY
        # M_XY_MOTION
        # M_DXDY
        # M_DXDY_MOTION
        # J_DPAD_XY
        # J_DPAD_XY_MOTION        
        if z==None:
            event = (key, (x,y) )
        else:
            event = (key, (x,y,z) )
        self.events.append(event)

    def update(self,dt):
        motion_dict={}
        key_events=[]
        deliver_pack = []

        events = self.events
        self.events=[]
        
        for event in events:
            key,value = event
            #--------------------------- _MOTION: for many time occur event.
            if key[-7:] == '_MOTION':
                #device_name = key.split('_MOTION')[0] #touch_54_MOTION
                device_name = key[:-7]
                
                if isinstance(value,tuple):
                    lenval = len(value)
                    if lenval==2:
                        x,y = value
                    elif lenval==3:
                        x,y,z = value
                else:
                    lenval=1
                    x = value                    

                if not motion_dict.get(device_name):
                    if lenval==1:motion_dict[device_name] = 0
                    elif lenval==2:motion_dict[device_name] = (0,0)
                    elif lenval==3:motion_dict[device_name] = (0,0,0)

                if device_name == "M_DXDY":
                    _x,_y = motion_dict[device_name]
                    motion_dict[device_name] = (_x+x, _y+y)                    
                else:
                    if lenval==1:motion_dict[device_name] = x #this can be happened. not tuple.
                    elif lenval==2:motion_dict[device_name] = (x,y)
                    elif lenval==3:motion_dict[device_name] = (x,y,z)

            else:#not motion =>direct append key-value[0-1].
                key_events.append(event)


        def add_event(key,value):
            event = key,value
            deliver_pack.append(event)

        for key, value in motion_dict.items():#value (x,y) or (x,y,z) from _MOTION
            if key == "M_DXDY":
                x,y = value
                add_event("M_DX",x)
                add_event("M_DY",y)
            
            elif key[-3:]=='_XY':
                name = key[:-3]
                x,y = value
                add_event(f"{name}_X",x)
                add_event(f"{name}_Y",y)                
            elif key[-4:]=='_XYZ':
                name = key[:-4]
                x,y,z = value
                add_event(f"{name}_X",x)
                add_event(f"{name}_Y",y)
                add_event(f"{name}_Z",z)
            add_event(key,value)

        deliver_pack.extend(key_events)
        self.controller.deliver(deliver_pack)


class Controller:
    #__getattribute__ is for internal . 1st override, while getattr occurs if not exist.
    #use getattr for __var
    def __init__(self, target=None):
        self.targets = []
        if target:self.targets.append(target)

    def set_target(self, target_s):
        if isinstance(target_s, list):
            self.targets = target_s
        else:
            self.targets = [target_s]
    def add_target(self, target):
        self.targets.append(target)

    def deliver(self, events):
        for event in events:
            for target in self.targets:
                key,value = event

                funcname = target.keymap.get(key,'xXxXxX')

                if funcname[-1] == ")":
                    ridx = funcname.find("(")
                    if not ridx == -1:
                        mixer = funcname[ridx:]
                        mixer = float(mixer[1:-1])
                        funcname = funcname[:ridx]
                else:
                    value = None

                func = getattr(target, funcname, False)
                if func:
                    if value==None:# 0==False
                        escape = func()
                    else:
                        if not isinstance(value,tuple):
                            value *= mixer
                            escape = func(value)
                        else:
                            lenval = len(value)
                            if lenval==2:
                                x,y = value
                                x*=mixer
                                y*=mixer
                                escape = func(x,y)
                            elif lenval==3:
                                x,y,z = value
                                x*=mixer
                                y*=mixer
                                z*=mixer
                                escape = func(x,y,z)                    
                    if escape:break # we skip to check next target



class PlayerController(Controller):
    """ Controller that has player(human) methods."""
    def __init__(self):
        super().__init__()



mycontroller = PlayerController()
mycontroller.add_target(window)
cam.keymap = keymap
mycontroller.add_target(cam)

inputlayer = InputLayer(mycontroller)
#inputlayer.controller = mycontroller

#inputlayer.controller.set_target(cam)
#inputlayer.controller.target = cam



#controller = cam

#jlhat = AxisDevice("J_LSTICK")
#inputlayer.add_AxisDevice(jlhat)


#touch drag device created each touch.
#controller.isdrag = True
#controller.axisdeviceDict[ID].isdrag=True 
#if drag_end: controller.axisdeviceDict.pop(ID)


# e = InputEvent("mouse",key,1,x,y, dx=dx,dy=dy)
# inputlayer.cast(ID, key,value)

# #inputlayer.castAxis(ID, key,value, x,y,dx,dy)
# inputlayer.cast(ID, key,value)
# inputlayer.castAxis(ID, key, x,y,dx,dy)

# inputlayer.castAxis(ID, key, x,y,z,dx,dy,dz)

# for event in eventList:
#     if type=="key":
#         deliver(key)
#     elif type=='axis':
#         axisDict[ID][x] += x
        
#         axisDevice[ID].x+=x
#         axisDevice[ID].y+=y

# for key in keyboard:
#     deliver(key)

# for event in mouse:
#     if event==key
#     elif event==move 

# [
#  ID key value
#  ID key value x,y,
#  ]


# if changed, add event
# if type == move:
#     axis[ID][x]+=X
#     axis[ID][x]+=y


#=====================================KEY EVENT
@window.event
def on_key_press(symbol,modifiers):
    key = symbol_to_key(symbol,modifiers)
    inputlayer.cast(key,1)
@window.event      
def on_key_release(symbol, modifiers):
    key = symbol_to_key(symbol,modifiers)
    inputlayer.cast(key,0)
#=====================================MOUSE EVENT
@window.event
def on_mouse_press(x, y, button, modifiers):
    key = symbol_to_key(button,modifiers)
    if not window.ismouselock:inputlayer.cast_axis(x,y)
    inputlayer.cast(key,1)
@window.event
def on_mouse_release(x, y, button, modifiers):
    key = symbol_to_key(button,modifiers)
    if not window.ismouselock:inputlayer.cast_axis(x,y)
    inputlayer.cast(key,0)
@window.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    if scroll_y>0:#up
        key = "M_SCROLL_UP"
    elif scroll_y<0:
        key = "M_SCROLL_DOWN"
    if not window.ismouselock:inputlayer.cast_axis(x,y)
    inputlayer.cast(key,1)

@window.event
def on_mouse_motion(x, y, dx, dy):
    """motion and broadcasted once a frame"""
    if not window.ismouselock:
        inputlayer.cast_axis(x,y, key = "M_XY_MOTION")
    else:
        inputlayer.cast_axis(dx,dy, key = "M_DXDY_MOTION")
@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):#ah, maybe when clicked, motion not occur but this.
    #drag is pressed move. assume it move, for simple way!
    if not window.ismouselock:
        inputlayer.cast_axis(x,y, key = "M_XY_MOTION")
    else:
        inputlayer.cast_axis(dx,dy, key = "M_DXDY_MOTION")

#thread, class, class runs thread, stores class attribute.. and cast to inputlayer
#and inputlayer has casted event.fine.

#class Gyroweb:
#g=Gyroweb()
#g.castto = inputlayer
#g.threadrun() --casts to inputlayer

#--update
#joystick.x
#joystick.LEFTXY

# @joysticks
# def on_leftxy:
#     inputlayer.castAxis(ID = "J_LSTICK", x,y)
# @joysticks
# def on_rightxy

# @joysticks
# def on_leftkey

# @joysticks
# def on_key

#https://pyglet.readthedocs.io/en/latest/modules/input.html#pyglet.input.Joystick.on_joybutton_press
joysticks = pyglet.input.get_joysticks()
if joysticks:
    joystick = joysticks[0]
    joystick.open()

    #mousemapping
    #joystickmapping
    joystickmapDict = {
    0:'J_A',
    1:'J_B',
    2:'J_X',
    3:'J_Y',
    4:'J_L1',
    5:'J_R1',
    6:'J_SELECT',
    7:'J_START',
    8:'J_L3',
    9:'J_R3',

    'x':'J_X',
    'y':'J_X',
    'rx':'J_RX',
    'ry':'J_RX',

    'z':'J_L2',
    }

    @joystick.event
    def on_joybutton_press(joystick, button):
        #print(joystick,button)#A B X Y L R selstart LhatRhat 012345 67 89
        key = joystickmapDict.get(button, "unknown")
        print(key)
        #inputlayer.cast(key, 1)
        pass

    @joystick.event
    def on_joybutton_release(joystick, button):
        key = joystickmapDict.get(button, "unknown")
        print(key)
        #inputlayer.cast(key, 0)
        pass

    @joystick.event
    def on_joyaxis_motion(joystick, axis, value):
        print(axis,value) #x,y or rx,ry up -1. Z L1 R-1 0.
        key = joystickmapDict.get(axis, "unknown")
        #inputlayer.cast(key, value)
        pass
    @joystick.event
    def on_joyhat_motion(joystick, hat_x, hat_y):
        #print(hat_x,hat_y,'hat')#cross key R UP 1,1
        inputlayer.cast_axis(hat_x, hat_y, key='J_DPAD_XY_MOTION')
        pass


# def on_joy_motion(x,y):
#     inputlayer.castAxis(ID = "JOYSTICK", x,y)

# def on_touch(ID, x,y):
#     #inputlayer.castAxis(ID = ID, x,y)
#     inputlayer.castAxis(ID = f"TOUCH_{ID}", x,y)

# def on_button(ID, x,y):
#     key = "J_Y"
#     inputlayer.cast(key,state)


#https://pyglet.readthedocs.io/en/latest/modules/input.html#pyglet.input.Joystick.on_joybutton_press


#we hold .. idontwantit.

def update(dt):
    if not dt==0:
        1
        #print(1/dt)
    #jlhat.cast(joystick.y)
    #inputlayer.cast_axis(ID = jlhat.ID, x=joystick.x, y = joystick.y)
    #print(joystick.x,joystick.y) #works great!
    
    eventpack = inputlayer.update(dt)#see what happens
    #eventpack = aicontrollerCV.update(dt)
    #playercontroller.deliver(eventpack)
    playercontroller.deliver(eventpack)

    UIlayer.update(dt)
    world.update(dt)
    #and draw


#pyglet.clock.schedule(update)
pyglet.clock.schedule_interval(update, 0.01) 


class World:
    def __init__(self):
        pass
    def update(self, dt):
        print(dt)
    def set_camer(self, ID):
        camera = self.cameraDict.get(ID)
        if camera !=None:
            projectionmat = camera.get_Projection()
            viewmat = camera.get_View()
            shader.set_Projection(projectionmat)
            shader.set_View(viewmat)


class UIWorld(World):
    """ it's for 2d layer, same structure, has UI componants. has orthogonal cam."""
    def __init__(self):
        super().__init__()


#------update loop
#0. keyboard, mouse, kinds event -> inputLayer.

#1. polling input device. set value.  including mouse xy.(if they moved.)
#2. inputManager, (window first), to controller. 2d layer is also an controlled system.
#3. update by input
#4. update by physics simulation
#5. draw

#UILayer.
#world

#world.cam1



@window.event
def on_draw():
    gldraw()

#@profile
def gldraw():
    #glClear(GL_COLOR_BUFFER_BIT)
    glClearColor(0.0, 0.24, 0.5, 1.0)
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

    #program = default_shader
    #glUseProgram(program)
    shader.bind()

    camera = cam
    # fov = camera.fov
    # window_ratio = camera.window_ratio
    # near = camera.near
    # far = camera.far
    # projectionmat = mperspective(fov, window_ratio, near,far)
    
    # eye = camera.pos
    # target = camera.pos+camera.front
    # upV = camera.up
    # viewmat = mlookat(eye,target,upV)
    
    
    projectionmat = camera.get_Projection()
    viewmat = camera.get_View()
    modelmat = eye4()

    #projectionmatID = glGetUniformLocation(program, "Projection")
    #viewmatID = glGetUniformLocation(program, "View")
    #modelmatID = glGetUniformLocation(program, "Model")
    #glUniformMatrix4fv(projectionmatID,1,False, projectionmat)
    #glUniformMatrix4fv(viewmatID,1,False, viewmat)
    #glUniformMatrix4fv(modelmatID,1,False, modelmat)# True for row major.ha.[1,2,3,4, ,]
    shader.set_Projection(projectionmat)
    shader.set_View(viewmat)
    shader.set_Model(modelmat)


    #glBindVertexArray(vaocart.VAO)
    #glBindTexture(GL_TEXTURE_2D, texture)
    #glDrawElements(GL_TRIANGLES, vaocart.size, GL_UNSIGNED_INT, None)
    #glDrawArrays(GL_TRIANGLES, 0, vaocart.size) #mode first count

    texture.bind()

    vaoidx.bind()
    vaoidx.draw()
    #FBO.save_img('ham2.jpg')

pyglet.app.run()
