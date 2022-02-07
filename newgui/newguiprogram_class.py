from time import time, sleep
import numpy as np


import pyglet
#from pyglet.gl import * #we don't use it!

from OpenGL.GL import *
from OpenGL.GL import shaders

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

    def mouse_lock(self):
        self.set_exclusive_mouse(True)
    def mouse_unlock(self):
        self.set_exclusive_mouse(False)

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
        
        self.window_ratio = window.width/window.height
        self.near = 0.1
        self.far = 1000

        self.sensitivity = 0.1

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
    
    def move_forward(self, ispress):
        if ispress:
            self.pos += vec3(0,1,0)
            #self.spd = vec3(0,1,0)
        #else:
            #self.spd = 0
    def move_backward(self, ispress):
        if ispress:self.pos += vec3(0,-1,0)
    def move_left(self, ispress):
        if ispress:self.pos += vec3(-1,0,0)
    def move_right(self, ispress):
        if ispress:self.pos += vec3(1,0,0)


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



#-------------------------------controller
#InputHandler
#seems too,, eventHandler kinds.
#what about InputLayer??\
#..ithink inputhandler fine.
#input handler takes from event handler, from pyglet window..
#event has key button modifier kinds..

#see
#https://pyglet.readthedocs.io/en/latest/programming_guide/events.html
#https://pyglet.readthedocs.io/en/latest/modules/event.html

#InputController
#.. i think Controller need to be as controller, which has it's actor..
#whatif Controller have keymap, while actor has only methods?
#Controller expected to know info what to do. not just key.

#PlayerController input by player. player presses key.
#AIController input by ai. ai simulated press key.

#----------------structure
#pyglet window brings event func.. send        key modifier xy kinds       to  inputhandelr 
# inputhandelr  interpretes        key modfier xy kinds [pack]  >>> to each layer
# layer   
#  layer to       actor func(func name global shared. called API)



#from pyglet.window import key as PYGLETKEY

# txt, w:move_forward

keymap = {
    'W': 'move_forward',
    'S': 'move_backward',
    'A': 'move_left',
    'D': 'move_right',

    'W+LCTRL': 'move_forward_fast',
}


keymap_camera = {
    #--------key input ispress
    'W': 'move_forward',
    'S': 'move_backward',
    'A': 'move_left',
    'D': 'move_right',

    'W+LCTRL': 'move_forward_fast',
    
    #----------mouse ..note LEFT also of arrow.
    'M_LEFT': 'change_camera',
    'M_RIGHT': 'screenshot',
    'M_SCROLL_UP':'zoom_in',
    'M_SCROLL_DOWN':'zoom_out',

    #----------motion input x,y,dx,dy
    'M_MOTION':'mouse_move',
}

#func(ispress)
#func(x,y,dx,dy)

#MIDDLE
#pyglet.window.mouse.buttons_string(1)
#'LEFT'
# pyglet.window.mouse.LEFT

#for integrate mouse to pack_key. mouse act like key.

mousemap = {'1': 'M_LEFT', '2':'M_MIDDLE', '4':'M_RIGHT'}#hope all system same..

