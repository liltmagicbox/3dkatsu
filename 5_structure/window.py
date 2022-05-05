#import glfw
from glfw.GLFW import *
from OpenGL.GL import *

import os
from PIL import Image

icon_fdir = 'icon.jpg'
icon_fdir = 'tick_after_glfwtimer.jpg'
icon_fdir = 'favicon.ico'
icon_fdir = 'yum.png'

def set_icon(window, fdir=None):#32 jpg default all.fine. 
    """best 16x16, 32x32 48x48.
    If passed an array of candidate images, those of or closest to the sizes
    desired by the system are selected.
    """
    #glfwSetWindowIcon(window, 2, [img1,img2]) 0 of sys default
    if fdir == None:
        glfwSetWindowIcon(window, 0, [])
        return
    if not os.path.exists(fdir):
        glfwSetWindowIcon(window, 0, [])
        return
    img = Image.open(fdir)
    glfwSetWindowIcon(window, 1, img)

from general import Logger, YAML, timef, Plotter, Uuid,Name
NAME = Name()
UUID = Uuid()

log = Logger(print=True)

#===============glfw minimum requirements.
#(event callback) seems anywhere.
#====on setup
#glfw.init()
#glfwWindowHint#before window
#window = glfw.create_window(640, 480, 'new window', None, None)
#glfw.make_context_current(window)#we gl, we write to here.
#glEnable#after context(window)
#====on draw
# glClearColor(0, 0, 0, 1)
# glClear(GL_COLOR_BUFFER_BIT)
# glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)#if glEnable(GL_DEPTH_TEST)
# glfw.swap_buffers(window)
# glfw.poll_events()
#====after run, return ram
#glfwTerminate()
#===============glfw minimum requirements.


#============================gl else
#glfwSetTime(time)
#glfwGetFramebufferSize(window)#need callback?
#glfwGetWindowAttrib.. not that. i like .ini , not in-game menu.
#print(glfw.get_version_string())
#glGetString(GL_VERSION)#b'4.6.0 NVIDIA 456.71'
#glGetString(GL_SHADING_LANGUAGE_VERSION) #b'4.60 NVIDIA'

#glfw.get_video_modes(monitor1)
#GLFWvidmode(size=Size(width=720, height=480), bits=Bits(red=8, green=8, blue=8), refresh_rate=60)
#GLFWvidmode(size=Size(width=1920, height=1080), bits=Bits(red=8, green=8, blue=8), refresh_rate=75)

#about depth testing:
#glEnable(GL_DEPTH_TEST)#test, discard fragment.
#glDepthMask(GL_FALSE)#tmp stops write to depth buffer.
#glDepthFunc(GL_LESS)#GL_ALWAYS
#https://learnopengl.com/Advanced-OpenGL/Depth-testing



#@vsync.setter
# def vsync(self,vsync):
#     """limit fps(powersave)by monitor. if slow draw, skips next loop."""
#     if vsync:
#         glfwSwapInterval(1)#0<0.001ms, 1:16ms,2:33ms, 10:5frame/s ..tearing(0)?
#     else:
#         glfwSwapInterval(0)
#     self._vsync = vsync

#=======this implements read-only.
    # @property
    # def main(self):
    #     return self._main
    # @main.setter
    # def main(self,main):
    #     1#not allow to set it.

#============this is fixed settings. not changeable runtime.

# ifyouwant_setting_saveload_by_dict_glfw_hint_namedict = {
# 'transparent_fbuffer' : GLFW_TRANSPARENT_FRAMEBUFFER
# 'always_on_top' : GLFW_FLOATING
# 'resizable' : GLFW_RESIZABLE
# 'samples' : GLFW_SAMPLES
# 'decorated' : GLFW_DECORATED
# }

