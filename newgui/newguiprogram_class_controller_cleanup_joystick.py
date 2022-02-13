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

#=============================== WINDOW
#window setting must be first, later gl settings.

#window = pyglet.window.Window()
#WINDOW_WIDTH = 800
#WINDOW_HEIGHT = 600
#window.set_size(WINDOW_WIDTH, WINDOW_HEIGHT)
#window.set_exclusive_mouse(True) #lock mouse x,y 0, hold. use dxdy then!
#window.set_vsync(False) #for maximum fps

#Win32Window
class Window(pyglet.window.Window):
    def __init__(self):
        super().__init__(800,600) #0-799, 1-600
        #self.set_size(500, 300)#need init resizable=True
        #self.get_framebuffer_size()
        #print(self.width,self.height)
        #print(window.get_size())
        #self.set_exclusive_mouse(True)
        self.set_vsync(False)        
        self.keymap = {'T': 'mouse_lock', 'ESCAPE': 'close'}
        self.ismouselock = False
        
        def on_key_press(symbol,modifiers):
            #print(symbol)
            #print(pyglet.window.key.symbol_string(symbol))
            pass
        self.on_key_press = on_key_press

    def close(self,value=None):#alt f4 error fixed.
        super().close()
    def mouse_lock(self,value):
        if not value:return#works great.
        self.ismouselock = not self.ismouselock
        self.set_exclusive_mouse(self.ismouselock)

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

    def mouse_move(self, dx,dy):
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
        print(key,'seenumberkeyboard')

    #======================modifiers
    #simple mod. ctrl advantaged.
    #key.modifiers_string(65505)
    #'MOD_SHIFT|MOD_SCROLLLOCK|MOD_COMMAND|MOD_OPTION|MOD_FUNCTION'
    mod = ''
    if modifiers & pyglet.window.key.LCTRL:
        mod = 'LCTRL'
    elif modifiers & pyglet.window.key.LSHIFT:
        mod = 'LSHIFT'
    if mod:
        key = f"{key}+{mod}"
    return key
    #we not use mouse drag. too complex. deal it as ordinary motion.
    #if buttons & pyglet.window.mouse.LEFT:
    #pass
    #pyglet.window.mouse.buttons_string(1)
    #'LEFT'
    # pyglet.window.mouse.LEFT


class AxisDeviceDX:
    """for custom device which has axis of 2 or 3. value simulatanously inserted"""
    ID = 0
    def __init__(self, name, axis=2):
        self.axis = axis
        self.name = name
        self.ID = AxisDeviceDX.ID
        AxisDeviceDX.ID+=1

        self.x = 0
        self._x = 0
        self.y = 0
        self._y = 0
        self.dx = 0
        self.dy = 0
        self.z = 0
        self._z = 0
        self.dz = 0

    def __repr__(self):
        return f"an axis {self.axis} device"

    def cast(self, x=None,y=None,z=None, dx=None,dy=None,dz=None):
        if x!=None: self.x = x
        if y!=None: self.y = y
        if dx!=None: self.dx += dx
        if dy!=None: self.dy += dy
        if z!=None: self.z = z
        if dz!=None: self.dz += dz

    def update(self):#not using dx now.
        eventList = []
        
        x = self.x
        y = self.y
        z = self.z
        dx = x - self._x
        dy = y - self._y
        dz = z - self._z
        if dx!=0 or dy!=0 or dz!=0:
            def addevent(adder,value):
                key = self.name+adder
                event = (key,value)
                eventList.append(event)
            
            if self.axis==2:
                addevent( "_XY", (x,y) )
                addevent( "_X", x )
                addevent( "_Y", y )
                
                addevent( "_DXDY", (dx,dy) )
                addevent( "_DX", dx )
                addevent( "_DY", dy )
            elif self.axis==3:
                addevent( "_XYZ", (x,y,z) )
                addevent( "_X", x )
                addevent( "_Y", y )
                addevent( "_Z", z )

                addevent( "_DXDYDZ", (dx,dy,dz) )
                addevent( "_DX", dx )
                addevent( "_DY", dy )
                addevent( "_DZ", dz )

        self._x = x
        self._y = y
        self._z = z
        return eventList



