#import glfw
from glfw.GLFW import *

def see_dirs():
    a = dir(glfw)
    for i in a:
        if 'ime' in i:
            print(i)
    #from glfw.GLFW import glfwGetTime
    #print(help(glfw.get_time))
    #print(help(glfwGetTime))

#https://www.glfw.org/docs/3.3/group__init.html#ga110fd1d3f0412822b4f1908c026f724a
#but seems only joystick hat..
#glfwInitHint(GLFW_VERSION_MAJOR, 4)
#glfwInitHint(GLFW_VERSION_MINOR, 2)

# Initialize the library
if not glfwInit():#need thread safe, run by mainthread.
    raise Exception('glfw init error')

class Window:
    """single window design."""
    def __init__(self, windowname = 'a window'):
        #hits int or str. do before create window.!
        #glfwWindowHint
        #glfwWindowHintString
        #glfwDefaultWindowHints

        print(GLFW_VERSION_MAJOR)
        print(GLFW_VERSION_MINOR)
        print(GLFW_VERSION_REVISION)
        #https://learnopengl.com/Getting-started/Hello-Window
        #https://www.glfw.org/docs/3.3/window_guide.html
        #https://kyoungwhankim.github.io/ko/blog/opengl_window/
        glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 4)
        glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3)
        #glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GLFW_TRUE)        
        #glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE)#compat works.
        glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_COMPAT_PROFILE)#compat works.
        #https://stackoverflow.com/questions/58022707/glvertexattribpointer-raise-gl-invalid-operation-version-330
        #Since you use a core profile ... the default Vertex Array Object 0 is not valid
        #i see.. compatibility,, 0 is automatically set.

        #If requesting an OpenGL version below 3.2, GLFW_OPENGL_ANY_PROFILE must be used.
        #If OpenGL ES is requested, this hint is ignored.
        
        #glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 2)
        #'Context profiles are only defined for OpenGL version 3.2 and above'
        print(GLFW_CONTEXT_VERSION_MAJOR)
        glfwWindowHint(GLFW_RESIZABLE,GLFW_FALSE)
        glfwWindowHint(GLFW_FLOATING, GLFW_TRUE)
        glfwWindowHint(GLFW_TRANSPARENT_FRAMEBUFFER, GLFW_TRUE)
        #glfwWindowHint(GLFW_CENTER_CURSOR , GLFW_TRUE)
        #glfwWindowHint(GLFW_DECORATED , GLFW_FALSE)#cool!
        
        monitor1 = glfwGetPrimaryMonitor()
        monitor1 = None
        window = glfwCreateWindow(640, 480, windowname, monitor1, None)
        #https://www.glfw.org/docs/3.3/window_guide.html
        print(glfwGetError())
        print(glfwGetVersion())
        s = glfwGetVersionString()
        print(s)

        

        if not window:
            raise Exception('no window created!')
        glfwMakeContextCurrent(window)
        # tell GLFW to capture our mouse
        #glfwSetInputMode(window, GLFW_CURSOR, GLFW_CURSOR_DISABLED)
        #glEnable(GL_DEPTH_TEST)
        #glClearColor(0.1, 0.1, 0.1, 1.0)
        #glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

        self.window = window
        self.events=[]
        self.set_current()
        self.bind_input()
    def set_time(self, time=120):
        #just sets internal time. for test..?
        glfwSetTime(time)
    def close(self):
        window = self.window
        glfwSetWindowShouldClose(window,True)
        #glfwDestroyWindow
    def set_current(self):
        window = self.window
        glfwMakeContextCurrent(window)
    def bind_input(self):
        #events = self.events not this. this becomes new object. use self.events directly.

        #bind all events. since file drop occured by event..
        #step 1. all call funcs.
        def drop_callback(path_count, paths):
            #no window, why??
            #https://www.glfw.org/docs/3.3/group__input.html#ga1caf18159767e761185e49a3be019f8d
            #path_count
            #<glfw.LP__GLFWwindow object at 0x0000028FE773B7C0>
            #print(int(path_count))#b'\x90\xca\xc5\xd7\x97\x02\x00\x00' .. bury it.
            #paths
            #['C:\\Users\\liltm\\Desktop\\vvv.png', 'C:\\Users\\liltm\\Desktop\\ff.png']    
            print(paths)
            event = paths
            self.events.append(event)

        def key_callback(window, key, scancode, action, mods):
            #if (key == GLFW_KEY_ESCAPE and action == GLFW_PRESS):
            #    glfwSetWindowShouldClose(window,True)
            #print(key, scancode, action, mods)
            #action 0=unp 1=pressed 2pressing
            if action==1:
                event = {'type':'key_pressed','key':key}
            elif action==2:
                event = {'type':'key_pressing','key':key}
            elif action==0:
                event = {'type':'key_unpressed','key':key}
            self.events.append(event)

        #step 2. actual bind.
        window = self.window
        glfwSetKeyCallback(window, key_callback)
        glfwSetDropCallback(window, drop_callback)

    def input(self, events):
        1#print(events)
    def update(self, dt):
        1
    def draw(self):
        1
    def run(self):
        window = self.window
        timewas = 0
        while not glfwWindowShouldClose(window):
            #input, update(ai,physics), draw 3-type.
            #---1 input
            self.input(self.events)
            self.events = []

            #---2 update
            #t = glfw.get_timer_value()#20540838386 2054 is seconds.
            t = glfwGetTime()
            dt = t-timewas
            self.update(dt)
            
            #---3 draw
            glClearColor(0, 0, 0, 1)
            glClear(GL_COLOR_BUFFER_BIT)
            self.draw()#[]=empty world
            # Swap front and back buffers
            glfwSwapBuffers(window)
            glfwPollEvents()#this , is the input! but to next time!

        glfwTerminate()#This function destroys all remaining windows and cursors, 