default_window_setting_dict={
'ifgles31shader':"#version 300 es \nprecision highp float;",
'gles31':False,

'gles31_glfwWindowHint':{
    'GLFW_CONTEXT_VERSION_MAJOR':3,
    'GLFW_CONTEXT_VERSION_MINOR':1,
    'GLFW_OPENGL_FORWARD_COMPAT':0,
    'GLFW_OPENGL_PROFILE':0,#GLFW_OPENGL_ANY_PROFILE = 0
    },

'glfwWindowHint':{
    'GLFW_RESIZABLE':0,
    'GLFW_DECORATED':1,
    'GLFW_FOCUSED':1,
    'GLFW_FLOATING':1,
    'GLFW_MAXIMIZED':0,#notfullscr.
    'GLFW_CENTER_CURSOR':1,#when fullscr.
    'GLFW_TRANSPARENT_FRAMEBUFFER':1,
    'GLFW_SAMPLES':4,
    'GLFW_DOUBLEBUFFER':1,
    #'GLFW_CONTEXT_RELEASE_BEHAVIOR':GLFW_RELEASE_BEHAVIOR_NONE,#he default value of
    #'GLFW_CLIENT_API':GLFW_OPENGL_ES_API,
    },
    #GLFW_CLIENT_API 는 컨텍스트를 생성할 클라이언트 API를 지정합니다.
    # 가능한 값은 GLFW_OPENGL_API, GLFW_OPENGL_ES_API및

'glEnable':[
    'GL_DEPTH_TEST',
    'GL_MULTISAMPLE',#default true already
    ],
'glDisable':[
    'GL_LINE_SMOOTH',
    ],

}

def load_window_settings(fdir):
    if os.path.exists(fdir):
        dd = YAML.load(fdir)
    else:
        dd = default_window_setting_dict
        YAML.save(dd,fdir)
    #gles31 = dd['gles31']
    return dd

def glfw_WindowHints(glfw_dict):
    for key,value in glfw_dict.items():
        #target = glfw_hint_namedict[key]
        target = globals()[key]                
        glfwWindowHint(target, int(value) )

#https://www.glfw.org/docs/3.3/window_guide.html
#glfwWindowHint(GLFW_DOUBLEBUFFER, False)#True/glfwSwapBuffers if vsync. else False/glFlush
#glfwWindowHint(GLFW_SAMPLES,4)#msaa
#glfwWindowHint(GLFW_TRANSPARENT_FRAMEBUFFER, True)#opacity works shader 1,0,0,0
#print(glfwGetWindowAttrib(window, GLFW_TRANSPARENT_FRAMEBUFFER))#default 1.

def gl_Enables(gl_list):
    for attr in gl_list:
        glattr = globals()[attr]
        glEnable(glattr)
def gl_Disables(gl_list):
    for attr in gl_list:
        glattr = globals()[attr]
        glDisable(glattr)

#glfwSetWindowAttrib
#see not that useful.
GLFW_DECORATED
GLFW_RESIZABLE
GLFW_FLOATING
GLFW_AUTO_ICONIFY
GLFW_FOCUS_ON_SHOW
#glfwSetWindowShouldClose.
#glfwSetWindowCloseCallback

def set_monitor(self, idx):
    #https://www.glfw.org/docs/3.3/monitor_guide.html#monitor_event
    #monitor1 = glfwGetPrimaryMonitor()#for full screen
    #monitors = glfwGetMonitors()
    #monitor = monitors[idx]
    #mode = glfwGetVideoMode(monitor)
    #m_width,m_height = mode.size
    #fps = mode.refresh_rate
    #something window pos change..?
    1

#little ram but fine. window 1st, renderer 2nd.
#if not glfwInit():#ready gl, load to ram
#    log.Exception('glfw init error')
glfwInit()