class AxisDevice:
    """for custom device which has axis of 2 or 3. value simulatanously inserted"""
    ID = 0
    def __init__(self, name, axis=2):
        self.axis = axis
        self.name = name
        self.ID = AxisDevice.ID
        AxisDevice.ID+=1

        self.x = 0
        self.y = 0
        self.z = 0
        self._x = 0
        self._y = 0
        self._z = 0

    def __repr__(self):
        return f"an axis {self.axis} device"

    def cast(self, x=None,y=None,z=None):
        if x!=None: self.x = x
        if y!=None: self.y = y
        if z!=None: self.z = z

    def update(self):#not using dx now.
        eventList = []
        
        x = self.x
        y = self.y
        z = self.z
        dx = x - self._x
        dy = y - self._y
        dz = z - self._z
        #if dx!=0 or dy!=0 or dz!=0:
        def addevent(adder,value):
            key = self.name+adder
            event = (key,value)
            eventList.append(event)
        
        if self.axis==2:
            addevent( "_XY", (x,y) )
            addevent( "_X", x )
            addevent( "_Y", y )
        elif self.axis==3:
            addevent( "_XYZ", (x,y,z) )
            addevent( "_X", x )
            addevent( "_Y", y )
            addevent( "_Z", z )

        self._x = x
        self._y = y
        self._z = z
        return eventList



#xboxLstick = AxisDevice(2)
#xboxRstick = AxisDevice(2)
#phoneGyro = AxisDevice(3)


badkeymap = {
        'W': ('move_forward',1),
        'WOFF': ('move_forward',0),
        'S': ('move_forward',-1),
        'SOFF': ('move_forward',0),
        'J_LSTICK_Y': ('move_forward',1),
        'F': ('fire',),
         }

#OFF INV -1!
#juse all method, if value: . a line, fine.
keymap = {
        'W': 'move_forward(0.2)',
        'S': 'move_forward(-0.2)',
        #'S': 'move_forward-1',
        'D': 'move_right(0.2)',
        'A': 'move_right(-0.2)',
        'F': 'fire',
        'M_DXDY': 'mouse_move',

        'M_SCROLL_UP': 'set_fov(-5)',
        'M_SCROLL_DOWN': 'set_fov(5)',

        'J_LSTICK_Y': 'move_forward(0.1)',
        'J_LSTICK_X': 'move_right(-0.1)',
         }


class InputLayer:
    def __init__(self,window, controller):
        window = window#has .keymap
        #self.layerList = [window, layer, controller]
        
        self.window = window
        self.controller = controller
        self.layerList = [window, controller]
        self.eventList = []

        self.x =0
        self.y =0
        self._x =0
        self._y =0
        self.dx=0
        self.dy=0

        self.axisDeviceDict={}

    def add_AxisDevice(self,ad):
        self.axisDeviceDict[ad.ID]=ad

    def update(self):
        mouseEventList = self.update_mouse()
        axisEventList = self.update_axis()
        allEventList = []
        allEventList.extend(mouseEventList)
        allEventList.extend(axisEventList)

        allEventList.extend(self.eventList)
        self.eventList = []

        for event in allEventList:
            for layer in self.layerList:
                key,value = event                
                funcname = layer.keymap.get(key,'xXxXxX')

                #if funcname[-2:] == '-1':
                #    funcname = funcname[:-2]
                #    value *= -1
                if funcname[-1] == ")":
                    ridx = funcname.find("(")
                    if not ridx == -1:
                        mixer = funcname[ridx:]
                        mixer = float(mixer[1:-1])
                        funcname = funcname[:ridx]
                        value *= mixer

                #if hasattr(layer, funcname):
                func = getattr(layer, funcname, False)
                if func:
                    if isinstance(value,tuple):
                        if len(value)==2:
                            x,y = value
                            func(x,y)
                        elif len(value)==3:
                            x,y,z = value
                            func(x,y,z)
                    else:
                        func(value)
                    break

    def cast_button(self, key, value):
        #if value == 0:            key+="OFF" use just if value check.fine. easy coding & 2x overhead
        event = (key,value)
        self.eventList.append(event)

    def cast_mouse(self, x,y, dx=0, dy=0):
        self.x =x
        self.y =y
        self.dx+=dx
        self.dy+=dy        

    def cast_axis(self, ID, x=None,y=None,z=None, dx=None,dy=None,dz=None):
        axisdevice = self.axisDeviceDict.get(ID,None)
        if axisdevice==None:
            print(f'no AxisDevice ID of {ID}')
        else:
            #axisdevice.cast(x,y,z,dx,dy,dz)
            axisdevice.cast(x,y,z)
    
    def update_mouse(self):
        eventList = []

        x = self.x
        y = self.y

        if self.window.ismouselock:
            dx = self.dx
            dy = self.dy
            if dx!=0 or dy!=0:
                def addevent(key,value):
                    event = (key,value)
                    eventList.append(event)
                addevent("M_DXDY", (dx,dy) )
                addevent("M_DX", dx )
                addevent("M_DY", dy )
        else:
            dx = x - self._x
            dy = y - self._y
            if dx!=0 or dy!=0:
                def addevent(key,value):
                    event = (key,value)
                    eventList.append(event)
                addevent("M_XY", (x,y) )
                addevent("M_X", x )
                addevent("M_Y", y )

        self._x = x
        self._y = y
        self.dx=0#or too massive value
        self.dy=0

        return eventList

    def update_axis(self):
        axisEventList = []
        for device in self.axisDeviceDict.values():
            eventList = device.update()
            axisEventList.extend(eventList)
        return axisEventList

