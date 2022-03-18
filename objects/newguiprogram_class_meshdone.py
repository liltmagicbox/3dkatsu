import uuid
import random
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
#texture.TEXTURE. long but fine. since VAO VBO.. --- ID, ID_VBO. ID better.
#update usually changes data. note VAO.update_indices means +indices.

#ID UI all capital
#is_() get_() set_() ,,,not direct self.isValue = True
# oop_ axis_
#def set_position_xy(self, value, mousex,mousey)

#is_bool attr.




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
        self.is_mouselock = False

        self.gl_settings()
        
        def on_key_press(symbol,modifiers):
            #print(pyglet.window.key.symbol_string(symbol))
            pass
        self.on_key_press = on_key_press

    def gl_settings(self):
        #===============================gl settings
        glEnable(GL_DEPTH_TEST) #--skip depth less kinds.. default fine.
        #glClearColor(0.0, 0.24, 0.5, 1.0) #moved from draw loop.. #..why it here??
        glPointSize(5) #good for debug



    def close(self,value=False):#alt f4 error fixed.            
        super().close()
        return True

    def lock_mouse(self,value=False):
        if not value:return True#works great. True for escape        
        self.is_mouselock = not self.is_mouselock
        self.set_exclusive_mouse(self.is_mouselock)#lock mouse x,y 0, hold. use dxdy then!         
        return True #escape

    def bind_inputlayer(self,inputlayer):
        #=====================================KEY EVENT
        #self.inputlayer = inputlayer
        #inputlayer = self.inputlayer
        window = self
        @window.event
        def on_key_press(symbol,modifiers):
            key = InputLayer.symbol_to_key(symbol,modifiers)            
            inputlayer.cast(key,1)
        @window.event      
        def on_key_release(symbol, modifiers):
            key = InputLayer.symbol_to_key(symbol,modifiers)
            inputlayer.cast(key,0)
        #=====================================MOUSE EVENT
        @window.event
        def on_mouse_press(x, y, button, modifiers):
            key = InputLayer.symbol_to_key(button,modifiers)
            if not window.is_mouselock:inputlayer.cast_axis(x,y)
            inputlayer.cast(key,1)
        @window.event
        def on_mouse_release(x, y, button, modifiers):
            key = InputLayer.symbol_to_key(button,modifiers)
            if not window.is_mouselock:inputlayer.cast_axis(x,y)
            inputlayer.cast(key,0)
        @window.event
        def on_mouse_scroll(x, y, scroll_x, scroll_y):
            if scroll_y>0:#up
                key = "M_SCROLL_UP"
            elif scroll_y<0:
                key = "M_SCROLL_DOWN"
            if not window.is_mouselock:inputlayer.cast_axis(x,y)
            inputlayer.cast(key,1)

        @window.event
        def on_mouse_motion(x, y, dx, dy):
            """motion and broadcasted once a frame"""
            if not window.is_mouselock:
                inputlayer.cast_axis(x,y, key = "M_XY_MOTION")
            else:
                inputlayer.cast_axis(dx,dy, key = "M_DXDY_MOTION")
        @window.event
        def on_mouse_drag(x, y, dx, dy, buttons, modifiers):#ah, maybe when clicked, motion not occur but this.
            #drag is pressed move. assume it move, for simple way!
            if not window.is_mouselock:
                inputlayer.cast_axis(x,y, key = "M_XY_MOTION")
            else:
                inputlayer.cast_axis(dx,dy, key = "M_DXDY_MOTION")
        
    



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