class Window:
    def __init__(self, yml_fdir = 'window_setting.yml'):
        #=====setting before window
        window_setting_dict = load_window_settings(yml_fdir)
        #------ special hint for gles31 for rpi4. default max gl version.
        gles31 = window_setting_dict['gles31']
        if gles31:#for low version 3.1 only.not3.0.        
            es31_dict = window_setting_dict['gles31_glfwWindowHint']
            glfw_WindowHints(es31_dict)
            log.log(glfw.get_version_string(), 'gles31 activated')
        
        #------hits before create window.
        glfw_dict = window_setting_dict['glfwWindowHint']
        glfw_WindowHints(glfw_dict)
        #=====creating window
        window = glfwCreateWindow(640, 480, 'a window', None, None)
        if window==None:
            log.Exception('no window error')
            return

        #======make current. gl state bound this window's context.
        glfwMakeContextCurrent(window)#this.. context.. grabs gl STATE.
        gl_Enables(window_setting_dict.get('glEnable',[]) )
        gl_Disables(window_setting_dict.get('glDisable',[]) )
        
        glfwSwapInterval(0)#not to vsync. for ensure.
        set_icon(window, icon_fdir)

        #====setting python class attrs
        #self.name = NAME.set('window',self)#more rigid.
        self.name = NAME.set(self)
        self.UUID = UUID.set(self)

        self.window = window #str repr of callback broken.
        self.events = []#all events polled here.
        
        #===intenal values
        self.skip_ratio = 0.0#if 2.0, skip 2*60 frames.(main 60hz)
        self.skip_counter = 0
        #self.event_halt_time = 0#become too complex.

        #====propertys.
        #==int/floats
        self.dt = 1/60 #this is more natural. not fps.
        #self.fps = 60 #@property
        
        #we dont need to store this. value is outside. @property dir() search-able!
        #self.size = (640,480)#this contains ratio also!
        #self.pos = (160,120)
        #self.width = 640
        #self.height = 480
        
        #==bool
        #self.is_msaa = False#onoff by glenable!
        #fps = 60 we not this. 1.vsync on, dosnt matter.  2.set fps, off vsync.
        #WE NOT USE VSYNC. all becomes very clear! (else vsync by monitor hz.. too bad.)
        
    def close(self):
        """set flag. window shall be deleted in loop start."""
        glfwSetWindowShouldClose(self.window,True)
    def close_check(self):
        """check after loop"""
        return glfwWindowShouldClose(self.window)
    def destroy(self):
        """actual destroyer"""
        UUID.delete(self.UUID)
        NAME.delete(self.name)        
        glfwDestroyWindow(self.window)#error occurs next draw code.
        self.window = None#we can not destroy py object.

    def glbind(self):#bind current make_current
        """make current requires 40ms of 1000x (12s:1ms)while gl int 4ms."""
        window = self.window
        current_window = glfwGetCurrentContext()
        if not window == current_window:
            glfwMakeContextCurrent(window)
    def current(self):self.glbind()


    def bind_callback(self, inputmanager):
        window = self.window
        #https://www.glfw.org/docs/3.3/group__input.html
        glfwSetErrorCallback(inputmanager.error_callback)#instead glfwGetError()
        glfwSetKeyCallback(window, inputmanager.key_callback)
        glfwSetMouseButtonCallback(window, inputmanager.mouse_callback)
        glfwSetCursorPosCallback(window, inputmanager.cursor_callback)
        glfwSetCursorEnterCallback(window, inputmanager.cursor_enter_callback)
        glfwSetScrollCallback(window, inputmanager.scroll_callback)
        glfwSetDropCallback(window, inputmanager.drop_callback)

        glfwSetFramebufferSizeCallback(window, inputmanager.fb_size_callback)
        glfwSetWindowPosCallback(window, inputmanager.pos_callback)
    
    #real window operations.
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
    def focus(self):#grab brutely. not wanted..
        glfwFocusWindow(self.window)#destructive.
    
    def set_gamma(self,value):
        """value 0.5-1.5 . bad for inter-monitor.."""
        value = clamp(0.5,1.5)
        monitor = glfwGetWindowMonitor(self.window)        
        glfwSetGamma(monitor, value)
    def set_title(self,value):
        glfwSetWindowTitle(self.window, value)
    #=============property
    #self.glbind() if gl functions used.(current context!)
    @property
    def fps(self):#0.001= 1ms
        return 1/self.dt
    @fps.setter
    def fps(self, fps):
        self.dt = 1/fps
    #window.fps = 30
    #fps = window.fps() and window.fps(30)

    @property
    def opacity(self):
        return glfwGetWindowOpacity(self.window)
        #return self.opacity
    @opacity.setter
    def opacity(self,opacity):
        glfwSetWindowOpacity(self.window, opacity)
    #============================size
    @property
    def size(self):
        return glfwGetWindowSize(self.window)
        #return self.size
    @size.setter
    def size(self,size):
        glfwSetWindowSize(self.window, size[0],size[1])
        #self.size = size
    @property
    def width(self):
        return glfwGetWindowSize(self.window)[0]
    @width.setter
    def width(self,width):
        height = glfwGetWindowSize(self.window)[1]
        glfwSetWindowSize(self.window, width,height)
    @property
    def height(self):
        return glfwGetWindowSize(self.window)[1]
    @height.setter
    def height(self,height):
        width = glfwGetWindowSize(self.window)[0]
        glfwSetWindowSize(self.window, width,height)
    

    #============================pos. window.x!
    #window.pos = (window.x+5,window.y+5). need property.
    #nx,ny = window.pos()[0]+5, window.pos()[1]+5 -bad! it frequenst self.value+=.
    #we can not window.x+=5,however. window.x=window.x+5 ..works! maybe 1.get 2.add 3.set
    @property
    def pos(self):
        return glfwGetWindowPos(self.window)
    @pos.setter
    def pos(self,pos):
        glfwSetWindowPos(self.window, pos[0],pos[1])
    @property
    def x(self):
        return glfwGetWindowPos(self.window)[0]
    @x.setter
    def x(self,x):
        height = glfwGetWindowPos(self.window)[1]
        glfwSetWindowPos(self.window, x,height)
    @property
    def y(self):
        return glfwGetWindowPos(self.window)[1]
    @y.setter
    def y(self,y):
        width = glfwGetWindowPos(self.window)[0]
        glfwSetWindowPos(self.window, width,y)

    #===================================cursor pos
    #for i in .. window.cursor_posx+=5
    @property
    def cursor_pos(self):
        return glfwGetCursorPos(self.window)
    @cursor_pos.setter
    def cursor_pos(self,cursor_pos):
        glfwSetCursorPos(self.window, cursor_pos[0],cursor_pos[1])
    @property
    def cursor_posx(self):
        return glfwGetWindowPos(self.window)[0]
    @cursor_posx.setter
    def cursor_posx(self,cursor_posx):
        height = glfwGetWindowPos(self.window)[1]
        glfwSetWindowPos(self.window, cursor_posx,height)
    @property
    def cursor_posy(self):
        return glfwGetWindowPos(self.window)[1]
    @cursor_posy.setter
    def cursor_posy(self,cursor_posy):
        width = glfwGetWindowPos(self.window)[0]
        glfwSetWindowPos(self.window, width,cursor_posy)
    

    def cursor_hide(self, lock=True):
        if lock:glfwSetInputMode(self.window, GLFW_CURSOR, GLFW_CURSOR_HIDDEN)
        else:glfwSetInputMode(self.window, GLFW_CURSOR, GLFW_CURSOR_NORMAL)

    def cursor_lock(self, lock=True):
        if lock:glfwSetInputMode(self.window, GLFW_CURSOR, GLFW_CURSOR_DISABLED)
        else:glfwSetInputMode(self.window, GLFW_CURSOR, GLFW_CURSOR_NORMAL)
        #bind mmove callback if c enabled.?
        #https://www.glfw.org/docs/3.3/group__input.html#gaa92336e173da9c8834558b54ee80563b        

    #don't know what current value is.
    # @property
    # def is_cursor_lock(self):
    #     state = glIsEnabled(GL_MULTISAMPLE)
    #     return state
    # @is_cursor_lock.setter
    # def is_cursor_lock(self, state):
    #     if state:glfwSetInputMode(window, GLFW_CURSOR, GLFW_CURSOR_DISABLED)
    #     else:glfwSetInputMode(window, GLFW_CURSOR, GLFW_CURSOR_NORMAL)

    def not_thisisbutseemsbad_cursor_pos(self, pos=None):
        if pos:
            x,y=pos
            glfwsetmousepos(x,y)
        else:
            return glfwGetCursorPos(self.window)
    
    #=============aspect and ..
    @property
    def ratio(self):
        x,y = glfwGetWindowSize(self.window)
        return x/y
    @ratio.setter
    def ratio(self, state):
        if state:
            x,y = glfwGetWindowSize(self.window)
            glfwSetWindowAspectRatio(self.window, x, y)
        else:
            glfwSetWindowAspectRatio(self.window, GLFW_DONT_CARE, GLFW_DONT_CARE)
    #glfwSetWindowSizeLimits(window, 100, 100, GLFW_DONT_CARE, GLFW_DONT_CARE)
    #glfwGetWindowContentScale(window, &xscale, &yscale);

    def fullscreen_off(self):
        x,y = 100,100
        w,h = self.size
        glfwSetWindowMonitor(self.window, None,x,y,w,h,0)
        #glfwSetWindowMonitor(glfwGetWindowMonitor(self.window), None,x,y,w,h,0)
    def fullscreen_on(self):#this no need to be attr of window.
        #if full:        
        #m_name = glfwGetMonitorName(monitor)

        #those 3 all different!!
        #monitor = glfwGetWindowMonitor(self.window)
        # monitor = glfwGetPrimaryMonitor()#for full screen
        # monitors = glfwGetMonitors()
        # for i in monitors:
        #     print(i,monitor,'=================mmmmm')
        #     print(glfwGetWindowMonitor(self.window),'getsingle')
        monitor = glfwGetPrimaryMonitor()
        mode = glfwGetVideoMode(monitor)
        mw,mh = mode.size
        fps = mode.refresh_rate
        glfwSetWindowMonitor(self.window, monitor, 0, 0, mw,mh, fps)

    #===============gl operation requires context current first
    #===================bool property is_.
    @property
    def is_msaa(self):
        self.glbind()
        state = glIsEnabled(GL_MULTISAMPLE)
        return state
    @is_msaa.setter
    def is_msaa(self, state):
        self.glbind()
        if state:glEnable(GL_MULTISAMPLE)
        else:glDisable(GL_MULTISAMPLE)

    @property
    def is_line_smooth(self):
        self.glbind()
        state = glIsEnabled(GL_LINE_SMOOTH)
        return state
    @is_line_smooth.setter
    def is_line_smooth(self, state):
        self.glbind()
        if state:glEnable(GL_LINE_SMOOTH)
        else:glDisable(GL_LINE_SMOOTH)

    @property
    def is_polygon_smooth(self):
        self.glbind()
        state = glIsEnabled(GL_POLYGON_SMOOTH)
        return state
    @is_polygon_smooth.setter
    def is_polygon_smooth(self, state):
        self.glbind()
        if state:glEnable(GL_POLYGON_SMOOTH)
        else:glDisable(GL_POLYGON_SMOOTH)

    

    def not_that_bad_msaa(self, value=None):
        self.glbind()
        if value==None:#not False.
            return glIsEnabled(GL_MULTISAMPLE)
        elif value==True:
            glEnable(GL_MULTISAMPLE)
        else:
            glDisable(GL_MULTISAMPLE)
    #window.is_msaa = True#bool seems not functional.
    #window.msaa(True)# value set.# this seems dont know whether 1 or 4..
    #window.msaa()
























