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

uniform mat4 Model;
uniform mat4 View;
uniform mat4 Projection;

void main() 
{
    gl_Position = Projection * View * Model * vec4(pos,1);
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
#glUseProgram(program) not here, SO strange! --ha! if you change each draw, you need so.
#=============================== SHADER end




#-----------window setting must be first, later gl settings.
window = pyglet.window.Window()
window.set_size(800, 600)

#============gl settings
glEnable(GL_DEPTH_TEST) #--skip depth less
pyglet.gl.glPointSize(5)





#--------------------------mesh data
from fastestobjread import OBJ
#obj = OBJ('objs/mem/mem.obj')
#obj = OBJ('objs/cube2/cubemap.obj')
#obj = OBJ('objs/s4/s4top.obj')

obj =OBJ( 'resources/obj4ue4/obj_ue4_zupyfo_x1.obj')
#obj =OBJ( 'resources/s4/s4.obj')


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

#=============================== SET VBO
#https://pyglet.readthedocs.io/en/latest/programming_guide/graphics.html#guide-graphics    
vertex_list_indexed1 = vertex_list_indexed(vertex_count,
    faces,
    ('0g3f', vertex_coordinate ),
    ('1g2f', vertex_uv),#1t2f strange, but not working! and also 1 works while 0,2 not.
    )

#-----------time
def update(e=None):
    1
    car.update()
pyglet.clock.schedule_interval(update, 1/60.0)
from pyglet import clock


import numpy as np
from np_modelmat import vpos3,vpos,eye4,  mlookat,mortho,mperspective, mtrans
import np_modelmat

#-==--=--==--==--==-===-classs
class Actor:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0
        self.speedx = 0
        self.speedy = 0
        self.speedz = 0

    def move_foward(self,speed):
        self.speedx = speed
    def move_right(self,speed):
        self.speedy = speed
    def move_up(self,speed):
        self.speedz = speed

    def acc_foward(self,speed):
        self.speedx = speed
    def acc_right(self,speed):
        self.speedy = speed
    def acc_up(self,speed):
        self.speedz = speed
    
    def update(self):
        self.x+=self.speedx
        self.y+=self.speedy# for RH.
        self.z+=self.speedz

car = Actor()


from pyglet.window import key
@window.event
def on_key_press(symbol,modifiers):
    if symbol == key.W:
        car.move_foward(0.1)
    if symbol == key.S:
        car.move_foward(-0.1)
    if symbol == key.A:
        car.move_right(0.1)
    if symbol == key.D:
        car.move_right(-0.1)

@window.event      
def on_key_release(symbol, modifiers):
    #if symbol == key.RIGHT:
    if symbol == key.W:
        car.move_foward(0)
    if symbol == key.S:
        car.move_foward(0)
    if symbol == key.A:
        car.move_right(0)
    if symbol == key.D:
        car.move_right(0)


@window.event
def on_draw():
    #glClear(GL_COLOR_BUFFER_BIT)
    glClearColor(0.0, 0.24, 0.5, 1.0)
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)   
    glUseProgram(program)


    #----------model update
    #..maybe moved to def update.
    #car.update()    

    #--------MVP
    mmodel= eye4()
    mview= eye4()
    mprojection= eye4()

    #mmodel = np.array([[1,0,0,0], [0,0.57,0.82,0], [0,-0.82,0.57,0], [0,0,0,1]]) #row major 4x4. same above. but True works fine. as it's row major..ha!    
    id_modelmat = glGetUniformLocation(program, "Model")#True if row major. [ [1,2,3,4],,
    #mmodel = mmodel@mtrans(1.32,0,0)
    #mmodel = mmodel@mtrans(car.x, car.y, car.z)
    glUniformMatrix4fv(id_modelmat,1,True, mmodel)

    eye = vpos3(car.x,car.y,car.z)
    target = vpos3(0,0,0)

    #eye = vpos3(0,-3,0) #upv 0,0,1. supringly works! 0,0 bottom left. 2d coord system. not 0,0 topleft.
    #target = vpos3(0,0,0)
    upV = vpos3(0,0,1)
    mview = mlookat(eye,target,upV)
    id_viewmat = glGetUniformLocation(program, "View")
    glUniformMatrix4fv(id_viewmat,1,True, mview)

    mprojection = [[1.81,0,0,0], [0,2.4,0,0], [0,0,-1,-0.2], [0,0,-1,1]]
    id_promat = glGetUniformLocation(program, "Projection")
    glUniformMatrix4fv(id_promat,1,True, mprojection)

    vertex_list_indexed1.draw(GL_TRIANGLES)
    vertex_list_indexed1.draw(GL_LINE_STRIP)    
    vertex_list_indexed1.draw(GL_POINTS)
    
    #dt = clock.tick()
    #print(clock.get_fps())

pyglet.app.run()