window = Window()




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
    GL_dict = {}
    last = -1
    @classmethod
    def get(cls,ID):
        return cls.GL_dict.get(ID)

    def __init__(self, vertstr, fragstr):
        assert bool(glCreateShader)#sometimes compile error occurs, before window() 
        vshader = shaders.compileShader( vertn, GL_VERTEX_SHADER)
        fshader = shaders.compileShader( fragn, GL_FRAGMENT_SHADER)
        program = shaders.compileProgram( vshader,fshader)
        glDeleteShader(vshader)
        glDeleteShader(fshader)
        self.ID= program
        Shader.GL_dict[self.ID] = self

        self.loc={}
        # #----Locations. no need to bind the program.
        # ProjectionLoc = glGetUniformLocation(program, "Projection")
        # ViewLoc = glGetUniformLocation(program, "View")
        # ModelLoc = glGetUniformLocation(program, "Model")
        # #self.ViewProjectionLoc = glGetUniformLocation(program, "ViewProjection")#ithink 4x4*4x4 not slow.
        # #-1 if not exist. or 0..1..2..kinds.
        # assert -1 not in (ProjectionLoc,ViewLoc,ModelLoc)
        # self.loc={
        # "Projection" : ProjectionLoc,
        # "View" : ViewLoc,
        # "Model" : ModelLoc,
        # }



    def bind(self):
        if Shader.last != self.ID:
            glUseProgram(self.ID)
            Shader.last = self.ID
    def unbind(self):
        glUseProgram(0)
        Shader.last = -1#not forget it!

    def get_loc(self, uniform_name):
        loc = self.loc.get(uniform_name)
        if not loc:
            program = self.ID
            loc = glGetUniformLocation(program, uniform_name)
            self.loc[uniform_name] = loc
        return loc

    def set_int(self, uniform_name, value):
        loc = self.get_loc(uniform_name)
        glUniform1i(loc,value)
    def set_float(self, uniform_name, value):
        loc = self.get_loc(uniform_name)
        glUniform1f(loc,value)
    def set_vec3(self, uniform_name, vec3):
        loc = self.get_loc(uniform_name)
        # if (len(args) == 1 and type(args[0]) == glm.vec3):
        #     glUniform3fv(glGetUniformLocation(self.ID, name), 1, glm.value_ptr(args[0]))
        # elif (len(args) == 3 and all(map(lambda x: type(x) == float, args))):
        #     glUniform3f(glGetUniformLocation(self.ID, name), *args)        
    def set_mat4(self, uniform_name, mat):
        """we need bind the shader first!"""
        loc = self.get_loc(uniform_name)
        glUniformMatrix4fv(loc,1,False, mat)# True for row major.ha.[1,2,3,4, ,]
        #location count transpose data
        #glUniformMatrix4fv(loc, 1, GL_FALSE, glm.value_ptr(mat))

    
    # def set_mat4(self,modelmat):
    #     """we need bind the shader first!"""
    #     ModelLoc = self.loc["ModelLoc"]
    #     glUniformMatrix4fv(ModelLoc,1,False, modelmat)# True for row major.ha.[1,2,3,4, ,]
    #     #location count transpose data
    # def set_Projection(self,projectionmat):
    #     ProjectionLoc = self.loc["ProjectionLoc"]
    #     glUniformMatrix4fv(ProjectionLoc,1,False, projectionmat)
    # def set_View(self,viewmat):
    #     ViewLoc = self.loc["ViewLoc"]
    #     glUniformMatrix4fv(ViewLoc,1,False, viewmat)

    #def set_Camera(self,camera): #we think, if (view,projedtion) or viewXprojection , but we don't so.
        #if len(camera) == 1:#VP            ViewProjectionLoc        



shader = Shader(vertn,fragn)
#print(s.ViewLoc)
#s.bind()
#s.set_Model(modelmat)
#s.unbind()
#=============================== SHADER





#=============================== MESH DATA
# --data area
# meshdata = xyz,uv,,kinds.
# VAO = VAO,VBO created, attr connects data.


class VAO:
    """indexed actually. hope we not use vao_notindexed."""
    last = -1
    GL_dict = {}
    @classmethod
    def get(cls,ID):
        return cls.GL_dict.get(ID)

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
            
        self.ID = VAO
        self.__class__.GL_dict[self.ID] = self
        self.ID_VBO = VBO
        self.ID_EBO = EBO
        #self.mode = GL_TRIANGLES some model drawn lines kind thing requires not use it.
        self.stride = stride
        self.points = len(indices)
    def update(self,vertices):
        """requires same shape kinds.."""
        #assert self.points == len(vertices)//self.stride
        VAO = self.ID
        VBO = self.ID_VBO
        glBindVertexArray(VAO)
        glBindBuffer(GL_ARRAY_BUFFER, VBO) #gpu bind VBO in VAO
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        #GL_STREAM_DRAW for little change, if you want someday..
        self.points = len(vertices)//self.stride

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

    def draw(self, MODE = GL_TRIANGLES):
        """requires bind first. it just draw command of VAO bound gpu."""
        #simple mode changeable draw. we not prefer partial draw which is slow.
        #glBindVertexArray(self.VAO)
        glDrawElements(MODE, self.points, GL_UNSIGNED_INT, None)