#glfwGetClipboardString
#glfwSetClipboardString




    #============below need context current. gl operations.    
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
        """this hopely happens when: some, really critical time."""
        if glfwWindowShouldClose(self.window):
            self.close()
        if self.window == None:            
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

        run_begin = timef()
        timewas = timef()
        glfwSwapInterval(1)
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

            #time.sleep seems ~20ms ..20! minimum 14ms at windows10.!
            target_dt = self.dt
            time_spent = input_time + update_time + render_time
            halt_time = target_dt - time_spent
            #print(render_time)

            #wait_s = timef()
            # wait_time=0
            # while timef()-wait_s < halt_time:
            #     wait_time = (timef()-wait_s)#/self.fps
            # self.wait_times += wait_time

            #print(wait_time)
            #print(update_time, render_time, wait_time, '       took times')
            #print(timef()-t)


            #timer.append(render_time)
            #===for check time
            #st = timef()
            #something to check time.
            #times = timef()-st
            #timer.append(times)
        glfwTerminate()#This function destroys all remaining windows and cursors,

        run_time = timef()-run_begin

        p = Plotter()
        #p.plot(timer)
        #p.show()
        #p.save('pp.jpg')
        #print(timer)
















#framebuffer_size_callback(window: GLFWwindow, width: int, height: int) -> None:
# make sure the viewport matches the new window dimensions note that width and 
# height will be significantly larger than specified on retina displays.
#glViewport(0, 0, width, height)




