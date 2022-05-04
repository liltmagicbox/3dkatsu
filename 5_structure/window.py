#import glfw
from glfw.GLFW import *

from general import Logger, YAML, timef, Plotter, Uuid,Name
NAME = Name()
UUID = Uuid()

log = Logger(print=True)

#https://webnautes.tistory.com/1103
def errorCallback(errcode, errdesc):
    #print('ERROR',errcode, errdesc)
    log.error(errcode, errdesc)
glfwSetErrorCallback(errorCallback)


#===============glfw minimum requirements.
#====on setup
#glfw.init()
#(window settings)
#window = glfw.create_window(640, 480, 'new window', None, None)
#glfw.make_context_current(window)#we gl, we write to here.
#(event callback)
#====on draw

# glClearColor(0, 0, 0, 1)
# glClear(GL_COLOR_BUFFER_BIT)
# glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)#if glEnable(GL_DEPTH_TEST)
# glfw.swap_buffers(window)
# glfw.poll_events()
#====return ram
#glfwTerminate()
#===============glfw minimum requirements.
        
dd = {
'name':'a window',
'gles31':False,

'glfwWindowHint':{
    
}
     }

YAML.save(dd,'window.yml')

from PIL import Image

#gl else
#glfwSetTime(time)
#glfwGetFramebufferSize(window)#need callback?
#glfwGetWindowAttrib.. not that. i like .ini , not in-game menu.