#low level objects
#we need vao, atleast.
#..but also shader.ha..
#..we do shader.
from OpenGL.GL import *
from OpenGL.GL import shaders

vertn = """
#version 410 core
layout (location = 0) in vec3 pos;
layout (location = 1) in vec3 color;
out vec3 ocolor;
void main() 
{
    gl_Position = vec4( pos, 1);
    ocolor = color;
}
"""

fragn = """
#version 410 core
in vec3 ocolor;
out vec4 FragColor;
void main()
{
    FragColor = vec4(1,1,0,1);
    //FragColor = vec4(0,0,0,0);
}
"""
def shasha():
    assert bool(glCreateShader)#sometimes compile error occurs, before window() 
    vshader = shaders.compileShader( vertn, GL_VERTEX_SHADER)
    fshader = shaders.compileShader( fragn, GL_FRAGMENT_SHADER)
    program = shaders.compileProgram( vshader,fshader)
    glUseProgram(program)
    glPointSize(10)
import numpy as np


class Vbo:
    def __init__(self, pos):
        VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, VBO)
        vertices = np.array([0,0,0, 0.5,0,0, 0,0.5,0]).astype('float32')
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        fsize = np.float32(0.0).nbytes
        stride = 3 * fsize
        offset = ctypes.c_void_p(0)
        glEnableVertexAttribArray(0)
        glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, offset)
        self.VBO = VBO
    def draw(self):
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glDrawArrays(GL_POINTS, 0,3)