#https://www.glfw.org/docs/3.3/group__window.html#gadd7ccd39fe7a7d1f0904666ae5932dc5
        # def window_pos_callback(window, xpos, ypos):
        #     print(xpos,ypos)            
        #     #xx = glfwGetFramebufferSize(window)
        #     #glfwSetFramebufferSizeCallback(window, framebuffer_size_callback);
        #     #basically when window changes, fbuffer changed.
        #     #content scale ratio of current DPI / platform's default DPI.
        
        # def key_callback(window, key, scancode, action, mods):
        #     #print(key, scancode, action, mods)
        #     #event = Event_key()
        #     if (key == GLFW_KEY_ESCAPE and action == GLFW_PRESS):
        #         self.close()
        #     #action 0=unp 1=pressed 2pressing
        #     if (key == GLFW_KEY_A and action == GLFW_PRESS):
        #         self.cursor_lock()
        #     if action==1:
        #         event = {'type':'key_pressed','key':key}
        #     elif action==2:
        #         event = {'type':'key_pressing','key':key}
        #     elif action==0:
        #         event = {'type':'key_unpressed','key':key}
        #     self._events.append(event)
        
        # def drop_callback(path_count, paths):#bury path_count. 
        #     #paths ['C:\\Users\\liltm\\Desktop\\vvv.png', 'C:\\Users\\liltm\\Desktop\\ff.png']
        #     for path in paths:
        #         #event = Event.filedrop(path)#or Event(type='filedrop',path)
        #         event = f"filedrop {path}"
        #         self._events.append(event)#..not inputs good name..
            
        # #step 2. actual bind.
        # window = self.window

        # def seterror_callback(error_code, description):
        #     log.error(error_code, description)
        












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


