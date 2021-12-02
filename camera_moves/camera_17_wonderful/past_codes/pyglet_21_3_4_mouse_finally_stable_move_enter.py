from time import time

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
window.set_exclusive_mouse(True) #lock mouse x,y 0, hold. use dxdy!

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
from np_modelmat import vpos3,vpos,eye4,  mlookat,mortho,mperspective, mtrans,mrotx
import np_modelmat

#-==--=--==--==--==-===-classs
class Actor:
    def __init__(self):
        self.pos = vpos3()
        self.speed = vpos3()
        self.speedX = 10 #once it was 100000, float uncertainty occured.ha.

        self.front = vpos3(1,0,0)
        #self.right = vpos3(0,-1,0) we calc when we want.
        self.up = vpos3(0,1,0)# yup..yeah..

    def move_front(self,speed):
        self.speed = self.front * speed * self.speedX
    def move_right(self,speed):
        right = np.cross(self.front, self.up)
        self.speed = right * speed * self.speedX
    def move_up(self,speed):
        self.speed = self.up * speed * self.speedX
    
    def update(self,dt):
        self.pos += dt*self.speed


class Car(Actor):
    def __init__(self):
        super(Car, self).__init__()

        self.roll = -90#deg not rad
        self.rollspeed = 0        
        
    def update(self,dt):
        super().update(dt)
        self.roll += dt*self.rollspeed

    def rotate(self,speed):
        self.rollspeed =speed * self.speedX *5

    def on_key_press(self,symbol):
        if symbol == key.UP:
            self.move_front(1)
        if symbol == key.DOWN:
            self.move_front(-1)
        if symbol == key.LEFT:
            self.move_right(-1)
        if symbol == key.RIGHT:
            self.move_right(1)

        if symbol == key.Q:
            self.rotate(-5)
        if symbol == key.E:
            self.rotate(5)
        if symbol == key.R:
            self.move_up(1)
        if symbol == key.F:
            self.move_up(-1)

    def on_key_release(self,symbol):
        if symbol == key.UP:
            self.move_front(0)
        if symbol == key.DOWN:
            self.move_front(0)
        if symbol == key.LEFT:
            self.move_right(0)
        if symbol == key.RIGHT:
            self.move_right(0)

        if symbol == key.Q:
            self.rotate(0)
        if symbol == key.E:
            self.rotate(0)
        if symbol == key.R:
            self.move_up(0)
        if symbol == key.F:
            self.move_up(0)


class Camera(Actor):
    def __init__(self):
        super(Camera, self).__init__()        
        
        #---below self.
        self.front = vpos3(0,0,-1)
        self.yaw = 0
        self.pitch = 0
    
    def update(self,dt):
        super().update(dt)
        #self.target = self.pos + self.front #was for camera only. yeah.

    def on_key_press(self,symbol):
        if symbol == key.W:
            self.move_front(1)
        if symbol == key.S:
            self.move_front(-1)
        if symbol == key.A:
            self.move_right(-1)
        if symbol == key.D:
            self.move_right(1)

    def on_key_release(self,symbol):
        if symbol == key.W:
            self.move_front(0)        
        if symbol == key.S:
            self.move_front(0)
        if symbol == key.A:
            self.move_right(0)
        if symbol == key.D:
            self.move_right(0)
        

    def mouse_move_by_front_cantsincedonno_howtorot_by_someaxis_quatanion(self, dx,dy):
        front = self.front

        sensitivity = 0.001
        dx *= sensitivity
        dy *= sensitivity        

        yaw = dx
        pitch = dy
        if (pitch > 89.0): #not pitch = max kinds.
            pitch = 89.0
        if (pitch < -89.0):
            pitch = -89.0
        
        #-----------phase2, change cam. we use 000 to xyz method.
        #degree = np.rad2deg(yaw) wow without this, feels non-linear. smaller,smallmove.
        degree = np.rad2deg(yaw)
        front_rotated = np_modelmat.rotate_y( front , degree)
        #lol i donno how to rotate by custom axis!
        #stuck here.fine.        
        self.front = front_rotated
        return 0

    def mouse_move(self, dx,dy):
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
        front = vpos3(0,0,0)
        front.x = np.cos(np.deg2rad(yaw)) * np.cos(np.deg2rad(pitch))
        front.y = np.sin(np.deg2rad(pitch))
        front.z = np.sin(np.deg2rad(yaw)) * np.cos(np.deg2rad(pitch))        
        
        #ssems normalized but do again..        
        self.front = front / np.linalg.norm(front)
        self.yaw = yaw
        self.pitch = pitch

    def keep_eye_on(self, target):
        front = target.pos - self.pos
        self.front = front / np.linalg.norm(front)




