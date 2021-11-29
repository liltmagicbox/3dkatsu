from pyglet.gl import *
#https://pyglet.readthedocs.io/en/latest/programming_guide/graphics.html

from pyglet.graphics import vertex_list, vertex_list_indexed
#pyglet.graphics.vertex_list


from OpenGL.GL import *
from OpenGL.GL import shaders
#=============================== SHADER
vertn = """
#version 410

layout (location = 0) in vec3 pos;
layout (location = 1) in vec2 uv;

out vec2 uvcord;

uniform mat4 M;
uniform mat4 V;
uniform mat4 P;

void main() 
{
    gl_Position = V*M* vec4(pos,1);
    uvcord = uv;
}
"""

fragn = """
#version 410

in vec2 uvcord;

out vec4 outcolor;

uniform sampler2D tex1;


void main()
{
    //outcolor = vec4(uvcord,1,1 );
    outcolor = texture2D(tex1, uvcord);
}
"""
vshader = shaders.compileShader( vertn, GL_VERTEX_SHADER)
fshader = shaders.compileShader( fragn, GL_FRAGMENT_SHADER)
program = shaders.compileProgram( vshader,fshader)
#glUseProgram(program) not here, SO strange!
#=============================== SHADER end



window = pyglet.window.Window()
window.set_size(800, 600)

#-----old texture load and bind.. use obj instead.
#pic = pyglet.image.load('objs/cubemap/cubemap.png')
#texture = pic.get_texture()
#glEnable(GL_TEXTURE_2D)
#glBindTexture(texture.target, texture.id)


#============depth
glEnable(GL_DEPTH_TEST)
#glDepthFunc(GL_LESS)
#------------------




#--------------------------mesh data

from fastestobjread import OBJ
#obj = OBJ('objs/mem/mem.obj')
obj = OBJ('objs/cube2/cubemap.obj')
#obj = OBJ('objs/s4/s4top.obj')

#obj = OBJ('objs/boxcar/boxcar.obj')
#obj = OBJ('objs/base3d/base3d.obj')
#obj = OBJ('objs/cubemap/cubemapc.obj')
#obj = OBJ('objs/cubemap/cubemap.obj')
pic = pyglet.image.load(obj.texture)
texture = pic.get_texture()
#print(obj.multices)

faces = obj.idxs

vertex_count = len(obj.multices)
vertex_coordinate = []
vertex_uv = []

for multex in obj.multices:
    vert = multex[0]
    uv = multex[1]
    vertex_coordinate.extend(vert)
    vertex_uv.extend(uv)
nv = []

#------old scale code.
#for cord in vertex_coordinate:
    #nv.append(cord/25)
#vertex_coordinate = nv

#for i in range(45445):
    #print( vertex_coordinate[i],vertex_coordinate[i+1],vertex_coordinate[i+2] )
#--------------------------mesh data


#=============================== SET VBO
pyglet.gl.glPointSize(5)
#https://pyglet.readthedocs.io/en/latest/programming_guide/graphics.html#guide-graphics    
vertex_list_indexed1 = vertex_list_indexed(vertex_count,
    faces,
    #('v2f', vertex_coordinate ),
    ('0g3f', vertex_coordinate ),
    ('1g2f', vertex_uv),#1t2f strange, but not working! and also 1 works while 0,2 not.
    )

#-----------------temp model pos, move var.
pos = 0,0,0
move_foward = False




#=============================== camera
#qwe xyz++
#asd xyz--
class Camera:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 2

cam = Camera()

#cam.x+=1
#cam.y+=1

# xplus(x)
# xminus(x)
# ...
# massa('x','+')
# massa('x',1)
#massa(0)-6

#-py not works like below::
# camval = [cam.x,cam.y, cam.z]
# def massa(i):
#     #i%3 #loops 0,1,2        
#     if i//3 == 0:
#         camval[i%3]+=1
#     else:#456
#         camval[i%3]-=1
#     print(camval[i%3])