class Shader:
    def __init__(self):
        1
    def bind(self):
        1
class Texture:
    def __init__(self):
        1
    def bind(self,loc):#loc?
        1
class Vao:
    def __init__(self):
        1
    def bind(self):
        1
    def draw(self):
        1
#=============
class Material:
    def __init__(self):
        self.shader = Shader()
        self.texture_dict = {}
    def bind(self):
        self.shader.bind()
        for key,value in self.texture_dict.items():
            #0:tex0, 1:tex1...
            #phong color normal specular?
            #bsdf color normal metallic roughness
            # N or name.
            #i think name-seperate is required. not N.
            #find loc of shader, by name.
            loc = self.shader.find(key)
            loc = value.find(key)
            value.bind(loc)

class Mesh:
    def __init__(self):
        self.vao = Vao()
        self.material = Material()
    def draw(self):
        self.material.bind()
        self.vao.bind()
        self.vao.draw()#technically.

class Actor:
    def __init__(self):
        self.meshes = []
    def draw(self):
        for mesh in self.meshes:
            mesh.draw()

class Camera(Actor):
    def __init__(self):
        1


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


#====generalize here. not original form.
class Event_key:
    __slots__ = ['type','key', 'mods']
    def __init__(self, type,key,mods):
        self.type = type
        self.key = key
        self.mods = mods


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
    w = Window()
    #w.bind_callback()

    glClearColor(0,0,0, 0)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
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
    drawf()
    glfwSwapBuffers(w.window)
    w.y = 200
    for i in range(100):
        time.sleep(0.01)
        w.x+=10
    #time.sleep(2)
    
    #not that works
    # w.fullscreen_on()
    # w.x=0
    # w.y = 400
    # for i in range(100):
    #     time.sleep(0.01)
    #     w.x+=10
    # time.sleep(5)
    # w.fullscreen_off()