vaoidx = VAO( {0:3,1:2},
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
    last=-1
    last_unit = 0
    GL_dict = {}
    @classmethod
    def get(cls,name):
        for ID, texture in cls.GL_dict.items():
            if texture.name == name:
                return texture
        return None
        #return cls.GL_dict.get(ID)

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

    def __init__(self,width,height, MIPMAP = False, FORMAT = GL_RGB, name=''):
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
        Texture.GL_dict[self.ID] = self
        self.width = width
        self.height = height
        self.name = name

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
        #https://www.khronos.org/registry/OpenGL-Refpages/gl4/html/glActiveTexture.xhtml
        if Texture.last_unit != unit:
            glActiveTexture(self.unitdict[unit])
            Texture.last_unit = unit
        if Texture.last != self.ID:
            glBindTexture(GL_TEXTURE_2D, self.ID)
            Texture.last = self.ID
    def unbind(self):
        glBindTexture(GL_TEXTURE_2D, 0)
        Texture.last = -1

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

#=============================== MESH










#=============================== MESH


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
from pymatrix_mini import vec3,eye4,translate, normalize, mperspective,mortho,mlookat


class Camera:
    ID = 0
    def __init__(self):
        self.ID = Camera.ID
        Camera.ID+=1

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

        self.target = None
        self.actor = None

        self.keymap = {
        'M_DXDY': 'mouse_moveDXDY(1)',
        'M_SCROLL_UP': 'set_fov(-5)',
        'M_SCROLL_DOWN': 'set_fov(5)',
        }

    def get_Projection(self):#was set_..
        fov = self.fov
        window_ratio = self.window_ratio
        near = self.near
        far = self.far            
        mprojection = mperspective(fov, window_ratio, near,far)
        return mprojection

    def get_View(self):
        if self.actor:#think here is fine.
            self.pos = self.actor.pos
        eye = self.pos
        if self.target:
            target = self.target.pos
        else:
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




#class AXISActor: #not here


#obj1 = load_obj(fname)

#obj has mesh-texture combination. thats called model.(combined mesh)

# mesh has vao-texture.
# obj has meshs. its middle form.
# model has texture, meshs. a complete 3dmodel. ready to draw. get_flag.
# actor has model, collmodel. fine. and animation maybe.
# world has actor, light, camera. and draws all.

#we need to keep vao texture data,, ..not! we load each time.

#mesh.textureID
# if texture.name == : dict[ID]=texture

#by dir name. fullname specifys a file.
#byte data lentgh kinds. hash.. but too mess. but maybe the only way :data.
#see vao.. we can make texture all by data, not by file.!

#yeah. we have gl id actually! from file obj can be ..done. same source,same data.


#this is the grand all file loaded data storage

#actor.texture
#actor.mesh1.texture

255 == int('0xff',base=16)
255 == int('ff',base=16)

0xFFF000 == 0xFFF<<12#(4*3)

#hex(1044480) =='0xff000'
#hex(1044480)[2:].zfill(6)

class Mesh:
    def __init__(self):
        self.shaderID = 0
        self.textureID = 0
        self.VAOID = 0
    def get_flag(self):
        sha = self.shaderID
        tex = self.textureID
        vao = self.VAOID
        #4*3=12, 4*6=24
        return sha<<24 +tex<<12 +vao
        #if sha*tex*vao==0:
        #    return "000000000"
        #sha_hex = hex(sha)[2:].zfill(3)
        #tex_hex = hex(tex)[2:].zfill(3)
        #vao_hex = hex(vao)[2:].zfill(3)
        #return sha_hex+tex_hex+vao_hex



class Level:
    def __init__(self):
        self.actor_dict = {}
        self.light_dict = {}
        self.camera_dict = {}
    def save(self,txtname):
        23
    def load(self,txtname):
        23

    def get_actor(self, name=None):
        if name in self.actor_dict:
            return self.actor_dict[name]
        return None





class PollingSocket:
    def __init__(self):
        self.targetIP = None
        self.connect()
        self.data = None
    def connect(self):
        socket.bind()
    def get(self):
        data = socket.get()
        if data:
            self.data = data
    def run(self):
        thread_timer(self.get,0.01)
    def bind_inputlayer(self, inputlayer):
        pass

#posePoll = PollingSocket()
#posePoll.bind_inputlayer(inputlayer)
#posePoll.run()









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

        'J_Y': 'move_forward(0.1)',
        'J_X': 'move_right(-0.1)',
        'J_DPAD_XY': 'halt',

        'J_R1': 'set_fov(-5)',
        'J_L1': 'set_fov(5)',
        #'J_RY': 'move_forward(0.1)',
        #'J_Z': 'move_forward(0.1)',
        #'J_X': 'move_right(-0.1)',
         }