class Window:
    _main = True
    _windows = []#holding created window.
    _current = None
    """single window design."""
    def __init__(self, windowname = 'a window', gles31=False, contextwindow = None):
        main = self.__class__._main
        if main:self.__class__._main = False
        self.__class__._windows.append(self)

        if main:
            if not glfwInit():#ready gl, load to ram
                log.Exception('glfw init error')
            
            dd = YAML.load('window.yml')
            windowname = dd['name']
            gles31 = dd['gles31']
        
        #defualt gl max version. print(glfw.get_version_string())
        if gles31:#for low version 3.1 only
            glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3)
            glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 1)
            glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, False)
            glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_ANY_PROFILE)
        
        #but replace  or glFinish.
        #------hits before create window.
        #glfwWindowHint(GLFW_DOUBLEBUFFER, False)#True/glfwSwapBuffers if vsync. else False/glFlush
        glfwWindowHint(GLFW_CENTER_CURSOR , True)#find GLFW_CURSOR_DISABLED
        glfwWindowHint(GLFW_FLOATING, True)
        glfwWindowHint(GLFW_RESIZABLE, 1)
        
        #glfwWindowHint(GLFW_SAMPLES,4)#msaa
        #glfwWindowHint(GLFW_DECORATED, False)
        #glfwWindowHint(GLFW_TRANSPARENT_FRAMEBUFFER, True)#opacity works shader 1,0,0,0
        
        #https://www.glfw.org/docs/3.3/window_guide.html
        #glfwGetError()

        #-gl functions not glfw


        monitor1 = glfwGetPrimaryMonitor()#for full screen
        monitor1 = None
        window = glfwCreateWindow(640, 480, windowname, None, contextwindow)
        if window==None:
            log.Exception('no window error')
            return

        glfwMakeContextCurrent(window)#this.. context.. grabs gl STATE.
        #after gl settings. hopely after we only need in draw.. else we need make current.
        glEnable(GL_MULTISAMPLE)#default was True.
        glEnable(GL_DEPTH_TEST)


        #self.__class__._windows.append(self)#for multiwindow draw. remember to delete.NO!
        #not since .. if window_shooting kinds happens... never happens and main window owes.
        self.__class__._current = self#since we did avobe. this is the right way.
        self.name = NAME.set(self)
        self.UUID = UUID.set(self)
        self.window = window #str repr of callback broken.
        self._main = main#see @property.
        
        self._events = []
        self._update_funcs = []
        self._draw_funcs = []

        self.skip_ratio = 2.0#for sub-window, if 2.0, skip 2*60 frames.(main 60hz)
        if main:self.skip_ratio=0
        self._dt = 1/60#this is more natural. not fps.
        self.event_halt_time = 0
        self.skipped_frame = 0#not in renderer
        
        #self.current = False#for safe. if for context, ofcourse.
        self.cookie = 0#just clicker. update, little time( 0.6ms kinds not for time.sleep)

    def destroy(self):
        """common self destoryer. attrs."""
        UUID.delete(self.UUID)
        #print(self.__class__._windows,'before')
        self.__class__._windows.remove(self)
        #print(self.__class__._windows,'AFTER')
        self.window = None#this is the checker..or not. this brings error.

    def close(self):
        window = self.window
        if self.main:
            glfwSetWindowShouldClose(window,True)#in run. destroy all by..            
        else:
            #glfwSetWindowShouldClose(window,True)
            glfwDestroyWindow(window)#error occurs next draw code.
        self.destroy()
        

    def set_vsync(self, set = True):
        """limit fps(powersave)by monitor. if slow draw, skips next loop."""
        if set:
            glfwSwapInterval(1)#0<0.001ms, 1:16ms,2:33ms, 10:5frame/s ..tearing(0)?
        else:
            glfwSwapInterval(0)
    
    #=======this implements read-only.
    @property
    def main(self):
        return self._main
    @main.setter
    def main(self,main):
        1#not allow to set it.
    #=======this implements read-only.

    def _xxxset_fps(self, fps):
        """breaks vsync. waits at self.run """
        self.fps = fps
        self.set_vsync(False)
    @property
    def fps(self):#0.001= 1ms
        return int(1/self._dt)
    @property
    def dt(self):
        return self._dt
    @dt.setter
    def dt(self,dt):
        1#self._dt = dt
    @fps.setter
    def fps(self, fps):
        self._dt = 1/fps
        self.set_vsync(False)
    #===fps set, not set dt. since dt 16ms or 0.016s.

    def pos(self, pos=None):
        window = self.window
        if pos:
            x,y = pos
            glfwSetWindowPos(window, x,y)
        else:
            return glfwGetWindowPos(window)
    def size(self, size=None):
        window = self.window
        if size:
            x,y = size
            glfwSetWindowSize(window, x,y)
            glfwSetWindowAspectRatio(window, x, y)#dontcare if no need
        else:
            return glfwGetWindowSize(window)
        #glfwSetWindowSizeLimits(window, 100, 100, GLFW_DONT_CARE, GLFW_DONT_CARE)    
        #glfwGetWindowContentScale(window, &xscale, &yscale);

    def ratio(self, size=None):
        window = self.window
        w,h = size
        glfwSetWindowAspectRatio(window, w,h)

    def gamma(self,value):
        """bad for inter-monitor.."""
        value = clamp(0.5,1.5)
        monitor = glfwGetMonitors()[0]#shall we save window.monitor?
        glfwSetGamma(monitor, value)

    def cursor_pos(self, pos=None):
        if pos:
            x,y=pos
            glfwsetmousepos(x,y)
        else:
            return glfwgetmousepos()

    def cursor_lock(self, lock=True):
        window = self.window
        #glfwSetInputMode(window, GLFW_CURSOR, GLFW_CURSOR_HIDDEN)#just hidden mouse over
        if lock:
            glfwSetInputMode(window, GLFW_CURSOR, GLFW_CURSOR_DISABLED)
        else:
            glfwSetInputMode(window, GLFW_CURSOR, GLFW_CURSOR_NORMAL)
        #bind mmove callback if c enabled.?

    def set_icon(self, fdir=None):#hope we from data not from fdir..
        """best 16x16, 32x32 48x48.
        If passed an array of candidate images, those of or closest to the sizes
        desired by the system are selected.
        """        
        #glfwSetWindowIcon(window, 2, [img1,img2]) 0 of sys default
        img = Image.open(fdir)
        window = self.window
        glfwSetWindowIcon(window, 1, img)
        if not fdir:
            glfwSetWindowIcon(window, 0, [])

    def hide(self):
        glfwHideWindow(self.window)
    def show(self):
        glfwShowWindow(self.window)
    def iconfy(self):
        glfwIconifyWindow(self.window)
    def maximize(self):
        glfwMaximizeWindow(self.window)
    def attention(self):
        glfwRequestWindowAttention(self.window)#blink.wow.
    def focus(self):
        """grab brutely. not wanted.."""
        glfwFocusWindow(window)#destructive.


    def bind_callback(self):
        window = self.window
        #https://www.glfw.org/docs/3.3/group__window.html#gadd7ccd39fe7a7d1f0904666ae5932dc5
        def window_pos_callback(window, xpos, ypos):
            print(xpos,ypos)            
            #xx = glfwGetFramebufferSize(window)
            #glfwSetFramebufferSizeCallback(window, framebuffer_size_callback);
            #basically when window changes, fbuffer changed.
            #content scale ratio of current DPI / platform's default DPI.
        def key_callback(window, key, scancode, action, mods):
            if (key == GLFW_KEY_ESCAPE and action == GLFW_PRESS):
                self.close()
               #glfwSetWindowShouldClose(window,True)
            #print(key, scancode, action, mods)
            #action 0=unp 1=pressed 2pressing
            if (key == GLFW_KEY_A and action == GLFW_PRESS):
                self.cursor_lock()
            if (key == GLFW_KEY_B and action == GLFW_PRESS):
                self.cursor_lock(False)
            if (key == GLFW_KEY_W and action == GLFW_PRESS):
                #w2=Window(contextwindow = self.window)#hard to know what main is.
                w2=Window()
                w2.bind_callback()

            if (key == GLFW_KEY_D and action == GLFW_PRESS):
                def xx():
                    glBegin(GL_TRIANGLES)
                    verts = [
                    [-0.5,0,0],
                    [0.5,0,0],
                    [0,0.5,0],
                    ]
                    for vert in verts:
                        glVertex3fv(vert)
                    ts.append(timef())
                    glEnd()
                self.draw_push(xx)
            if action==1:
                event = {'type':'key_pressed','key':key}
            elif action==2:
                event = {'type':'key_pressing','key':key}
            elif action==0:
                event = {'type':'key_unpressed','key':key}
            self._events.append(event)
        
        def drop_callback(path_count, paths):#bury path_count. 
            #paths ['C:\\Users\\liltm\\Desktop\\vvv.png', 'C:\\Users\\liltm\\Desktop\\ff.png']
            for path in paths:
                #event = Event.filedrop(path)#or Event(type='filedrop',path)
                event = f"filedrop {path}"
                self._events.append(event)#..not inputs good name..
            
        #step 2. actual bind.
        window = self.window
        glfwSetWindowPosCallback(window, window_pos_callback)
        glfwSetKeyCallback(window, key_callback)
        glfwSetDropCallback(window, drop_callback)

    #============below need context current. gl operations.
    def get_glversion(self):
        a = glGetString(GL_VERSION)#b'4.6.0 NVIDIA 456.71'
        b = glGetString(GL_SHADING_LANGUAGE_VERSION) #b'4.60 NVIDIA'
        return a,b
    def get_monitor(self):
        #print(glfwGetWindowMonitor(window))<glfw.LP__GLFWmonitor object at 0x00000250FFE71F40>
        #print(glfwGetWindowAttrib(window, GLFW_TRANSPARENT_FRAMEBUFFER))#default 1.
        monitors = glfwGetMonitors()#)[<glfw.LP__GLFWmonitor object at 0x00000228D5740140>]
        monitor = monitors[0]
        glfwGetMonitorName(monitor)#)b'Generic PnP Monitor'
    
    def _bind(self):
        #currentwin = glfwGetCurrentContext()print(currentwin == self.window,'wwww') course not
        #https://stackoverflow.com/questions/45309537/glfw-one-context-for-all-windows
        if not self.__class__._current == self:
            glfwMakeContextCurrent(self.window)
            #print(self.__class__._current.name, self.__class__._current,'========>>>>>>',self.name,self)
            self.__class__._current = self
    def clear(self):#gl_ for requires contextcurrent. ..not_gl even bind() in it..
        """bind needed. glclearcolor,clearbuffer. change if not of those."""
        # if self.window==None:
        #     print('hhhhhhhhhhhh')
        # if glfwWindowShouldClose(self.window):
        #     print('hahaoijergajioweragiojgerawioj')
        # print(self.window)
        # glfwMakeContextCurrent(self.window)
        glClearColor(0, 0, 0, 1)#hope all same color.
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        #whatif stensil buffer? window knows what to do.
    def _swap(self):
        """not technically but near claer"""
        glfwSwapBuffers(self.window)#Swap front and back buffers#4e-5 0.00004 of empty.

    #=====================================
    def _input(self, _events):
        1#print(events)
    def _update(self, dt):
        for func in self._update_funcs:#now world2
            func(dt)
    def _draw(self):
        """actual draw call of an window"""
        self._bind()#simple, one bind, one draw. we don't need to check context..
        self.clear()
        for func in self._draw_funcs:
            func()
        self._swap()    
    #=====================================
    def update_push(self, func):
        """maybe its easy to def new draw..containing all. thats what was for."""
        self._update_funcs.append(func)
    def update_pop(self, func):
        """not that returns. just remove."""
        if func in self._update_funcs:
            self._update_funcs.remove(func)
            #idx = self._update_funcs.index(func)
            #self._update_funcs.pop(idx)
    def draw_push(self, func):
        """maybe its easy to def new draw..containing all. thats what was for."""
        self._draw_funcs.append(func)        
    def draw_pop(self, func):
        if func in self._draw_funcs:
            self._draw_funcs.remove(func)
    #==========================
    def _draw_main(self):
        """shall NOT be replaced by renderer."""
        for window in self.__class__._windows:
            if not window._draw_check():
                continue
            if window._threshold_check():
                window._draw()
    def _draw_check(self):
        if glfwWindowShouldClose(self.window):
            print('bbbbbbbbbbbbb')
            self.window.close()
        if self.window == None:
            print('draw check False=================\nFalse=================')
            return False
        return True
    def _threshold_check(self):
        #1M, loop.. actions adds 12ms to 20ms.  8 actions, 1k: 20us~100us
        if self.skip_ratio==0:#for visual seperation. 0 still works.
            return True
        else:
            self.skipped_frame += 1
            threshold = self.fps * self.skip_ratio#60*2.0=120 frames
            energy = self.skipped_frame #119not 121 y4eah
            if energy >= threshold:
                self.skipped_frame=0
                return True
            else:
                return False
    #============
    def run(self):
        if not self.main:
            log.Exception('it should be main(1st) window')
            #raise Exception()

        def timespent(t):
            nt = timef()
            spent = nt -t
            return spent, nt

        timer = []
        render_time = 0.001
        timewas = timef()
        #while not glfwWindowShouldClose(self.window):
        while not self.window==None:#this prevents destroyed window run.
            #t = glfw.get_timer_value()#20540838386 2054 is seconds.
            #t = glfwGetTime()#0.000001 both seems accuracy  1/1000 of 1ms.
            #we use more accurate time.perf_counter()
            t = timef()#remember timespent: glft 3seconds different.
            dt = t-timewas
            timewas = t
            #=================
            
            #=====input, update(ai,physics), draw 3-type.
            #---1 input
            if self.event_halt_time == 0:glfwPollEvents()#4e-4 0.0004
            else:glfwWaitEventsTimeout(self.event_halt_time)
            #else wait till Xseconds. it blocks mainloop.

            self._input(self._events)
            self._events = []
            input_time, t = timespent(t)

            #---2 update
            self._update(dt)
            update_time, t = timespent(t)

            # #case: render over dt
            # #update over dt            
            # min_simulation = 0.001#2/2ms fast enough. mach1 plane 360m/s, 36cm/s*2/2.
            # self.update(min_simulation)
            # update_time, t = timespent(t)
            
            # timetook = input_time + update_time + render_time
            # target_dt = 1/self.fps - min_simulation
            # timeleft = target_dt - timetook
            
            # updateN, revtinytime = divmod(timeleft,update_time)
            # tinytime = revtinytime/update_time
            # for i in range(updateN):
            #     self.update(min_simulation)
            
            # hangout = timef()
            # while timef()-hangout<tinytime:
            #     self.cookie+=1
            
            #---3 draw
            #self.draw()
            #for win in self.__class__._windows:#seems still best way..
            #not use: if class Window_advanced(Window).
            self._draw_main()#will be replaced to renderer.render
            render_time, t = timespent(t)

            #time.sleep seems ~20ms ..20!
            target_dt = self.dt
            timetook = input_time + update_time + render_time
            tinytime = target_dt - timetook

            # hangout = timef()
            # while timef()-hangout<tinytime:
            #     1


            #timer.append(render_time)
            #===for check time
            #st = timef()
            #something to check time.
            #times = timef()-st
            #timer.append(times)

        glfwTerminate()#This function destroys all remaining windows and cursors,

        p = Plotter()
        p.plot(timer)
        #p.show()
        #p.save('pp.jpg')
        #print(timer)


