#import glfw
from glfw.GLFW import *
from OpenGL.GL import *

def see_dirs():
    a = dir(glfw)
    for i in a:
        if 'ime' in i:
            print(i)
    #from glfw.GLFW import glfwGetTime
    #print(help(glfw.get_time))
    #print(help(glfwGetTime))


# Initialize the library
if not glfwInit():#need thread safe, run by mainthread.
    raise Exception('glfw init error')

from time import time



class Window:
    main = True
    windows = []
    #focused = None if destroy, we need more task. just for 10 of windows. not slow!
    """single window design."""
    def __init__(self, windowname = 'a window'):
        #anyway we use 4-buffer, 2 camera, draw scene 2x, send them via jpg or webp.fine.
        #glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3);
        #glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 2);
        #glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, GL_TRUE);
        #glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE);
        #glfwWindowHint(GLFW_STEREO, GL_TRUE);
        #glGetBooleanv(GLFW_STEREO)
        #window = glfwCreateWindow(640, 480, windowname, glfwGetPrimaryMonitor(), None)

        window = glfwCreateWindow(640, 480, windowname, None, None)
        self.window = window
        self.main = self.__class__.main
        self.__class__.main = False
        #self.count = self.__class__.counter
        #self.__class__.counter+=1
        self.windows.append(self)
        self.focused = False
        
        def xx(www,state):
            1
            #input www is global window. not that..
            print(www,state)
            print(self,'state')#is this the only way???
            #if self.__class__.windows == []:
            #    1
            #window same however.
        glfwSetWindowFocusCallback(window,xx)
    def close(self):
        if self.main:
            glfwSetWindowShouldClose(self.window,True)
        else:
            self.destroy()
    def destroy(self):
        idx = self.__class__.windows.index(self)
        self.__class__.windows.pop(idx)
        glfwDestroyWindow(self.window)
        print('alldone')

    def focus(self):#note: this .. all gl acts here. even still controll is there.
        window = self.window
        # Make the window's context current
        glfwMakeContextCurrent(window)

        for i in Window.windows:
            i.unbind()
        self.bind()
        self.__class__.focused = self
    def unbind(self):
        window = self.window
        def nofun(*args, **kwargs):print('no')
        glfwSetKeyCallback(window, nofun)
        glfwSetDropCallback(window, nofun)
    
    #def bind(self, excepts=[]):
        """excepts of 'key', drop, mmove, mbutton, ,,"""
    def bind(self):#basically we need to all unbind and bind self.. except main's exit.
        #..what if all func is just bound always, but only event happens.. to inputmanager?
        #of just  get events from focused one. or current one. focused fine.
        #and if we track cursor, need capture alwayse m's pos. this also basic feature~esc
        #bind all events. since file drop occured by event..
        window = self.window
        glfwSetKeyCallback(window, key_callback)
        glfwSetDropCallback(window, drop_callback)

    def set_time(self, time=120):
        #just sets internal time. for test..?
        self.focus()
        window = self.window
        glfwSetTime(time)

    def draw(self):
        window = self.window
        #print('drawing(' , f'{window}')
        #glClearColor(1,0,1,1)
        #glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glfwSwapBuffers(window)


    def run(self):
        self.focus()
        self.bind()
        window = self.window
        timewas = glfwGetTime()
        t2was = time()
        beg = time()
        dts = 0
        dts2=0
        while not glfwWindowShouldClose(window):
            #input, update(ai,physics), draw 3-type.
            glfwPollEvents()#this , is the input!
            
            # Render here, e.g. using pyOpenGL
            #t = glfw.get_timer_value()#20540838386 2054 is seconds.
            t = glfwGetTime()
            dt = t-timewas
            timewas = t
            dts+=dt

            t2 = time()
            dt2 = t2-t2was
            #print(dt-dt2)
            if dt-dt2>0.001:#less 1ms..
                print(dt,dt2)
            t2was = t2
            dts2+=dt2
            #9.112866640090942 end intertime
            #9.1122746 9.112866640090942

            #2120.0516250133514 end intertime
            #2120.035877 2120.0356678962708
            #2 test means, time-safe. we can use any of way.
            #3600s, 36ms slip.

            # Swap front and back buffers
            #glfwSwapBuffers(window)
            for win in Window.windows:
                win.draw()

            # Poll for and process events

        print(time()-beg,'end intertime')
        print(dts,dts2)
        glfwTerminate()#This function destroys all remaining windows and cursors, 

#def drop_callback(window, path_count, paths):
def drop_callback(path_count, paths):
    #no window, why??
    #https://www.glfw.org/docs/3.3/group__input.html#ga1caf18159767e761185e49a3be019f8d
    #path_count
    #<glfw.LP__GLFWwindow object at 0x0000028FE773B7C0>
    #print(int(path_count))#b'\x90\xca\xc5\xd7\x97\x02\x00\x00' .. bury it.
    #paths
    #['C:\\Users\\liltm\\Desktop\\vvv.png', 'C:\\Users\\liltm\\Desktop\\ff.png']    
    print(paths)

def key_callback(window, key, scancode, action, mods):
    #https://www.glfw.org/docs/3.3/group__keys.html
    if (key == GLFW_KEY_SPACE and action == GLFW_PRESS):
        print('space')
        #print(str(Window.focused.window) , str(window) )
        #<glfw.LP__GLFWwindow object at 0x000001FDB3B313C0>
        #<glfw.LP__GLFWwindow object at 0x000001FDB3B31BC0>
        #if Window.focused.window == window:
        #see, hard to act like. window is required..thats why inputmanager.
        #after, input event delivered to actor, in this case, window object.
        #that knows itself if focused. .. or what.
        #hope we not store window.focused . too dirty. easy to forget.

        w2 = Window('w222')
        w2.focus()

    if (key == GLFW_KEY_R and action == GLFW_PRESS):
        ww = Window.focused
        print(ww,'rr')
    if (key == GLFW_KEY_E and action == GLFW_PRESS):
        #do once. see d.buffer.
        glClearColor(1,0,0,1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    if (key == GLFW_KEY_F and action == GLFW_PRESS):
        glClearColor(1,1,0,1)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    if (key == GLFW_KEY_0 and action == GLFW_PRESS):
        w = Window.windows[0]
        w.focus()
        print(0)
    if (key == GLFW_KEY_1 and action == GLFW_PRESS):
        w = Window.windows[-1]
        w.focus()
        print(1)

    if (key == GLFW_KEY_ESCAPE and action == GLFW_PRESS):
        Window.windows[-1].close()
        #glfw.SetWindowShouldClose(window, True)
        #glfw.set_window_should_close(window, True)
        #glfwSetWindowShouldClose(window,True)
        #too hard way.
        #we just send all inputs to inputmanger.fine.

#glfw.set_window_focus_callback


#=_-more to know
#https://www.glfw.org/docs/3.3/group__window.html#gade3593916b4c507900aa2d6844810e00
#GLFW_DOUBLEBUFFER
#GLFW_SAMPLES
#GLFW_STEREO ...see 4k jpg:1MB, 100fps, 100MB/s. we can consider webp..?
#GLFW_TRANSPARENT_FRAMEBUFFER

def main():
    w = Window('w1')
    w.run()
if __name__ == "__main__":
    main()