#1. (ratio), delivers value.  if not value:return  if you want pressed only
#func
#func(2.5)
#funcDXDY(1)
#_XY _DXDY _XYZ






class InputLayer:
    @classmethod
    def symbol_to_key(cls, symbol, modifiers):
        """ translate keyboard,mouse input, to use directly keymap={'W':do_func}.


        :param symbol: keyboard,mouse button (not for the state of drag 1+4=5.)
        :param modifiers: CTRL(1st), LSHIFT only.
        :returns: key. W W+CTRL M_LEFT...
        """
        
        #======================symbol
        key = pyglet.window.key.symbol_string(symbol)
        #'1' if mouse button 1.  key.symbol_string(49) > "_1"
        #if buttons & pyglet.window.mouse.LEFT:
        #pass
        #pyglet.window.mouse.buttons_string(1)
        #'LEFT'
        # pyglet.window.mouse.LEFT
        
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
        #NOTE: MOD_SCROLLLOCK -> CTRL
        #print( pyglet.window.key.modifiers_string(modifiers) )    
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
    


    """has window check. sends packed events to  Controller (2d,3d) """
    def __init__(self):
        self.events = [] #eventList ..fast but not PEP8.  (list)-s (dict)_dict fine.        
            
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
        #AXIS KINDS: X XY XYZ DXDY
        # M_XY
        # M_XY_MOTION
        # M_DXDY
        # M_DXDY_MOTION
        # J_DPAD_XY
        # J_DPAD_XY_MOTION        
        if z is None:# better than == None
            event = (key, (x,y) )
        else:
            event = (key, (x,y,z) )
        self.events.append(event)

    def update(self):
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
        return deliver_pack        

inputlayer = InputLayer()
window.bind_inputlayer(inputlayer)