def massa(i):
    #camval = [cam.x,cam.y, cam.z] not this way
    #camdict = {0:cam.x,1:cam.y,2:cam.z} #not thisway, too!
    #i%3 #loops 0,1,2 
    # q w e
    # a s d   
    if i == 0:
        cam.x += 1
        print(cam.x)
    elif i == 1:
        cam.y += 1
    elif i == 2:
        cam.z += 1
    elif i == 3:
        cam.x -= 1
    elif i == 4:
        cam.y -= 1
    elif i == 5:
        cam.z -= 1



class Rotman:
    def __init__(self):
        self.i = 0
        self.j = 0
        self.mat = [[1,0,0], [0,1,0], [0,0,1]]        
    def plus(self):
        self.mat[self.i][self.j] +=1
        print(self.mat[self.i][self.j])
    def minus(self):
        self.mat[self.i][self.j] -=1
        print(self.mat[self.i][self.j])
    def target(self,i,j):
        self.i = i
        self.j = j
        print(i,j)


rotman = Rotman()

#=============================== keyboard
from pyglet.window import key

@window.event
def on_key_press(symbol,modifiers):
    global move_foward
    if symbol == key.RIGHT:
        move_foward = True

    elif symbol == key.Q:
        massa(0)
    elif symbol == key.W:
        massa(1)
    elif symbol == key.E:
        massa(2)
    elif symbol == key.A:
        massa(3)
    elif symbol == key.S:
        massa(4)
    elif symbol == key.D:
        massa(5)

    elif symbol == key.NUM_1:
        rotman.target(2,0)
    elif symbol == key.NUM_2:
        rotman.target(2,1)
    elif symbol == key.NUM_3:
        rotman.target(2,2)
    elif symbol == key.NUM_4:
        rotman.target(1,0)
    elif symbol == key.NUM_5:
        rotman.target(1,1)
    elif symbol == key.NUM_6:
        rotman.target(1,2)
    elif symbol == key.NUM_7:
        rotman.target(0,0)
    elif symbol == key.NUM_8:
        rotman.target(0,1)
    elif symbol == key.NUM_9:
        rotman.target(0,2)

    elif symbol == key.NUM_ADD:
        rotman.plus()
    elif symbol == key.NUM_SUBTRACT:
        rotman.minus()
    

@window.event      
def on_key_release(symbol, modifiers):
    global move_foward
    if symbol == key.RIGHT:
        move_foward = False




#=============================== fps kinds. ignore it, if you do not use it...
#https://pyglet.readthedocs.io/en/latest/modules/clock.html
from pyglet import clock

#-----------------------so called benchmark, but 60fps max
#missile moves so fast
def benchmark(dt):
    ha = pyglet.clock.get_fps()
    if ha>90:
        print('ham')

    global pos
    if move_foward:
        #pos= list(map(lambda x:x+1, pos))
        speedx = 0.1
        pos= pos[0]+speedx,pos[1],pos[2]

pyglet.clock.schedule(benchmark)

#missile descrete move..why? ..cause 0.1!
#if move mouse, 1000fps.
def update(dt):
    ha = pyglet.clock.get_fps()
    #print(ha)
    if ha>120:
        print('ham')    
#pyglet.clock.schedule_interval(update, 0.01)

#--------------------------





#-----------------aa not works yet..
#glEnable(GL_MULTISAMPLE)
#glEnable(GL_LINE_SMOOTH)
#glEnable(GL_POLYGON_SMOOTH)
import numpy as np
from np_modelmat import vpos3, mview,mortho,mviewport, vpos, eye4, mview_rotation, mview_translate,mview_col