from OpenGL.GL import *



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
            if i['key']==49:
                a = glGetString(GL_VERSION)#b'4.6.0 NVIDIA 456.71'
                print(a)
                time.sleep(1)
                #exit()
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
        1
    def render(self, window, target, camera=None, posaabb=None):
        """add render target all inputs become draw-ready objects. and draw_push of window"""
        if hasattr(target, 'maincam'):
            camera = target.camera[0]
        if camera == None:#we can have many,many camera. hahaha!
            camera = 1#Camera()

        #if isinstance(target, World): not this strict way.
        if isinstance(target, World):#shall world not import window. it's fine.
            for i in target.actors:
                self.targets = []

        if isinstance(target, list):
            vao = Vbo(target)
            self.targets = [vao]
        
        def draw_func():
            #here set MVP.
            1
        window.draw_push(draw_func)



#input or key or general?
# class Event:
#     def __init__(self):
#         self.name = 
#         self.type = 
#         self.key

#{'type': 'key_unpressed', 'key': 49}

import time

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

#renderer = Renderer(window)#this limited init

#type1
# renderer = Renderer(window)#replace draw
# renderer.bind(window)
# renderer.render(world, world.maincam)
# renderer.render([actor1,actor2], cam)
# renderer.render('xxx.png')
# renderer.bind(window2)
# renderer.render(world, world.maincam)
# renderer.render([actor1,actor2], cam)
# renderer.render('xxx.png')