class Controller:
    def __init__(self, target=None):
        self.layers = []#for high layer. window, UIworld, world
        self.targets = []
        if target:self.targets.append(target)
        #self.target = target #for Actor.
    
    def add_layer(self, layer):
        self.layers.append(layer)

    def add_target(self, target):
        self.targets.append(target)
    def set_target(self, target_s):
        if isinstance(target_s, list):
            self.targets = target_s
        else:
            self.targets = [target_s]

    def broadcast(self, events):
        targets = []
        targets.extend(self.layers)
        targets.extend(self.targets)
        for event in events:
            for target in targets:
                consume = self.deliver(target,event)
                if consume:break
                #we not transfer to child. parent only get event. gun 'K':fire nonsense. human fires.

                # maxrecursion = 5
                # while maxrecursion:#prevent stuck in loop. max_depth
                #     #print(maxrecursion,target) if maxrecursion<5 else 1
                #     child_ID = getattr(target, "child_ID", None)
                #     if child_ID:
                #         maxrecursion-=1
                #         target = world.get_actor(child_ID)
                #         consume = self.deliver(target,event)
                #         if consume:break#for childs.
                #     else:
                #         break



    @classmethod
    def deliver(cls,target,event):
        """ key,value = event, value 1.0, (1,2),(1,2,3) return True if consume"""
        key,value = event
        if not hasattr(target, "keymap"):
            return
        funcname = target.keymap.get(key,None)
        if funcname is None:
            return
        
        skip_deliver = False

        if funcname[-1] == ")":
            ridx = funcname.find("(")
            if not ridx == -1:
                mixer = funcname[ridx:]
                mixer = float(mixer[1:-1])
                funcname = funcname[:ridx]
        else:# no (1.0), we not deliver value.
            skip_deliver = True

        func = getattr(target, funcname, False)
        if func:
            if skip_deliver:#value is None:# 0==False +we skip when value==0, key released.
                if value==0:#do only pressed
                    return
                else:
                    return func()
            else:
                if not isinstance(value,tuple):
                    value *= mixer
                    return func(value)
                else:
                    lenval = len(value)
                    if lenval==2:
                        x,y = value
                        x*=mixer
                        y*=mixer
                        return func(x,y)
                    elif lenval==3:
                        x,y,z = value
                        x*=mixer
                        y*=mixer
                        z*=mixer
                        return func(x,y,z)


class PlayerController(Controller):
    """ Controller that has player(human) methods."""
    def __init__(self):
        super().__init__()



playercontroller = PlayerController()



#__getattribute__ is for internal . 1st override, while getattr occurs if not exist.
#use getattr for __var


class Joystick:
    @classmethod
    def available(cls):
        joysticks = pyglet.input.get_joysticks()
        return len(joysticks)>0

    def __init__(self):
        joysticks = pyglet.input.get_joysticks()
        if joysticks:
            joystick = joysticks[0]
            joystick.open()

            self.joystick = joystick            

    def bind_inputlayer(self,inputlayer):
        joystick_mapping = {
            0:'J_BUTTONA',
            1:'J_BUTTONB',
            2:'J_BUTTONX',
            3:'J_BUTTONY',
            4:'J_L1',
            5:'J_R1',
            6:'J_SELECT',
            7:'J_START',
            8:'J_L2',
            9:'J_R2',

            'x':'J_X_MOTION',
            'y':'J_Y_MOTION',
            'z':'J_Z_MOTION',
            'rx':'J_RX_MOTION',
            'ry':'J_RY_MOTION',
            }

        joystick = self.joystick

        @joystick.event
        def on_joybutton_press(joystick, button):
            #print(joystick,button)#A B X Y L R selstart LhatRhat 012345 67 89
            key = joystick_mapping.get(button, "unknown")
            inputlayer.cast(key, 1)
            pass

        @joystick.event
        def on_joybutton_release(joystick, button):
            key = joystick_mapping.get(button, "unknown")
            inputlayer.cast(key, 0)
            pass

        @joystick.event
        def on_joyaxis_motion(joystick, axis, value):
            #print(axis,value) #x,y or rx,ry up -1. Z L1 R-1 0.
            key = joystick_mapping.get(axis, "unknown")
            inputlayer.cast(key, value)
            pass
        @joystick.event
        def on_joyhat_motion(joystick, hat_x, hat_y):
            #print(hat_x,hat_y,'hat')#cross key R UP 1,1
            inputlayer.cast_axis(hat_x, hat_y, key='J_DPAD_XY')            
            pass
    #https://pyglet.readthedocs.io/en/latest/modules/input.html#pyglet.input.Joystick.on_joybutton_press



if Joystick.available():
    joystick = Joystick()
    joystick.bind_inputlayer(inputlayer)













class Resource:#deprecated for gl objects. each class contains dict[ID:object]!
    def __init__(self):
        #self.shader = {}
        #self.texture = {}
        #self.VAO = {}

        #what about ID?
        self.sound = {}
        self.music = {}
        self.keymaps = []
    def add(self,object):
        #key = object.ID#thats for it
        key =  getattr(object, "ID", None)
        if not key:
            print('no ID')
            return
        if isinstance(object, Shader):
            self.shader[key] = object
        elif isinstance(object, Texture):
            self.texture[key] = object
        elif isinstance(object, VAO):
            self.VAO[key] = object
        print(key, 'add resource',object)


