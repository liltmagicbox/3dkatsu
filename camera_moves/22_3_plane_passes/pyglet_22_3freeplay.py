from time import time

from pyglet.gl import *
#https://pyglet.readthedocs.io/en/latest/programming_guide/graphics.html

from pyglet.graphics import vertex_list, vertex_list_indexed, Batch
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

uniform sampler2D tex0;
uniform sampler2D tex1;


void main()
{
    //outcolor = vec4(uvcord,1,1 );
    //outcolor = texture2D(tex0, uvcord);
    outcolor = mix(texture(tex0, uvcord), texture(tex1, uvcord), 0.4);
}
"""
vshader = shaders.compileShader( vertn, GL_VERTEX_SHADER)
fshader = shaders.compileShader( fragn, GL_FRAGMENT_SHADER)
shader_default = shaders.compileProgram( vshader,fshader)
#print(dir(program))
#print(help( program.load))
#glUseProgram(program) not here, SO strange! --ha! if you change each draw, you need so.
#we will use like: instancedshader.use()
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
#obj =OBJ( 'resources/s4/s4.obj')

objname = 'resources/obj4ue4/obj_ue4_zupyfo_x1.obj'

def loadobj_return_vlist_texture(objname):
    obj =OBJ(objname)
    
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
    #<pyglet.graphics.vertexdomain.IndexedVertexList object at 0x000001CD7EB22370>
    return vertex_list_indexed1,texture


import numpy as np
from np_modelmat import vec3,vpos,eye4,  mlookat,mortho,mperspective, mtrans,mrotx
import np_modelmat



#-==--=--==--==--==-===-classs
#- we use world=Gameworld, which has up,front. for gravity or kinds.. no magic number.


class Gameworld:
    def __init__(self, shader=None ):
        self.front = vec3(1,0,0)
        self.up = vec3(0,1,0)

        #self.batch = Batch()
        self.actor_list = []        
        self.camera_list = []# it stores too, just so.. dont such: actor_list=[]
        #self.camera = None maybe will be betterway..
        #self.shader_id_list = [] gone pure var. like world itself.
    def front_copy(self):
        return self.front.copy()
    def up_copy(self):
        return self.up.copy()
    def actor_add(self,actor):
        self.actor_list.append(actor)

        #ithink it's best way found yet..
        if isinstance(actor, Camera):
            self.camera_list.append(actor)

    #ihope get cam by camera_list[i].  but unless you not use world.actor_list=[]...?
    def get_camera(self, i):
        camera = self.camera_list[i] #better for actor if actor.iscamera.
        
        #garbege collection.. idontlikeit.
        if not camera in self.actor_list:
            del self.camera_list[i]#hope it will just pop like delete..
            return None
        return camera

    #deprecated camadd.
    def xxxcamera_add(self,camera):
        self.camera_list.append(camera)
        #if not self.camera_list:#seems unsatisfing..
        #    self.camera = camera



world = Gameworld()


class Actor:
    """
    rule:
    don't have on_key kinds. unnessassary super.()things, feel free to add method way.
    """
    def __init__(self):
        self.pos = vec3()
        self.speed = vec3()
        self.speed_factor = 10 #once it was 100000, float uncertainty occured.ha.

        self.front = world.front_copy()
        #self.right = vec3(0,-1,0) we calc when we want.
        self.up = world.up_copy() # yup..yeah..

        self.isgravity = False
        self.gravity_factor = 9.8 #if worldglobal, there will no be floting mascote..

        self.mesh_list = [] # a mesh is just [vbo, [textures]]

    def move_front(self,speed):
        self.speed = self.front * speed * self.speed_factor
    def move_right(self,speed):
        right = np.cross(self.front, self.up)
        self.speed = right * speed * self.speed_factor
    def move_up(self,speed):
        self.speed = self.up * speed * self.speed_factor

    def move_front_world(self,speed):
        self.speed = world.front * speed * self.speed_factor
    def move_right_world(self,speed):
        right = np.cross(world.front, world.up)
        self.speed = right * speed * self.speed_factor
    def move_up_world(self,speed):
        self.speed = world.up * speed * self.speed_factor
    
    def update(self,dt):
        #note cam also actor!
        #if self.isfreeze return0 kinds.
        if self.isgravity:
            self.speed -= dt*self.up *self.gravity_factor

        self.pos += dt*self.speed

    def add_mesh(self, mesh):
        self.mesh_list.append(mesh)

    def get_matrix_model(self):
        mmodel = eye4()
        #mmodel = mtrans(self.pos)@mrotx(self.roll)@mmodel #trans rotate scale pos
        #keepit untill quaternion.
        mmodel = mtrans(self.pos)@mmodel
        return mmodel        




class Car(Actor):
    def __init__(self):
        super(Car, self).__init__()

        self.roll = -90#deg not rad
        self.rollspeed = 0
        self.isgravity = True
        
    def update(self,dt):
        super().update(dt)
        self.roll += dt*self.rollspeed

    def rotate(self,speed):
        self.rollspeed =speed * self.speed_factor *5

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
        self.front_default = vec3(0,0,-1)
        self.front = self.front_default
        self.yaw = 0
        self.pitch = 0

        self.target = None
        self.istrack = False
        
        self.isperspective = True
        self.fov = 50
        self.window_ratio = 800/600
        self.near = 0.1
        self.far = 100
    
    def update(self,dt):
        super().update(dt)
        #self.target = self.pos + self.front #was for camera only. yeah.
        if self.istrack:
            if self.target:
                front = self.target.pos - self.pos
                self.front = front / np.linalg.norm(front)

    def on_key_press(self,symbol):
        if symbol == key.W:
            self.move_front(1)
        if symbol == key.S:
            self.move_front(-1)
        if symbol == key.A:
            self.move_right(-1)
        if symbol == key.D:
            self.move_right(1)

        if symbol == key.T:
            self.istrack = True
            self.target = car

    def on_key_release(self,symbol):
        if symbol == key.W:
            self.move_front(0)        
        if symbol == key.S:
            self.move_front(0)
        if symbol == key.A:
            self.move_right(0)
        if symbol == key.D:
            self.move_right(0)
        if symbol == key.T:
            self.istrack = False
        

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
        front = vec3(0,0,0)
        front.x = np.cos(np.deg2rad(yaw)) * np.cos(np.deg2rad(pitch))
        front.y = np.sin(np.deg2rad(pitch))
        front.z = np.sin(np.deg2rad(yaw)) * np.cos(np.deg2rad(pitch))        
        
        #ssems normalized but do again..        
        self.front = front / np.linalg.norm(front)
        self.yaw = yaw
        self.pitch = pitch


    #seems better: target, on=True on=False..?
    # def keep_eye_on(self, target):
    #     front = target.pos - self.pos
    #     self.front = front / np.linalg.norm(front)
    # def keep_eye_on_release(self):
    #     self.front = self.pos + self.front_default

    def get_matrix_projection(self):#was set_..
        fov = self.fov
        window_ratio = self.window_ratio
        near = self.near
        far = self.far
        
        if self.isperspective:
            mprojection = mperspective(fov, window_ratio, near,far)
        else:
            mprojection = mortho(-5,5,-5,5,0.1,100)
        return mprojection

    def get_matrix_view(self):
        eye = self.pos
        target = self.pos+self.front
        upV = self.up
        mview = mlookat(eye,target,upV)
        return mview



class Projectile(Actor):
    def __init__(self):
        super().__init__()#maybe it's ok..
        
        #---below self.
        self.isgravity = False
        self.speed = vec3(5,0,0)

        #self.front = vec3(0,0,-1)
        #self.pos = vec3()
        #self.speed_factor = 10 #once it was 100000, float uncertainty occured.ha.

        #self.up = world.up_copy() # yup..yeah..

        #self.mesh_list = [] # a mesh is just [

    #def update(self,dt):
        #super().update(dt)

    # def on_key_press(self,symbol):
    #     if symbol == key.W:
    #         self.move_front(1)
    #     if symbol == key.S:

#=====================================OBJECTS

#=====================================WORLD SETTING
car = Car()
car.isgravity = False

vlist1 , texture1 = loadobj_return_vlist_texture(objname)


#----look how wonderful it used!
pic = pyglet.image.load('onpa.png')
texture2 = pic.get_texture()

carmesh = [vlist1, [texture1, texture2]] #no tuple can't change inner.
car.add_mesh(carmesh)

cam = Camera()
cam.pos = vec3(-2,0,0)
#cam.target = car
#cam.istrack = True

world.actor_add(car)
world.actor_add(cam)
#world.camera_add(cam) boldly, we do.



car2 = Car()
car2.pos = vec3(0,0,-2)
car2.isgravity = True
carmesh2 = [vlist1, [texture1,texture1]] #no tuple can't change inner.
car2.add_mesh(carmesh2)
world.actor_add(car2)


objname = 'resources/plane/plane.obj'
vlist1 , texture1 = loadobj_return_vlist_texture(objname)
projectile = Projectile()
#projectile.speed = vec3(10,5,0)
projectile.speed = vec3(-15,0,0)
projectile.pos = vec3(30,0,0)
rockmesh = [vlist1, [texture1,texture1]]
projectile.add_mesh(rockmesh)
world.actor_add(projectile)




from matplotlib import pyplot as plt
#x=range(10)
#y = [i*i for i in x]
#=====================================DEBUGGER
class Debugger:
    """ set value , p to set scoPe, [ ] to duration.
    """
    def __init__(self):
        self.debug = False        
        self.data_list = []
        
        #---time may no need..?
        self.time_list = []        
        self.starttime = 0        
        
        #self.target = "None" #is pure str, directly gets value.
        self.code = None

    def update(self):# acutally time stamp need. fine.
        if self.debug:
            value = eval( self.code ) #runs compiled code. eval catchs value..
            self.data_list.append(value)
            #---time may no need..?
            tpassed = time()-self.starttime
            self.time_list.append(tpassed)

    def on_key_press(self,symbol):
        if symbol == key.P:
            #requires input, like console input, and type, and enter.
            text = 'world.actor_list[2].pos.y'
            try:
                self.code = compile( text, '<string>', 'eval')
            except:
                self.code = 'return None'
            print('debug set: code compiled')
        if symbol == key.BRACKETLEFT:
            self.debug = True
            self.data_list = []
            self.starttime = time()
            print('debug start at:', time())#pyglet.colock.time wanted..
        if symbol == key.BRACKETRIGHT:
            self.debug = False
            print('debug end at:',time())
            self.show()

    def show(self):
        dtlist = self.data_list
        #print(max(dtlist))
        #print(min(dtlist))
        #print(sum(dtlist)/len(dtlist))
        plt.plot(dtlist)
        plt.show()
    


debugger = Debugger()
#debugger.debug = True






#=====================================UPDATE OCCURS
def update(dt):
    #fps = pyglet.clock.get_fps()
    #print(fps)    #or 1/dt-errors div/0
    
    #----input manager #assume it called before ondraw
    controller.update(dt)

    #dx,dy = controller.mouse_value.get_dxdy()
    #cam.mouse_move(dx,dy)

    #dx,dy = mouse_value.get_dxdy()
    
    #---------------------dt deal
    #print(dt)
    for actor in world.actor_list:
        actor.update(dt)
    #cam.update(dt) #bacically cam also a actor. update as actor.
    #dont: for cam in camera_list: cam.update()
    
    debugger.update()

pyglet.clock.schedule(update)#passes dt. for maxspeed. finally! with vsync.



#=====================================MOUSE EVENT
class Mouse_value:
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

#mouse_value = Mouse_value()
#also moved controller.
#class but remained out here.

@window.event
def on_mouse_motion(x, y, dx, dy):
    controller.on_mouse_motion(x, y, dx, dy)
    #mouse_value.x += dx
    #mouse_value.y += dy



#=====================================KEY EVENT
from pyglet.window import key
@window.event
def on_key_press(symbol,modifiers):
    controller.on_key_press(symbol,modifiers)#finayll with modifiers!
    #we move it to player controller.
    #for actor in world.actor_list:
    #    actor.on_key_press(symbol)
    
    #we try treat a cam as also an actor
    # for camera in world.camera_list:
    #     camera.on_key_press(symbol)
    debugger.on_key_press(symbol)

@window.event      
def on_key_release(symbol, modifiers):
    controller.on_key_release(symbol,modifiers)

    #for actor in world.actor_list:
    #    actor.on_key_release(symbol)
    # for camera in world.camera_list:
    #     camera.on_key_release(symbol)



#=====================================CONTROLLER FOR BOTH KEY-MOUSE-MAYBEMORE!
class Controller:
    def __init__(self):
        self.mouse_value = Mouse_value()

    def on_mouse_motion(self, x,y,dx,dy):
        self.mouse_value.x += dx
        self.mouse_value.y += dy

    def on_key_press(self, symbol,modifiers):
        for actor in world.actor_list:
            if getattr(actor, "on_key_press", None): #callable(return_of_getattr)
                actor.on_key_press(symbol)
    def on_key_release(self, symbol,modifiers):
        for actor in world.actor_list:
            if getattr(actor, "on_key_press", None):
                actor.on_key_release(symbol)
    
    def update(self, dt):
        dx,dy = self.mouse_value.get_dxdy()
        cam.mouse_move(dx,dy)


controller = Controller()



#=====================================DRAW EVENT
@window.event
def on_draw():
    #glClear(GL_COLOR_BUFFER_BIT)
    glClearColor(0.0, 0.24, 0.5, 1.0)
    glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)   


#---------------------------------------each shader, each draw loop ??
#----------------------since shader contains MVP..
#----------------------------------- kinds like group of pyglet.
    program = shader_default    #shaderprogram too long..
    
    glUseProgram(program)
    #========================when using some shader:
    #--------MVP
    # V,P may remained while actor changes model.
    projectionmat = world.camera_list[0].get_matrix_projection() #want world.currentcam kidns..
    viewmat = world.camera_list[0].get_matrix_view()
    
    projectionmatID = glGetUniformLocation(program, "Projection")
    glUniformMatrix4fv(projectionmatID,1,True, projectionmat)
    viewmatID = glGetUniformLocation(program, "View")
    glUniformMatrix4fv(viewmatID,1,True, viewmat)

    #--------draw each actor
    # GL_POINTS  GL_LINE_STRIP  GL_TRIANGLES
    for actor in world.actor_list: # xxx_list named to: 'maybe use for loop'
        #--------MODEL
        modelmat = actor.get_matrix_model()                
        modelmatID = glGetUniformLocation(program, "Model")#True if row major. [ [1,2,3,4],,
        glUniformMatrix4fv(modelmatID,1,True, modelmat)
        
        for vbo,textures in actor.mesh_list:#mesh, which contains vbo1-tex1-tex2..
            for i, texture in enumerate(textures):
                
                #program.set_texture(i, texture.id ) #hopefully it's the one..

            #in Myshader:
            #def set_texture(self, i, textureID):
                shader_program = program
                if i == 0:
                    shader_textureID = 'tex0'
                    tex_index = 0
                    activate_target = GL_TEXTURE0
                elif i == 1:
                    shader_textureID = 'tex1'
                    tex_index = 1
                    activate_target = GL_TEXTURE1
                glsltexID = glGetUniformLocation(shader_program, shader_textureID)
                glUniform1i(glsltexID, tex_index) # 0 means GL_TEXTURE0, 0th texture.        
                glActiveTexture(activate_target)
                glBindTexture(GL_TEXTURE_2D, texture.id)

            vbo.draw(GL_TRIANGLES)
        
    #world.batch.draw() # we do not use it yet. system too complex, no freedom.

pyglet.app.run()