cam.keymap = keymap
controller = cam

inputlayer = InputLayer(window, controller)

jlhat = AxisDevice("J_LSTICK")
inputlayer.add_AxisDevice(jlhat)

#def get_tabdrag(): inputlayer.cast_axis(4,x,y)
#def get_tabdrag(): inputlayer.cast_axis(ID=4,x=x,y=y)
#def get_gyro(): inputlayer.cast_axis(3,x,y,z)
#def get_gyro(): inputlayer.cast_axis(ID=3,x=x,y=y,z=z)

#touch drag device created each touch.
#controller.isdrag = True
#controller.axisdeviceDict[ID].isdrag=True 
#if drag_end: controller.axisdeviceDict.pop(ID)

#=====================================KEY EVENT
@window.event
def on_key_press(symbol,modifiers):
    key = symbol_to_key(symbol,modifiers)
    inputlayer.cast_button(key,1)
@window.event      
def on_key_release(symbol, modifiers):
    key = symbol_to_key(symbol,modifiers)
    inputlayer.cast_button(key,0)

#=====================================MOUSE EVENT
@window.event
def on_mouse_press(x, y, button, modifiers):
    key = symbol_to_key(button,modifiers)
    inputlayer.cast_mouse(x,y)
    inputlayer.cast_button(key,1)
@window.event
def on_mouse_release(x, y, button, modifiers):
    key = symbol_to_key(button,modifiers)
    inputlayer.cast_mouse(x,y)
    inputlayer.cast_button(key,0)    
@window.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    if scroll_y>0:#up
        key = "M_SCROLL_UP"
    elif scroll_y<0:
        key = "M_SCROLL_DOWN"
    inputlayer.cast_mouse(x,y)
    inputlayer.cast_button(key,1)

@window.event
def on_mouse_motion(x, y, dx, dy):
    """motion and broadcasted once a frame"""
    inputlayer.cast_mouse(x,y,dx,dy)

@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):#ah, maybe when clicked, motion not occur but this.
    #drag is pressed move. assume it move, for simple way!
    inputlayer.cast_mouse(x,y,dx,dy)


#https://pyglet.readthedocs.io/en/latest/modules/input.html#pyglet.input.Joystick.on_joybutton_press
joysticks = pyglet.input.get_joysticks()
if joysticks:
    joystick = joysticks[0]
joystick.open()

#we hold .. idontwantit.
def on_joybutton_press(joystick, button):
    print(joystick,button)
    pass



def update(dt):
    if not dt==0:
        1
        #print(1/dt)
    #jlhat.cast(joystick.y)
    inputlayer.cast_axis(ID = jlhat.ID, x=joystick.x, y = joystick.y)
    inputlayer.update()
    #print(joystick.x,joystick.y) #works great!
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