class Controller:#fianlly!
    def __init__(self):
        world=cam
        world.keymap = keymap
        self.layer = {0: world}
        #layer 0 1 2 3...
        #acutally level 0 is deeper ground, while lv8 is higher gui layer..
        # window MENU HUD 3D kinds..        
        # we create world.. which always level 0.

        #cam.keymap = keymap_camera#we attach like this. wonderful.
        #self.layer[9]=cam
        #=world ..yeah.world.

        self._x = 0
        self._y = 0
        self._dx = 0
        self._dy = 0

    def layer_add(self, layer):
        maxman = max(self.layer.keys())        
        self.layer[maxman+1] = layer
        #a[99] = a.pop(5) is maybe the way of ,,key change.

    #-----------------toomessy
    def layer_changeto(self, layeridx, to):
        if to in self.layer:
            print('layeridx already is!')
            return 0
        self.layer[to] = self.layer.pop(layeridx)
    def see(self):
        for key in self.layer:
            print(f"{key} : {self.layer[key]}")
    #-----------------toomessy

    def layer_hit(self, key):
        layerkeys = list( self.layer.keys() )
        layerkeys.sort( reverse = True) #lower first. >>higher first.
        for layerkey in layerkeys:
            layer = self.layer[layerkey]
            if key in layer.keymap.keys():#this means, 'hit'
                print('hit,',layerkey)
                return layer
        #---if no hit..
        return None

    def layer_run_key(self, layer, key, ispress ):#really good. see how it become simple..
        funcname = layer.keymap.get(key)
        try:
            func = getattr(layer, funcname)
        except:
            return#returns None
        func(ispress)#occurs err while run func.

    def layer_run_mouse(self, layer, key, x,y,dx,dy ):#really good. see how it become simple..
        funcname = layer.keymap.get(key)
        try:
            func = getattr(layer, funcname)
        except:
            return#returns None
        func(x,y,dx,dy)#occurs err while run func.


    def deliver_key(self, key, ispress):
        #--keep always filled atleast one layer.
        # if len(self.layer)==0:
        #     print('layer empty',key)
        #     return 0
        
        #----when list
        #for layer in self.layer:
        #    if key in layer.keymap.keys():
        #        break

        #----when dict
        #see: dict.popitem() leftpop. while pop(key) ..pops.fine.

        #-----phase1, get all layer, if hit, break. we got hit layer.
        layer = self.layer_hit(key)

        #-----assume layer was looping for..
        #-----phase2, get keymap, get func, run func.

        # if funcname in dir(layer):
        #     #layer.exec(funcname) we cannot do this..
        #     func = getattr(layer,funcname)#but this way! i love py!
        #     #key not delivered. key done it's duty , mapping.
        #     func(ispress) #send key, and ispress..better than just state.
        #     #this is method of a object, so it works great.
        #     print('done',funcname)
        if layer:
            self.layer_run_key(layer, key, ispress)

    def deliver_mouse(self, x,y,dx,dy):
        """simulate rough dx,dy mouse motion. + x,y. """
        #x,y 0 if mouse stuck.
        #see if 3d cursor firework. fine.
        key = 'M_MOTION'
        layer = self.layer_hit(key)
        
        #we dont know wherer cursor stuck. just give them all!
        if layer:
            self.layer_run_mouse(layer, key, x,y, dx,dy)#hope, if stuck, use dxdy, free cursor, use x,y.


    def xxxevent_motion(self, key, ispress):
        if len(self.layer)==0:
            print('layer empty',key)
            return 0
        #----when list
        #for layer in self.layer:
        #    if key in layer.keymap.keys():
        #        break

        #----when dict
        #see: dict.popitem() leftpop. while pop(key) ..pops.fine.
        layerkeys = list( self.layer.keys() )
        layerkeys.sort() #lower first.
        for layerkey in layerkeys:
            layer = self.layer[layerkey]
            if key in layer.keymap.keys():#this means, 'hit'
                break

        #-----assume layer was looping for..
        funcname = layer.keymap.get(key)
        if funcname in dir(layer):
            #layer.exec(funcname) we cannot do this..
            func = getattr(layer,funcname)#but this way! i love py!

            #key not delivered. key done it's duty , mapping.
            func(ispress) #send key, and ispress..better than just state.
            print('done',funcname)


    def pack_key(self, ispress, symbol,modifiers ):
        """ispress T/F, symbol mod directly."""
        #key.symbol_string(49)
        key = pyglet.window.key.symbol_string(symbol)# '1' if mouse button 1.

        #int 1 2 4 LEFT MIDDLE RIGHT. for flag bit..
        #pyglet.window.mouse.buttons_string(1)
        #pyglet.window.mouse.LEFT
        #if key in ('1','2','4'):
        #    key = pyglet.window.mouse.buttons_string( int(key) )
        #we have arrow's LEFT. we need mousemap.        
        if key in mousemap.keys():
            key = mousemap[key]#fine.
        
        #if key in ('_0','_1','_2','_3','_4','_5','_6','_7','_8','_9'): #maybe slow?? ,,whatever!
        #    key = key[1]

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
        self.deliver_key( key, ispress)

    def pack_mouse_key(self, ispress, x,y,button,modifiers):
        #this maybe useful when click, touch event. not occured motion..
        self._x = x
        self._y = y
        #symbol = mousemap[str(button)]# why int!huh. Nth..fine.
        self.pack_key( ispress, button, modifiers) # wow. thats why _1 and 1.
        #we need deiver x,y coordinates.. or set internal _x, _y. not bad..        
    
    def pack_mouse_scroll(self, x, y, scroll_x, scroll_y):
        if scroll_y>0:
            key = "M_SCROLL_UP"
        else:
            key = "M_SCROLL_DOWN"
        ispress = True
        self.pack_key( ispress, key, modifiers)
        
    
    #-------------------------mouse motion
    def pack_mouse_motion(self, x,y,dx,dy):
        """motion too frequent.
        it just updates internal value. to activate: self.update"""
        self._x = x
        self._y = y
        #---maybe dx is too ..unstable...? i don know yet. we didnot test it..
        #---no. see pyglet 24.1 VAO imporeivpotitdw , it += dxdy , fine.
        self._dx += dx
        self._dy += dy
        #self.mouse_motion(x,y)# too frequent! we maybe update it.. grab changed.. add _dx+=dx..
        #print(x,y)
        #--------------assume we drive plane.. ..plane actually grabs current _x
    
    #was mouse_tick. anyway do inside of .update
    def tick(self):
        """since mouse motion too frequent_even 300s /seconds. do it in inf. fast update loop."""
        #we have _dx witch large powered.
        #but acutally we already changed _x, the position.
        #so.. we don't need dx, but x - x_before??
        x = self._x
        y = self._y

        dx = self._x - self._x_before
        dy = self._y - self._y_before
        self._x_before = self._x
        self._y_before = self._y

        #-hope we not use it... OH, when mouse stuck, this is the only way move.
        dx2 = self._dx
        dy2 = self._dy
        self._dx = 0
        self._dy = 0

        self.deliver_mouse(x,y,dx2,dy2)

        #----------------------we have x,y,dx,dy. send to mouse event kinds..

        #compare below.
        #dx = self.mouseX - self.mouseX_before
        #dy = self.mouseY - self.mouseY_before
        #self.mouseX_before = self.mouseX
        #self.mouseY_before = self.mouseY
        #cam.mouse_move(dx,dy)