class Vao:
    def __init__(self, pos, color=None):
        vertices = np.array( [0,0,0, 0.5,0,0, 0,0.5,0] ).astype('float32')
        indices = np.array( [0,1,2] ).astype('uint')#not uint8 but uint. since:GL_UNSIGNED_INT
        
        VAO = glGenVertexArrays(1) # create a VA. if 3, 3of VA got. #errs if no window.
        VBO = glGenBuffers(1) #it's buffer, for data of vao.fine.
        EBO = glGenBuffers(1) #indexed, so EBO also. yeah.
        glBindVertexArray(VAO) #gpu bind VAO
        glBindBuffer(GL_ARRAY_BUFFER, VBO) #gpu bind VBO in VAO
        glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, indices.nbytes, indices, GL_STATIC_DRAW)

        # fsize = np.float32(0.0).nbytes
        # stride = 3 * fsize
        # offset = ctypes.c_void_p(0)
        # glVertexAttribPointer(0, 3, GL_FLOAT, GL_FALSE, stride, offset)
        # glEnableVertexAttribArray(0)

        #this only for location 0. not works to 1..
        attrs = {'position':vertices}
        points = len(attrs['position'])//3
        fsize = np.float32(0.0).nbytes #to ensure namespace-safe.        
        offset = ctypes.c_void_p(0)
        loc = 0#NOTE:opengl core no attr 0.
        stride = 3* fsize
        for data_array in attrs.values():
            data_len = len(data_array)
            size = data_len//points#size 2,3,4
            #loc = glGetAttribLocation(shader.ID, attrname)
            glEnableVertexAttribArray(loc)
            glVertexAttribPointer(loc, size, GL_FLOAT, GL_FALSE, stride, offset)
            offset = ctypes.c_void_p(data_len*fsize)
            loc+=1

        self.VAO = VAO
        self.VBO = VBO
        self.EBO = EBO
        self.points = len(indices)
    def draw(self):        
        glBindVertexArray(self.VAO)
        glDrawElements(GL_POINTS, 3, GL_UNSIGNED_INT, None)






#______high level objects

class Inputmanager:
    def __init__(self):#init without window, maybe we simulate events.!
        self.window = None
    def input(self, events):
        """actual process inputs(events)"""
        for i in events:
            if '256' in str(i):
                if self.window:
                    self.window.close()
            print(i)
    def bind(self, window):
        """let the window bound"""
        self.window = window
        window.input = self.input

class World:
    def __init__(self):
        self.actors = []
    def update(self, dt):
        if int(dt%2)==0:
            print(dt)
    def bind(self, window):
        window.update = self.update

class Renderer:
    def __init__(self):
        self.targets = []
    #def render(self, world_or_actors_or_target, camera=None, window = None, pos_aabb=None):
    def render(self, target, camera=None):
        """add render target
        all inputs become draw-ready objects."""
        #world,maybe just 1 simulated,.. if you can multi world, but dt takes time..
        #cam that sees world
        #window that draws from camera.


        
        shasha()#init shader here..? course not! its for temp.
        
        if hasattr(target, 'maincam'):
            camera = target.camera[0]
        if camera == None:
            camera = 1#Camera()


        #if isinstance(target, World): not this strict way.
        if isinstance(target, World):
            for i in target.actors:
                self.targets = []

        if isinstance(target, list):
            vao = Vbo(target)
            self.targets = [vao]

    def draw(self):
        """real draw. set MVP.."""
        for i in self.targets:
            i.draw()
        print('i rendered')
    def bind(self, window):
        """window runs and calls this"""
        window.draw = self.draw










def main():
    w = Window('w1')
    
    #---old but independant way
    def custom_input_function(events):
        for e in events:
            if e['key']==256:#we need class not dict.
                w.close()
    #w.input = lambda y:print(y)
    #w.input = custom_input_function

    #--from the concept
    #inputmanager = Inputmanager(window)
    #inputmanager.input(window)
    #--we arrived here. see input changed bind.
    i = Inputmanager()
    #w.input = i.input
    i.bind(w)#thats the way!
    #means i.get_events_from(w)
    #and i shall send events to ..controller? world? world seems fair.
    

    world = World()
    #world.update(dt) #not thisway.
    world.bind(w)
    #means world.get_dt_from(w)
    #and simulated. fine. no need more.



    r = Renderer()#..holds mvp bind kinds. it shall not be in world nor window.yeah.
    r.bind(w)
    #r.render(world)
    r.render([0,0,0, 0.5,0,0, 0,0.5,0])

    #def mydraw():
        #set mvp
        #vao = vao()
        #vao.bind()
        #vao.draw()
    #render.draw = mydraw
    
    #r.render('ham')
    #r.get_world_from(w) or actors. or mesh or vao or [0,0,0, 1,0,0, 0,1,0]..?
    #NO!!! render requires world, but not from window.
    #r.render(world)#maybe, world or [actors] or kinds.
    #r.render([0,0,0, 1,0,0, 0,1,0])#yeah. default cam 0,0,-2?

    #basically we want []s, ,means we need actor class not [?].
    
    #and, window draw is performed by r.
    #window holds world, for simulation.

    w.run()
if __name__ == "__main__":
    main()