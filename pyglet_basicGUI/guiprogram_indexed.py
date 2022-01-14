from time import time

import pyglet
#from pyglet.gl import * #we don't use it!

from OpenGL.GL import *
from OpenGL.GL import shaders



#=============================== WINDOW
#window setting must be first, later gl settings.
window = pyglet.window.Window()
window.set_size(800, 600)
window.set_exclusive_mouse(True) #lock mouse x,y 0, hold. use dxdy then!

window.set_vsync(False) #for maximum fps

#============gl settings
glEnable(GL_DEPTH_TEST) #--skip depth less kinds.. default fine.
glClearColor(0.0, 0.24, 0.5, 1.0) #moved from draw loop..
glPointSize(5) #good for debug




#=============================== SHADER
vertn = """
#version 410

layout (location = 0) in vec3 pos;
layout (location = 1) in vec2 uv;

out vec2 uvcord;

//uniform int idx;
//uniform mat4 Model[252]; //253 max.. why not 255? 250 to remember easy
uniform mat4 Model;
uniform mat4 View;
uniform mat4 Projection;

void main() 
{
    //gl_Position = Projection * View * Model[gl_InstanceID] * vec4(pos,1);
    gl_Position = Projection * View * Model * vec4(pos,1);
    uvcord = uv;
}
"""

fragn = """
#version 410

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
#print( bool(glCreateShader) ) #sometimes compile error occurs, before window() 
vshader = shaders.compileShader( vertn, GL_VERTEX_SHADER)
fshader = shaders.compileShader( fragn, GL_FRAGMENT_SHADER)
default_shader = shaders.compileProgram( vshader,fshader)
# delete the shaders as they're linked into our program now and no longer necessary
glDeleteShader(vshader)
glDeleteShader(fshader)

#=============================== SHADER



#=============================== MESH DATA
# --data area
# meshdata = xyz,uv,,kinds.
# VAO = VAO,VBO created, attr connects data.

class VAO_indexed:
    def __init__(self, stride, attr_size_tuple,  vertices, indices):
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
        for i in range(int(len(attr_size_tuple)/2)):
            attr_index = attr_size_tuple[i*2]
            size = attr_size_tuple[i*2+1]

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
        self.size = len(indices)

    def update_vertices(self,vertices):
        """requires same shape kinds.."""
        VAO = self.VAO
        VBO = self.VBO
        glBindVertexArray(VAO)
        glBindBuffer(GL_ARRAY_BUFFER, VBO) #gpu bind VBO in VAO
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        #GL_STREAM_DRAW for little change, if you want someday..

    def update_vertices_indices(self,vertices, indices):
        VAO = self.VAO
        VBO = self.VBO
        EBO = self.EBO
        glBindVertexArray(VAO)
        glBindBuffer(GL_ARRAY_BUFFER, VBO) #gpu bind VBO in VAO
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)



import numpy as np

modelmat = [1,0,0,0, 0,1,0,0,  0,0,1,0,  0,0,0,1]

vaocart = VAO_indexed( 5,(0,3,1,2),
    #np.array([0,0,0, 0,0,  0.5,0,0, 1,0,  0.5,0.5,0, 1,1,  0,0.5,0, 0,1, ]).astype('float32'),
    np.array([0,0,0, 0,0,  1,0,0, 1,0,  1,1,0, 1,1,  0,1,0, 0,1, ]).astype('float32'),
    np.array([0,1,2,0,2,3,]).astype('uint')
    )


#=============================== MESH DATA




#=============================== TEXTURE
from PIL import Image
def texture_load(imgname):
    texture = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texture) # all upcoming GL_TEXTURE_2D operations now have effect on this texture object
    # set the texture wrapping parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)    # set texture wrapping to GL_REPEAT (default wrapping method)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
    # set texture filtering parameters
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

    # load image, create texture and generate mipmaps
    try:
        img = Image.open(imgname)

        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, img.width, img.height, 0, GL_RGB, GL_UNSIGNED_BYTE, img.tobytes())
        glGenerateMipmap(GL_TEXTURE_2D)

        img.close()

    except:
        print("Failed to load texture")

    return texture

texture = texture_load('texture2.jpg')

#=============================== TEXTURE



import math
from pymatrix_mini import vec3,eye4, normalize,  mperspective,mortho,mlookat

class Camera:
    def __init__(self):
        self.pos = vec3(0,0,0)

        self.front = vec3(0,0,-1)#toward screen
        self.up = vec3(0,1,0)
        
        #self.yaw = -90# means LH, ..fine.
        self.yaw = math.degrees(math.asin(self.front.z))
        self.pitch = 0

        self.isperspective = True
        self.fov = 50
        self.ortho_scale = 1
        #self.window_ratio = 800/600
        self.window_ratio = window.width/window.height
        self.near = 0.1
        self.far = 1000

    def mouse_move(self, dx,dy):
        #yaw LH rule, but works as we expect. use front, not yaw directly.
        yaw = self.yaw
        pitch = self.pitch

        sensitivity = 0.1
        dx *= sensitivity
        dy *= sensitivity        

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


    
    def get_matrix_projection(self):#was set_..
        if self.isperspective:
            fov = self.fov
            window_ratio = self.window_ratio
            near = self.near
            far = self.far            
            mprojection = mperspective(fov, window_ratio, near,far)
        else:
            ortho_scale = self.ortho_scale
            width = self.window_ratio *ortho_scale
            height = ortho_scale
            near = self.near
            far = self.far        
            mprojection = mortho(-width,width,-height,height,near,far)
            #(left, right, bottom, top, near, far)
        return mprojection

    def get_matrix_view(self):
        eye = self.pos
        target = self.pos+self.front
        upV = self.up
        mview = mlookat(eye,target,upV)
        return mview


cam = Camera()
cam.pos = vec3(0,0,2)
cam.isperspective=False


#=====================================MOUSE EVENT
@window.event
def on_mouse_motion(x, y, dx, dy):
    cam.mouse_move(dx,dy)
    #controller.on_mouse_motion(x, y, dx, dy)
@window.event
def on_mouse_press(x, y, button, modifiers):
    pass
    #controller.on_mouse_press(x, y, button, modifiers)
#=====================================KEY EVENT
from pyglet.window import key
@window.event
def on_key_press(symbol,modifiers):
    if symbol == key.W:
        cam.pos += vec3(0,1,0)
    if symbol == key.S:
        cam.pos += vec3(0,-1,0)
    if symbol == key.A:
        cam.pos += vec3(-1,0,0)
    if symbol == key.D:
        cam.pos += vec3(1,0,0)
@window.event      
def on_key_release(symbol, modifiers):
    pass
    
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
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)  

    program = default_shader
    glUseProgram(program)

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
    
    
    projectionmat = camera.get_matrix_projection()
    viewmat = camera.get_matrix_view()
    modelmat = eye4()
    
    projectionmatID = glGetUniformLocation(program, "Projection")
    viewmatID = glGetUniformLocation(program, "View")
    modelmatID = glGetUniformLocation(program, "Model")
    glUniformMatrix4fv(projectionmatID,1,False, projectionmat)
    glUniformMatrix4fv(viewmatID,1,False, viewmat)
    glUniformMatrix4fv(modelmatID,1,False, modelmat)# True for row major.ha.[1,2,3,4, ,]

    glBindVertexArray(vaocart.VAO)
    glBindTexture(GL_TEXTURE_2D, texture)
    glDrawElements(GL_TRIANGLES, vaocart.size, GL_UNSIGNED_INT, None)

pyglet.app.run()