#resource = Resource()
#resource.add(texture)
#resource.add(vaoidx)
#resource.add(shader)


class Actor:
    ID = 0
    def __init__(self):
        self.ID = Actor.ID#or uuid kinds.
        Actor.ID+=1

        self.pos = vec3(0,0,0)
        #---gldraw
        self.shader_ID = 0 #shader_ID or even shader.ID?? think we dont need but only ID. +save
        self.texture_ID = 0
        self.VAO_ID = 0
        self.is_skipdraw = False

        self.keymap = {}#this is basic form. not None. .get err at Controller.deliver.

        self.parent_ID = None
        self.child_ID_list = [] #child can be multiple.

        #self.attr_classdict = {'pos':vec3, }
        self.attr_vec3 = ('pos',)
        self.attr_keys = [ "pos", "keymap", "shader_ID","texture_ID","VAO_ID","is_skipdraw",
        ]

    def savestr(self):
        # vec3 ->list. False false.  NOTE: None->null, tuple->list.
        outdict = {}
        for key in self.attr_keys:
            outdict[key] = getattr(self,key)
        return json.dumps(outdict)

    def loadstr(self, string):
        indict = json.loads(string)
        for key,value in indict.items():
            if key in self.attr_vec3:
                setattr(self,key, vec3(value) )
            else:
                setattr(self,key,value)

    def copy(self):
        actor = Actor()
        #-----i hope these can be sent all in once, by dict kinds..
        #we did.
        for key in self.attr_keys:
            value = getattr(self,key)
            if key in self.attr_vec3:
                setattr(actor,key, vec3(value) )
            else:
                setattr(actor,key,value)
        return actor

    def add_child(self,child):
        self.child_ID_list.append(child.ID)
    def set_child(self, child_s):
        """set_childs too bad name. we know it is list, from add_child method. """
        if isinstance(child_s, list):
            self.child_ID_list = [ child.ID for child in child_s]
        else:
            self.child_ID_list = [child_s.ID]

    def get_Model(self):
        x,y,z = self.pos
        return translate(eye4(),x,y,z)

    #def destroy(self):        wecannot refer world. let world delete it.

    #Actor_saveload (small means method.) see Actor_method_saveload is too long.
    #SaveActor
    #Unit(Actor, Actor_save, ) #Actor_save only for methods.
    #-00these kinds .. we expend  Actor_Movable kinds. not pawn.
    def move_forward(self, value):
        if not value:return
        self.pos += vec3(0,0,-value)
    def move_right(self, value):
        if not value:return
        self.pos += vec3(value,0,0)


actor = Actor()
actor.shader_ID = shader.ID
actor.texture_ID = texture.ID
actor.VAO_ID = vaoidx.ID

#maxn = GL_MAX_VERTEX_UNIFORM_COMPONENTS
#maxn = glGetIntegerv(GL_MAX_VERTEX_UNIFORM_COMPONENTS)
#https://forums.raspberrypi.com/viewtopic.php?t=120029
#maxn = glGetIntegerv(GL_MAX_VERTEX_UNIFORM_VECTORS)