@window.event
def on_draw():
    #glClear(GL_COLOR_BUFFER_BIT)
    glClearColor(0.0, 0.24, 0.5, 0)
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)   
    glUseProgram(program)

    #size = glGetUniformLocation(program, "pos")
    #glUniform3f(size, pos[0],pos[1],pos[2])

    

    #---------------------------model matrix
    scalef = 0.8
    id_modelmat = glGetUniformLocation(program, "M")
    #glUniformMatrix4fv(id_modelmat,1,False, [scalef,0,0,0, 0,scalef,0,0, 0,0,scalef,0, 0,0,0,1])
    glUniformMatrix4fv(id_modelmat,1,False, [[scalef,0,0,0],[0,scalef,0,0], [0,0,scalef,0], [0,0,0,1]])


    #---------------------------view matrix
    id_viewmat = glGetUniformLocation(program, "V")
    #eye = vpos3(5,0,5)
    eye = vpos3(cam.x,cam.y,cam.z)
    target = vpos3(0,0,0)
    upV = vpos3(0,1,0)
    vv = mview(eye,target,upV)
    #po = vpos(1,0,0)
    #print(vv.dot(po))
    #viewmat = vv

    viewmat = eye4()#passs as input. how wonderful..
    
    
    #-----------camrot
    viewmat[0][0] = rotman.mat[0][0]
    viewmat[0][1] = rotman.mat[0][1]
    viewmat[0][2] = rotman.mat[0][2]

    viewmat[1][0] = rotman.mat[1][0]
    viewmat[1][1] = rotman.mat[1][1]
    viewmat[1][2] = rotman.mat[1][2]

    viewmat[2][0] = rotman.mat[2][0]
    viewmat[2][1] = rotman.mat[2][1]
    viewmat[2][2] = rotman.mat[2][2]

    viewmat[0][3] = 0
    viewmat[1][3] = 1
    viewmat[2][3] = 1
    #print(rotman.mat)

    #viewmat[3] = [-cam.x, -cam.y, -cam.z, 1]#for keyboard qwe asd

    #viewmat[0][3] = 0.1

    #-------------cam pos matrix[3][-px -py -pz 1].
    #viewmat[3][0] = -1 #camera x position
    #viewmat[3][1] = -1 #y
    #viewmat[3][2] = -1 #z
    
    #viewmat[3] = [-cam.x, -cam.y, -cam.z, 1]
    
    eye = vpos3(2,0,0)
    #eye = vpos3(cam.x,cam.y,cam.z)
    target = vpos3(0,0,0)
    upV = vpos3(0,1,0)
    
    #rotv = mview_rotation(eye,target,upV)
    rotv = mview_col(eye,target,upV)
    transv = mview_translate(eye,target,upV)
    
    #viewmat = transv
    #viewmat = transv@rotv
    viewmat = rotv@transv
    #print(viewmat)
    print(rotv)
    #print(rotv,'r')
    #print(transv,'T')
    #print(viewmat,'V')
    #print(cam.x)


    #viewmat[3][2]=-1

    #print(rotv,'r')
    #print(transv,'tt')
    #print(viewmat,'view')

    #print(viewmat)
    
    #viewmat = eye4()
    #viewmat[3][0] = cam.x
    #viewmat[3][1] = cam.y
    #viewmat[3][2] = cam.z
    #viewmat[3][2] = -1

    #print(cam.x,cam.y,cam.z)
    #print(viewmat)

    viewmat = np.array([ #for front
        [ 1,  0,  0,  0,],
        [ 0,  1,  0,  0,],
        [0,  0, 1,  0,],
        [0,  0,  -1.1,  1,]
        ])
    viewmat = np.array([ # for right. campos=2,0,0
        [ 0,  0,  1,  0,],
        [ 0,  1,  0,  0,],
        [-1,  0, 0,  0,],
        [0,  0,  -1.1,  1,]
        ])
    #viewmat = viewmat.flatten()
    #print(viewmat)
    glUniformMatrix4fv(id_viewmat,1,False, viewmat)

    
    
    #---------------------------projection matrix
    ww,wh = window.get_size()
    view_width = 3
    wratio = ww/wh
    
    promat = mortho(-view_width*wratio,view_width*wratio, -view_width,view_width, 0.1,100)
    id_promat = glGetUniformLocation(program, "P")
    glUniformMatrix4fv(id_promat,1,False, promat)


    #you want -1 to 1 NDC to 800 600 pixel space??
    #viewportmat = mviewport(100,100,200,200)
    #id_viewportmat = glGetUniformLocation(program, "VIEWPORT")
    #glUniformMatrix4fv(id_viewportmat,1,False, viewportmat)

    

    vertex_list_indexed1.draw(GL_TRIANGLES)
    #vertex_list_indexed1.draw(GL_LINE_STRIP)    
    #vertex_list_indexed1.draw(GL_POINTS)

pyglet.app.run()
