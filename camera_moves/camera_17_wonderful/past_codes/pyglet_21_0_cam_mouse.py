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




import numpy as np
from np_modelmat import vpos3,vpos,eye4,  mlookat,mortho,mperspective, mtrans,mrotroll
import np_modelmat

#-==--=--==--==--==-===-classs
class Actor:
    def __init__(self):
        self.pos = vpos3()
        self.speed = vpos3()

        self.roll = 0#deg not rad
        self.rollspeed = 0

        self.speedmultiplyer = 10000

        self.foward = vpos3(1,0,0)
        self.right = vpos3(0,-1,0)
        self.up = vpos3(0,0,1)
        self.target = self.pos + self.foward

    def move_foward(self,speed):
        self.speed[0] = speed * self.speedmultiplyer
    def move_right(self,speed):
        self.speed[1] = speed * self.speedmultiplyer
    def move_up(self,speed):
        self.speed[2] = speed * self.speedmultiplyer
    def rotate_roll(self,speed):
        self.rollspeed =speed * self.speedmultiplyer

    #def acc_foward(self,speed):
    
    def update(self,dt):        
        #self.pos[0]+=dt*self.speed[0]
        #self.pos[1]+=dt*self.speed[1]# for RH.
        #self.pos[2]+=dt*self.speed[2]
        self.pos+=dt*self.speed
        self.roll += dt*self.rollspeed

        #self vector
        self.target = self.pos + self.foward


car = Actor()

cam = Actor()

from pyglet.window import key
@window.event
def on_key_press(symbol,modifiers):
    if symbol == key.W:
        cam.move_foward(1)
    if symbol == key.S:
        cam.move_foward(-1)
    if symbol == key.A:
        cam.move_right(1)
    if symbol == key.D:
        cam.move_right(-1)
    if symbol == key.Q:
        cam.rotate_roll(-1)
    if symbol == key.E:
        cam.rotate_roll(1)

    if symbol == key.UP:
        car.move_foward(1)
    if symbol == key.DOWN:
        car.move_foward(-1)        
    if symbol == key.LEFT:
        car.move_right(1)
    if symbol == key.RIGHT:
        car.move_right(-1)

@window.event      
def on_key_release(symbol, modifiers):
    #if symbol == key.RIGHT:
    if symbol == key.W:
        cam.move_foward(0)        
    if symbol == key.S:
        cam.move_foward(0)
    if symbol == key.A:
        cam.move_right(0)
    if symbol == key.D:
        cam.move_right(0)
    if symbol == key.Q:
        cam.rotate_roll(0)
    if symbol == key.E:
        cam.rotate_roll(0)

    if symbol == key.UP:
        car.move_foward(0)
    if symbol == key.DOWN:
        car.move_foward(0)
    if symbol == key.LEFT:
        car.move_right(0)
    if symbol == key.RIGHT:
        car.move_right(0)



#-----------time
def update(e=None):
    global dtlist
    #print(pyglet.clock.get_fps())    
    
    #dt = pyglet.clock.tick()
    #print(dt)
    car.update(0.0001)
    cam.update(0.0001)
#pyglet.clock.schedule_interval(update, 1/60.0)
pyglet.clock.schedule(update)


@window.event
# def on_draw():
def on_draw():
    #glClear(GL_COLOR_BUFFER_BIT)
    glClearColor(0.0, 0.24, 0.5, 1.0)
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)   
    glUseProgram(program)

    #--------MVP
    mmodel= eye4()
    mview= eye4()
    mprojection= eye4()

    #mmodel = np.array([[1,0,0,0], [0,0.57,0.82,0], [0,-0.82,0.57,0], [0,0,0,1]]) #row major 4x4. same above. but True works fine. as it's row major..ha!    
    id_modelmat = glGetUniformLocation(program, "Model")#True if row major. [ [1,2,3,4],,
    mmodel = mtrans(car.pos)@mrotroll(car.roll)@mmodel #trans rotate scale pos
    glUniformMatrix4fv(id_modelmat,1,True, mmodel)

    
    #mview = np.array([[1,0,0,0], [0,1,0,0], [0,0,1,-3], [0,0,0,1]])# from top. youcan see head(z) of obj.    
    #---Zup , to screen is -y
    eye = vpos3(0,-3,5) #upv 0,0,1. supringly works! 0,0 bottom left. 2d coord system. not 0,0 topleft.
    #eye = vpos3(cam.pos.x,cam.pos.y,cam.pos.z)
    
    eye = cam.pos
    target = cam.target
    upV = cam.up    
    mview = mlookat(eye,target,upV)# lookat by cam by cam data.. for genelization..
    id_viewmat = glGetUniformLocation(program, "View")
    glUniformMatrix4fv(id_viewmat,1,True, mview)

    #---ortho vs perspective.
    #mprojection = [[1.81,0,0,0], [0,2.4,0,0], [0,0,-1,-0.2], [0,0,-1,1]]
    #mprojection = mortho(-5,5,-5,5,0.1,100)
    mprojection = mperspective(50, (800/600), 0.1,100)
    id_promat = glGetUniformLocation(program, "Projection")
    glUniformMatrix4fv(id_promat,1,True, mprojection)

    vertex_list_indexed1.draw(GL_TRIANGLES)
    vertex_list_indexed1.draw(GL_LINE_STRIP)    
    vertex_list_indexed1.draw(GL_POINTS)

pyglet.app.run()