#level = []
class World:
    def __init__(self):
        self.actor_dict = {}
        self.camera_dict = {}
        self.light_dict = {}

        #---sort kinds.
        self.gl_sortedID = []
        self.gl_sort_required = True

        #self.controlltarget = None#moved to Controller.

        self.keymap = {"C":"create_plate"}
    def create_plate(self):
        actor = Actor()
        x=0#x = random.random()
        y=0#y = random.random()
        y=1
        z = random.random()*2
        actor.pos = vec3(x,y,z)
        actor.shader_ID = shader.ID
        actor.texture_ID = texture.ID
        actor.VAO_ID = vaoidx.ID
        self.add_actor(actor)

    def add_actor(self,actor):
        self.actor_dict[actor.ID] = actor
    def add_camera(self,camera):
        self.camera_dict[camera.ID] = camera
    def get_actor(self, ID):
        actor = self.actor_dict.get(ID, None)
        if actor:
            return actor
    def get_actor_name(self, name):
        for ID , actor in self.actor_dict.items():        
            if actor.name == name:
                return actor

    def get_camera(self, idx=0):#note  idx or camera.ID.. what to use?
        cam = self.camera_dict.get(idx, None)
        if cam:
            return cam

    def remove_actor(self,actor_ID):#pop..nah..       #should we input ID directly? 
        #actor = self.actor_dict[actor.ID]
        actor = self.actor_dict.pop(actor_ID)#..pop!
        #its done here. it not drawed.. neither updated.. we only access bia world.
        #check controller target to None..

    
    def update(self, dt):
        print(dt)

    def set_camer(self, ID):#deprecated. fine.
        camera = self.cameraDict.get(ID)
        if camera !=None:
            projectionmat = camera.get_Projection()
            viewmat = camera.get_View()
            shader.set_Projection(projectionmat)
            shader.set_View(viewmat)

    def gl_sort_ID(self):
        shader_dict = {}
        texture_dict = {}
        vao_dict = {}
        for ID, actor in self.actor_dict.items():
            shader_dict[ID] = actor.shader_ID
            texture_dict[ID] = actor.texture_ID
            vao_dict[ID] = actor.VAO_ID

        length_list = []
        length_list.append( (len(set(shader_dict.values())) ,shader_dict) )
        length_list.append( (len(set(texture_dict.values())) ,texture_dict) )
        length_list.append( (len(set(vao_dict.values())) ,vao_dict) )

        sorted_list = sorted(length_list, key = lambda k: k[0] ) #by length.fine.
        #print(sorted_list)#[(1, {0: 3}), (1, {0: 1}), (1, {0: 2})]
        book={}
        book[0] = sorted_list[0][1]#{0: 3}
        book[1] = sorted_list[1][1]
        book[2] = sorted_list[2][1]

        sorted_key = sorted(self.actor_dict, key=lambda k: (book[0][k],book[1][k],book[2][k]) )
        self.gl_sortedID =sorted_key
        self.gl_sort_required = False
        #return sorted_key

    def draw(self):
        #proejction
        #view
        #shader.set_Projection(projectionmat)
        #shader.set_View(viewmat)

        camera = self.get_camera()
        
        if self.gl_sort_required:
            self.gl_sort_ID()
        print(self.gl_sortedID)
        #-----------draw
        for ID in self.gl_sortedID:
            actor = self.actor_dict[ID]
            if actor.is_skipdraw:
                continue#to next iter
            modelmat = actor.get_Model()

            projectionmat = camera.get_Projection()
            viewmat = camera.get_View()
            shader.bind()
            shader.set_Projection(projectionmat)
            shader.set_View(viewmat)
            break
            
            #--------------------------
            mesh = actor.mesh

            mesh.shader.bind()
            mesh.shader.set_Model(modelmat)
            mesh.texture_bind()#for multi texture.
            #mesh has texture_dict
            mesh.VAO.bind()
            mesh.VAO.draw()
            
            texdict = {
            0:'color',
            1:'color2',
            2:'color3',
            3:'specular',
            4:'normal',
            5:'bump',
            }

            #def init
                #location = glGetUniformLocation(self.shader.ID, f"tex{N}")#no need to bind..
                #texturename, location

            texture_dict={
            'diffuse':texture1,
            'color2':texture2,
            }
            #https://www.loc.gov/preservation/digital/formats/fdd/fdd000508.shtml
            #.mtl: Ka ambient Kd diffuse Ks specular-color Ns specular-highlight map_d alpha map_bump
            #0 coloron amb off, 1:ambon, 2 hi on            
            #Ns: defines the focus of specular highlights in the material.
            #Ns values normally range from 0 to 1000, with a high value
            #resulting in a tight, concentrated highlight.
            #..anyway i dont want use those!
            #we use: basic phong (use 0 only for color)
            #and advanced pbr (fixed and uniform option)
            #and full customized (files with mesh directory)

            #
            
            #phong: ambient diffuse specular
            #pbr: albedo, normal, specular, roughness +metallic.
            #with blender: color, metalic ,roughness, normal, alpha. (specular not that used. 0.5fixed)
            #+pbr, goodbye specular. ->reflection.
            def texture_bind(self):            
                for N, texture in self.texture_dict.items():
                #texname
                
                    glUniform1i(location, N)
                    glActiveTexture(GL_TEXTURE0)
                    glBindTexture(GL_TEXTURE_2D, texture.ID)
                    
                    Texture.set_target
                    texture.bind()



            meshmodel.bind()
            meshmodel.vao.draw()

            #for by texture.
            tex_ID_list = actor.meshmodel.texture_ID_list

            sha_ID = actor.meshmodel.shader_ID
            vao_ID = actor.meshmodel.VAO_ID            
            sha = Shader.get(sha_ID)
            vao = VAO.get(vao_ID)
            sha.bind()
            vao.bind()

            sha.set_Model(modelmat)

            #if len(tex_ID_list)==1:
                #tex_ID = tex_ID_list[0]#92% will be 1 texture.

            #pros: easy to see. cons: multiple objects with texture [1,2,3,4] , 
            for tex_ID in tex_ID_list:
                tex = resource.texture[tex_ID]
                tex.bind()
                vao.draw()#a single line.!

