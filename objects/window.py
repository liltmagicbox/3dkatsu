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


# Initialize the library
if not glfwInit():#need thread safe, run by mainthread.
    raise Exception('glfw init error')

class Window:
    """single window design."""
    def __init__(self, windowname = 'a window'):
        window = glfwCreateWindow(640, 480, windowname, None, None)
        if not window:
            raise Exception('no window created!')
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
    def update(self,dt):
        1
    def draw(self):
        1
    def run(self):
        window = self.window
        timewas = 0
        while not glfwWindowShouldClose(window):
            #input, update(ai,physics), draw 3-type.
            #---1 input
            glfwPollEvents()#this , is the input!
            self.input(self.events)
            self.events = []

            #---2 update
            #t = glfw.get_timer_value()#20540838386 2054 is seconds.
            t = glfwGetTime()
            dt = t-timewas
            self.update(dt)
            
            #---3 draw
            self.draw()
            # Swap front and back buffers
            glfwSwapBuffers(window)

        glfwTerminate()#This function destroys all remaining windows and cursors, 


class Inputmanager:
    def __init__(self):
        1
    def input(self, events):
        for i in events:
            print(i)
    def bind(self, window):
        window.input = self.input

def main():
    w = Window('w1')
    
    #inputmanager = Inputmanager(window)
    #inputmanager.input(window)
    def custom_input_function(events):
        for e in events:
            if e['key']==256:#we need class not dict.
                w.close()

    #w.input = lambda y:print(y)
    #w.input = custom_input_function

    i = Inputmanager()
    #w.input = i.input
    i.bind(w)#thats the way!


    #r = Renderer()
    #r.render(world)

    w.run()
if __name__ == "__main__":
    main()