#win! this can easyly add or delete window.
#but not direct execution but add to dict of windows.
#but this was the only way of :renderer.render(window2, 'xxx.png')
#since we have .run of window, not of renderer. fine.
#_-type2
# renderer = Renderer(window)#replace draw
# #renderer.bind(window)#replace draw
# renderer.render(window, world, world.maincam)
# renderer.render(window, [actor1,actor2], cam)
# renderer.render(window, 'xxx.png')
# renderer.render(window2, 'xxx.png')

# window.run()#this brings input-update-draw cycle.

#OH, i wanted we update some slow window.. while main runs fast.


# def drawer():
#     renderer.bind(window)#even thisway!wow. renderer as gl connector
#     renderer.render(actor)#render is directly instructs.
    #actor.draw() not this way.!
#window.draw_push(drawer)# we shall never not win2.draw_push..



# from general import Clock
# clock = Clock()
# def update_render(time):
#     #dt = time-timewas
#     #timewas = time
#     dt = clock.dt()#each call.
#     world.update(dt)
#     #we cant since we update dynamically..
#     renderer.draw()


#window.update = update_render

if __name__ == "__main__":
    w = Window('w1')
    w.bind_callback()


    print(w.pos())
    w.pos( (500,500) )
    w.size( (300,300) )
    print(w.size())
    w.set_icon('icon.jpg')

    ts = []
    def drawf():
        glBegin(GL_TRIANGLES)
        verts = [
        [-1,0,0],
        [0.5,0,0],
        [0,0.8,0],
        ]
        for vert in verts:
            glVertex3fv(vert)
        ts.append(timef())
        glEnd()
    w.draw_push(drawf)


    def ttt(dt):
        #print(dt)
        print(1/dt)
    w.update_push(ttt)
    w.update_pop(ttt)

    #renderer = Renderer(w)
    w.fps=90
    #not w.set_fps(90). yeah.
    
    #time.sleep 0.0001 became 15ms kinds. while 0.0 is 1ns.
    for i in range(3):
        t = timef()
        time.sleep(0.0)
        print(timef()-t,'need 0.001')
    #w.update_push(timec)

    #window.fps set but dt. but dt not allows set.
    print(w.fps, w.dt)
    w.fps = 30
    print(w.fps, w.dt)
    w.dt = 16.666#not working. since 16ms or 0.016 problem.
    print(w.fps, w.dt)    

    #window.main read-only
    print(w.main)
    w.main = False
    print(w.main)
    w.main = True
    w.main = 55
    print(w.main)
    exit()

    w.run()

    X = []
    ii = ts[0]
    for i in ts:
        dt = i-ii
        ii = i
        X.append(dt)
    pp=Plotter()
    pp.plot(X)
    #pp.show()
