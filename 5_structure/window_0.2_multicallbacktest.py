#import glfw
from glfw.GLFW import *
from OpenGL.GL import *

# Initialize the library
if not glfwInit():#need thread safe, run by mainthread.
    raise Exception('glfw init error')

from time import time
import random
#<glfw.LP__GLFWwindow object at 0x000002937F861740> focus
#<glfw.LP__GLFWwindow object at 0x000002937F861740> focus2
#740 is kind of general window class, seems class repr is bad.

#we can: know when create , window.
#we can't:  print( window of callback, is broken. but works fine to target.
#we bind only bound.

def xx(www,state):
    if state:
        print(www,'focus')

def xxx(www,state):
    if state:
        print(www,'focus2')

class Window:
    main = True
    def __init__(self, windowname = 'a window'):
        window = glfwCreateWindow(640, 480, windowname, None, None)
        main = self.__class__.main
        if main:self.__class__.main = False
        if main:
            glfwSetKeyCallback(window, key_callback)
            glfwSetWindowFocusCallback(window,xx)#whis this shares all?
            glfwSwapInterval(1)
        else:
            glfwSetKeyCallback(window, key_callback_sub)
            glfwWindowHint(GLFW_DOUBLEBUFFER, False)
            glfwSetWindowFocusCallback(window,xxx)#whis this shares all?

        self.window = window
        print(window,'created')
        
    def run(self):
        window = self.window
        glfwMakeContextCurrent(window)
        f=0.5
        while not glfwWindowShouldClose(window):
            glfwMakeContextCurrent(window)
            glClearColor(0,0.2,0,1)
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            
            f+= time()%1*0.01
            if f>1:
                f=0.5
            glColor3f(f, 0, 1)
            glBegin(GL_TRIANGLES)
            verts = [
            [-f,0,0],
            [f,0,0],
            [0,f,0],
            ]
            for vert in verts:
                glVertex3fv(vert)
            glEnd()

            glfwSwapBuffers(window)
            #glfwWaitEventsTimeout(5)
            glfwPollEvents()#this , is the input!       
           
        glfwTerminate()#This function destroys all remaining windows and cursors, 


def key_callback(window, key, scancode, action, mods):
    if (key == GLFW_KEY_SPACE and action == GLFW_PRESS):
        print('space')
        w2 = Window('w222')
    if (key == GLFW_KEY_Q and action == GLFW_PRESS):
        print('qqqqqqqqqqq')
    if (key == GLFW_KEY_F and action == GLFW_PRESS):
        glfwMakeContextCurrent(window)

def key_callback_sub(window, key, scancode, action, mods):
    if (key == GLFW_KEY_SPACE and action == GLFW_PRESS):
        print('only first born make baby!!')
    if (key == GLFW_KEY_F and action == GLFW_PRESS):
        glfwMakeContextCurrent(window)
    if (key == GLFW_KEY_R and action == GLFW_PRESS):
        #glfwDestroyWindow(window)
        glfwMakeContextCurrent(window)#NO! window broken in callback!
        c = random.random()
        #d = random.random()
        glColor3f(c, 0, 1)
        print(c)
        glBegin(GL_TRIANGLES)
        verts = [
        [-0.5,0,0],
        [0.5,0,0],
        [0,0.5,0],
        ]
        for vert in verts:
            glVertex3fv(vert)
        glEnd()
        #glClearColor(0.5,0.2,0,1)
        #glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glfwSwapBuffers(window)#not repr but works great to target window.
        #glFlush()
        #glFinish()
        #glfwPollEvents()
        #print('d')

def main():
    w = Window('w1')
    w.run()
if __name__ == "__main__":
    main()