world = World()

newactor = actor.copy()
newactor.pos.x -= 1
world.add_actor(newactor)


actor.keymap = {
"W":"move_forward(1)",
"D":"move_right(1)",
"S":"move_forward(-1)",
"A":"move_right(-1)",
}
actor.pos.z+=2
world.add_actor(actor)

#cam.keymap = keymap
#cam.target
cam.actor = actor
world.add_camera(cam)

#playercontroller.add_target(cam)
#playercontroller.add_target(actor)
#playercontroller.set_target([])#to empty
playercontroller.add_layer(window)
playercontroller.add_layer(world)
playercontroller.set_target([cam,actor])


allnewactor = newactor.copy()#keymap also copied?
allnewactor.pos.y += 1
allnewactor.keymap = actor.keymap #copyied now. donno we need it or not.
world.add_actor(allnewactor)
playercontroller.add_target(allnewactor)


#actor.child_ID = newactor.ID
#actor.add_child#no effect yet.fine. maybe in update..




class UIworld(World):
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

def update(dt):
    if not dt==0:
        1
        #print(1/dt)
    
    eventpack = inputlayer.update()    
    #eventpack = aicontrollerCV.get()
    
    playercontroller.broadcast(eventpack)

    #uiworld.update(dt)
    world.update(dt)
    

#pyglet.clock.schedule(update)
pyglet.clock.schedule_interval(update, 0.0051) 

texture4 =  Texture.byimg('texture2.jpg')

from mesh import Mesh
#maha = Mesh([0,0,0, 1,0,0, 0,1,0, 1,0,0, 0,1,0,1,1,0] )
maha = Mesh(position =[0,0,0, 1,0,0, 0,1,0] , uv=[0,0, 1,0, 0,1])
#from vao import VAO
#VAO.get(maha.VAO).update_position([0,0,0, 1.5,0,0, 0,1,0])

@window.event
def on_draw():
    gldraw()

#@profile
def gldraw():
    #glClear(GL_COLOR_BUFFER_BIT)
    glClearColor(0.0, 0.24, 0.5, 1.0)
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)
    #world.draw()

    #print(cam)
    shader.bind()
    camera = cam
    projectionmat = camera.get_Projection()
    viewmat = camera.get_View()
    modelmat = eye4()
    shader.set_mat4('Projection',projectionmat)
    shader.set_mat4('View',viewmat)
    shader.set_mat4('Model',modelmat)

    #glBindVertexArray(vaocart.VAO)
    #glBindTexture(GL_TEXTURE_2D, texture)
    #glDrawElements(GL_TRIANGLES, vaocart.size, GL_UNSIGNED_INT, None)
    #glDrawArrays(GL_TRIANGLES, 0, vaocart.size) #mode first count

    texture4.bind()

    #vaoidx.bind()
    #vaoidx.draw()
    maha.draw()

    return

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