#=====================================OBJECTS

car = Car()
cam = Camera()
cam.pos = vpos3(-2,0,0)



#=====================================DEBUGGER
class Debugger:
    def __init__(self):
        self.dtlist = []
        self.oldt = 0
        self.debug = False
    def update(self, dt):
        newt = time()
        dt = newt - self.oldt
        self.oldt = newt
        self.dtlist.append(dt)

debugger = Debugger()
#debugger.debug = True




#=====================================UPDATE OCCURS
def update(dt):
    #fps = pyglet.clock.get_fps()
    #print(fps)    #or 1/dt-errors div/0
    
    #----input manager #assume it called before ondraw
    dx,dy = mousevalue.get_dxdy()
    cam.mouse_move(dx,dy)
    
    #---------------------dt deal
    #print(dt)
    car.update(dt)
    cam.update(dt)
    #cam.keep_eye_on(car)works great!
    
    debugger.update(dt)

pyglet.clock.schedule(update)#passes dt. for maxspeed. finally! with vsync.



#=====================================MOUSE EVENT
class Mousevalue:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.x_before = 0
        self.y_before = 0
    def get_dxdy(self):
        dx = self.x - self.x_before
        dy = self.y - self.y_before

        self.x_before = self.x
        self.y_before = self.y
        return dx,dy

mousevalue = Mousevalue()

@window.event
def on_mouse_motion(x, y, dx, dy):
    mousevalue.x += dx
    mousevalue.y += dy



#=====================================KEY EVENT
from pyglet.window import key
@window.event
def on_key_press(symbol,modifiers):
    car.on_key_press(symbol)
    cam.on_key_press(symbol)

@window.event      
def on_key_release(symbol, modifiers):
    car.on_key_release(symbol)
    cam.on_key_release(symbol)



#=====================================DRAW EVENT
@window.event
def on_draw():
    #glClear(GL_COLOR_BUFFER_BIT)
    glClearColor(0.0, 0.24, 0.5, 1.0)
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)   
    glUseProgram(program)


    #get projection
    #get view
    #getmodel:

    #-===== when you model too model,
    # get view projection, which stuck already,.
    # and each model, get modelmat, and model.draw() each. i think that's good.. 
    #or model.vertlist.draw(gltriangle). anyway model has own mode...el...? ah?
    #actualy model has it's name for VBO. a-ha. check whth a is b.
    # ma = vertex_list_indexed1
    # mb = vertex_list_indexed1
    # print( ma is mb, 'samevbo')
    # True samevbo
    #---------------so,
    # worldmat = 
    # for model in models:
    #     model.getmat
    #     set gpu 4x stuff..
    #     model.vbo.draw(GL_TRIANGLES)


    #--------MVP
    mmodel= eye4()
    mview= eye4()
    mprojection= eye4()

    #mmodel = np.array([[1,0,0,0], [0,0.57,0.82,0], [0,-0.82,0.57,0], [0,0,0,1]]) #row major 4x4. same above. but True works fine. as it's row major..ha!    
    id_modelmat = glGetUniformLocation(program, "Model")#True if row major. [ [1,2,3,4],,
    mmodel = mtrans(car.pos)@mrotx(car.roll)@mmodel #trans rotate scale pos
    glUniformMatrix4fv(id_modelmat,1,True, mmodel)

    
    #mview = np.array([[1,0,0,0], [0,1,0,0], [0,0,1,-3], [0,0,0,1]])# from top. youcan see head(z) of obj.    
    #---Zup , to screen is -y
    #eye = vpos3(0,-3,5) #upv 0,0,1. supringly works! 0,0 bottom left. 2d coord system. not 0,0 topleft.
    #eye = vpos3(cam.pos.x,cam.pos.y,cam.pos.z)
    
    eye = cam.pos
    
    target = cam.pos+cam.front
    # degree = 30
    # tmp = np_modelmat.rotate_z( cam.front , degree)
    # target = cam.pos + tmp
    # print(cam.front, tmp)

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



#------------------for fps test
from matplotlib import pyplot as plt
#x=range(10)
#y = [i*i for i in x]

if debugger.debug:
    dtlist = debugger.dtlist
    dtlist.pop(0)
    print(max(dtlist))
    print(min(dtlist))
    print(sum(dtlist)/len(dtlist))
    plt.plot(dtlist)
    plt.show()