controller = Controller()

#controller


class ActorController:
    def __init__(self):
        self.actor = None
        self.state = 0#state machine
        PAUSE = 0
        MOVE = 1
        ATTACK = 2
    def map(self):
        actor = self.actor
        keymap = actor.keymap
        funcname = keymap.get("w")
        func = getattr(actor,funcname)
        func()
    def attack(self, target):
        actor = self.actor

    def move(self, vec3):
        actor = self.actor

# user input  >>  Controller  >>  PlayerController  >>  actor.keymap  >>  actor
class PlayerController:
    def __init__(self):
        self.actor = None
        self.state = 0#state machine
        PAUSE = 0
        MOVE = 1
        ATTACK = 2
    
    #def map(self, key):
    def map(self, key, ispress=None, level=None):
        actor = self.actor
        keymap = actor.keymap
        funcname = keymap.get(key, "__str__")
        func = getattr(actor,funcname)
        func(ispress,level)#hope None gose None..

    def act(self, key):
        self.map(key)

# func()
# func(ispress)
# func(ispress, ratio)#value level ratio ...
# func(*args)
# func(**kwargs)
# #(ispress=None, level=None)
# kwargs = {'ispress':ispress, 'level':level,}

#----i love py 2. we can send arg None as None. nothing happens.
def hoho(aa=None,bb=None):
    print('')
hoho(None,None)


class AIController:
    1

#tell ai to press w!
#=====================================MOUSE EVENT
@window.event
def on_mouse_motion(x, y, dx, dy):
    controller.pack_mouse_motion(x,y,dx,dy)

#pyglet.window.mouse.buttons_string(1)
#'LEFT'
# pyglet.window.mouse.LEFT
# pyglet.window.mouse.MIDDLE
# pyglet.window.mouse.RIGHT
@window.event
def on_mouse_scroll(x, y, scroll_x, scroll_y):
    controller.pack_mouse_scroll( x, y, scroll_x, scroll_y)
    #yup to up, 1.0, sx most devices 0.

@window.event
def on_mouse_drag(x, y, dx, dy, buttons, modifiers):
    controller.pack_mouse_drag( x, y, dx, dy, buttons, modifiers )
    #if buttons & pyglet.window.mouse.LEFT:
        #pass
# def on_mouse_enter(x, y):
#     pass
# def on_mouse_leave(x, y):
#     pass

@window.event
def on_mouse_press(x, y, button, modifiers):
    controller.pack_mouse_key(True, x,y,button,modifiers)   
@window.event
def on_mouse_release(x, y, button, modifiers):
    controller.pack_mouse_key(False, x,y,button,modifiers)
#=====================================KEY EVENT

@window.event
def on_key_press(symbol,modifiers):
    controller.pack_key(True,symbol,modifiers)
    # if symbol == key.W:
    #     cam.pos += vec3(0,1,0)
    # if symbol == key.S:
    #     cam.pos += vec3(0,-1,0)
    # if symbol == key.A:
    #     cam.pos += vec3(-1,0,0)
    # if symbol == key.D:
    #     cam.pos += vec3(1,0,0)
@window.event      
def on_key_release(symbol, modifiers):
    controller.pack_key(False,symbol,modifiers)

# --input event
# w-> cam.posx+=1
# ( for instance movement. not recommended.)
# w-> cam.spdx=1
# (requires update, preserved speed.)

# --update
# cam.update , cam.pos+=cam.spd
# (+ modeldata x+= 3..)



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
