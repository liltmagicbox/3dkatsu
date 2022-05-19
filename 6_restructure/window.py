from glfw.GLFW import *
from OpenGL.GL import *

import os
from yamldict import YAML
from general import Uuid,Name, Logger
NAME = Name()
UUID = Uuid()
LOG = Logger()

import inputcaster
IC = inputcaster.InputCaster()


class BasicWindow:
    number = 0
    def __init__(self):
        if BasicWindow.number==0:
            glfwInit()
        setting_dict = load_window_settings('window_setting.yml')        
        hint = setting_dict['glfwWindowHint']
        enable = setting_dict['glEnable']
        disable = setting_dict['glDisable']

        glfw_WindowHints(hint)
        window = glfwCreateWindow(640, 480, 'a window', None, None)
        glfwMakeContextCurrent(window)
        gl_Enables(enable)
        gl_Disables(disable)
        
        glfwSwapInterval(0)
        glfwSetWindowSizeLimits(window, 100, 100, GLFW_DONT_CARE, GLFW_DONT_CARE)


        self.name = NAME.set(self)
        self.UUID = UUID.set(self)
        self.window = window
        BasicWindow.number+=1

    #===========
    def close(self):
        """set flag. window shall be destroyed in loop start."""
        glfwSetWindowShouldClose(self.window,True)
    def should_close(self):
        """check after loop"""
        return glfwWindowShouldClose(self.window)
    def destroy(self):
        """actual destroyer"""
        UUID.delete(self.UUID)
        NAME.delete(self.name)        
        glfwDestroyWindow(self.window)#error occurs next draw code.
        self.window = None
        BasicWindow.number-=1
        if BasicWindow.number==0:
            glfwTerminate()
    @property
    def count(self):
        """global window numbers"""
        return BasicWindow.number        
    #===================================
    def make_current(self):
        """make current requires 40ms of 1000x (12s:1ms)while gl int 4ms."""
        window = self.window
        current_window = glfwGetCurrentContext()
        if not window == current_window:
            glfwMakeContextCurrent(window)
    #===============gl operation requires context current first
    def gl_msaa(self, state=True):
        self.make_current()
        if state:
            glEnable(GL_MULTISAMPLE)
        else:
            glDisable(GL_MULTISAMPLE)
    def gl_line_smooth(self, state=True):
        self.make_current()
        if state:
            glEnable(GL_LINE_SMOOTH)
        else:
            glDisable(GL_LINE_SMOOTH)
    def gl_polygon_smooth(self, state=True):
        self.make_current()
        if state:
            glEnable(GL_POLYGON_SMOOTH)
        else:
            glDisable(GL_POLYGON_SMOOTH)



class InputWindow(BasicWindow):
    def bind_callback(self, IC):
        """IC is InputCaster, singleton"""
        window = self.window
        #https://www.glfw.org/docs/3.3/group__input.html
        #joystick requires polling. no callback!
        key_dict = inputcaster.map_keyboard
        mouse_dict = inputcaster.map_mouse
        mods_dict = inputcaster.map_mods
        mods_values = list(mods_dict.values())
        
        def error_callback(error_code, description):
            LOG.error(error_code, description, self.name,self.UUID)
        def char_callback(window, codepoint):#can pressing input.
            if (0x3130<= codepoint <= 0x318F)or\
            (0x1100<= codepoint <= 0x11FF) or\
            (0xAC00<= codepoint <= 0xD7A3) or\
            (30<= codepoint <= 128):#!*:
                #uni = '\u'+str(codepoint)
                uni = chr(codepoint)
                print(uni)
                abskey = "CHAR"
                value = uni
                IC.input(abskey, value, self.name, self.UUID)            
        def key_callback(window, key, scancode, action, mods):
            if action==2:
                return
            #action 0,1 and 2 pressing. mods 1 2 4 of shift ctrl alt
            key = key_dict.get(key, f"KEY_{key}")
            mods = mods_dict.get(mods, f"MODS_{mods}")
            abskey = key
            #assume CTRL+C only instant not pressing.
            if (action!=0 and mods!=''):
                abskey = mods+'+'+key
            if key in mods_values:#CTRL+CTRL
                abskey = key
            value = 1.0 if action==1 else 0.0#>0 occurs 2

            IC.input(abskey, value, self.name, self.UUID)
        def mouse_button_callback(window, button, action, mods):
            key = mouse_dict.get(button, f"M_BUTTON_{button}")
            mods = mods_dict.get(mods, f"MODS_{mods}")
            abskey = key
            if (action!=0 and mods!=''):
                abskey = mods+'+'+key
            value = 1.0 if action==1 else 0.0#>0 occurs 2

            IC.input(abskey, value, self.name, self.UUID)
        def scroll_callback(window, xoffset, yoffset):
            abskey = "M_SCROLL"
            value = 1.0 if yoffset>0 else -1.0
            IC.input(abskey, value, self.name, self.UUID)
        def cursor_pos_callback(window, xpos,ypos):
            abskey = "CURSOR_POS"
            value = (xpos,ypos)
            IC.input(abskey, value, self.name, self.UUID)

        def cursor_enter_callback(window, state):
            abskey = "CURSOR_ENTER"
            value = state
            IC.input(abskey, value, self.name, self.UUID)
        def drop_callback(window, path_count, ):#bury path_count. ->paths vanished.?
            #paths ['C:\\Users\\liltm\\Desktop\\vvv.png', 'C:\\Users\\liltm\\Desktop\\ff.png']
            #print(path_count)['C:\\Users\\Public\\Desktop\\Shotcut.lnk']
            paths=path_count
            for path in paths:
                #event = Event.filedrop(path)#or Event(type='filedrop',path)
                abskey = "FILEDROP"
                value = path
                IC.input(abskey, value, self.name, self.UUID)
        def window_pos_callback(window, xpos, ypos):#not from win.x+=5
            abskey = "WINDOW_POS"
            value = (xpos,ypos)
            IC.input(abskey, value, self.name, self.UUID)
        def fb_size_callback(window, width, height):
            self.make_current()
            glViewport(0, 0, width, height)#need context?
            #no draw, no update!
        def close_callback(window):
            glfwSetWindowShouldClose(window,True)
            self.close()
            self.destroy()
        glfwSetErrorCallback(error_callback)#instead glfwGetError()        
        glfwSetCharCallback(window, char_callback)
        glfwSetKeyCallback(window, key_callback)
        glfwSetMouseButtonCallback(window, mouse_button_callback)
        glfwSetScrollCallback(window, scroll_callback)
        glfwSetCursorPosCallback(window, cursor_pos_callback)
        glfwSetCursorEnterCallback(window, cursor_enter_callback)
        glfwSetDropCallback(window, drop_callback)
        glfwSetWindowPosCallback(window, window_pos_callback)
        glfwSetFramebufferSizeCallback(window, fb_size_callback)
        glfwSetWindowCloseCallback(window, close_callback)









#=============================================

class SettingWindow(InputWindow):
    def set_title(self,value):
        glfwSetWindowTitle(self.window, value)
    def set_cursor_hide(self):
        glfwSetInputMode(self.window, GLFW_CURSOR, GLFW_CURSOR_HIDDEN)
    def set_cursor_lock(self):
        glfwSetInputMode(self.window, GLFW_CURSOR, GLFW_CURSOR_DISABLED)
    def set_cursor_normal(self):
        glfwSetInputMode(self.window, GLFW_CURSOR, GLFW_CURSOR_NORMAL)

    def __init__(self):
        super().__init__()        
        self._fullscreen = False
        self.windowed_size = self.size
    @property
    def fullscreen(self):
        return self._fullscreen
    @fullscreen.setter
    def fullscreen(self,value):    
        if value:
            self.windowed_size = self.size
            monitor = glfwGetPrimaryMonitor()
            mode = glfwGetVideoMode(monitor)
            mw,mh = mode.size
            fps = mode.refresh_rate
            glfwSetWindowMonitor(self.window, monitor, 0, 0, mw,mh, fps)
            self._fullscreen = True
        else:
            x,y = 100,100
            w,h = self.windowed_size
            glfwSetWindowMonitor(self.window, None,x,y,w,h,0)
            self._fullscreen = False

    #==========
    def glfw_hide(self):
        glfwHideWindow(self.window)
    def glfw_show(self):
        glfwShowWindow(self.window)
    def glfw_iconfy(self):
        glfwIconifyWindow(self.window)
    def glfw_maximize(self):
        glfwMaximizeWindow(self.window)
    def glfw_attention(self):
        glfwRequestWindowAttention(self.window)#blink.wow.
    def glfw_focus(self):#grab brutely. not wanted..
        glfwFocusWindow(self.window)#destructive.
    #===================================


class PropertyWindow(SettingWindow):
    """for size, mouse pos.."""
    #=============property .. all lower, toolongCapital rule. partial be like x,w
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
    def w(self):
        return glfwGetWindowSize(self.window)[0]
    @w.setter
    def w(self,w):
        h = glfwGetWindowSize(self.window)[1]
        glfwSetWindowSize(self.window, w,h)
    @property
    def h(self):
        return glfwGetWindowSize(self.window)[1]
    @h.setter
    def h(self,h):
        w = glfwGetWindowSize(self.window)[0]
        glfwSetWindowSize(self.window, w,h)    

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
        glfwSetWindowPos(self.window, x,height)#no callback
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
    def mpos(self):
        """mouse pos"""
        return glfwGetCursorPos(self.window)
    @mpos.setter
    def mpos(self,mpos):
        glfwSetCursorPos(self.window, mpos[0],mpos[1])
    @property
    def mx(self):
        """mouse x"""
        return glfwGetCursorPos(self.window)[0]
    @mx.setter
    def mx(self,cursor_posx):
        height = glfwGetCursorPos(self.window)[1]
        glfwSetCursorPos(self.window, cursor_posx,height)
    @property
    def my(self):
        return glfwGetCursorPos(self.window)[1]
    @my.setter
    def my(self,cursor_posy):
        width = glfwGetCursorPos(self.window)[0]
        glfwSetCursorPos(self.window, width,cursor_posy)

    #=============aspect and ..    
    @property
    def ratio(self):
        x,y = glfwGetWindowSize(self.window)
        return x/y
    @ratio.setter
    def ratio(self, value):
        if value==0:
            glfwSetWindowAspectRatio(self.window, GLFW_DONT_CARE, GLFW_DONT_CARE)
        else:
            x,y = glfwGetWindowSize(self.window)
            x = int(y*value)
            glfwSetWindowAspectRatio(self.window, x, y)
    
    @property#for fade effects kind.
    def opacity(self):
        return glfwGetWindowOpacity(self.window)
    @opacity.setter
    def opacity(self,opacity):
        glfwSetWindowOpacity(self.window, opacity)
    





class MultiWindow(PropertyWindow):
    """for multi window."""
    1

#=========================================


window_setting_dict = {

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
    },
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
        dd = window_setting_dict
        YAML.save(dd,fdir)
    return dd


def glfw_WindowHints(glfw_dict):
    for key,value in glfw_dict.items():
        #target = glfw_hint_namedict[key]
        target = globals()[key]                
        glfwWindowHint(target, int(value) )

def gl_Enables(gl_list):
    for attr in gl_list:
        glattr = globals()[attr]
        glEnable(glattr)
def gl_Disables(gl_list):
    for attr in gl_list:
        glattr = globals()[attr]
        glDisable(glattr)


#=========================================

class Window_es31:
    def __init__(self):
        """ifgles31shader':"#version 300 es \nprecision highp float;"""
        glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3)
        glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 1)
        glfwWindowHint(GLFW_OPENGL_FORWARD_COMPAT, 0)
        glfwWindowHint(GLFW_OPENGL_PROFILE, 0)
        glfwWindowHint(GLFW_CLIENT_API, GLFW_OPENGL_ES_API)#is it works?

        glfwWindowHint(GLFW_RESIZABLE, 0)
        glfwWindowHint(GLFW_DECORATED, 1)
        glfwWindowHint(GLFW_FOCUSED, 1)
        #glfwWindowHint(GLFW_FLOATING, 1)
        #glfwWindowHint(GLFW_MAXIMIZED, 0)
        glfwWindowHint(GLFW_CENTER_CURSOR, 1)
        #glfwWindowHint(GLFW_TRANSPARENT_FRAMEBUFFER, 1)
        glfwWindowHint(GLFW_SAMPLES, 4)
        glfwWindowHint(GLFW_DOUBLEBUFFER, 1)

        window = glfwCreateWindow(640, 480, 'es31 window', None, None)
        glfwMakeContextCurrent(window)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_MULTISAMPLE)
        
        glfwSwapInterval(0)
        glfwSetWindowSizeLimits(window, 100, 100, GLFW_DONT_CARE, GLFW_DONT_CARE)


        self.name = NAME.set(self)
        self.UUID = UUID.set(self)
        self.window = window

if __name__=='__main__':
    #window = Window_es31()
    a = MultiWindow()
    b = MultiWindow()
    a.set_title('window first')
    b.set_title('window 2nd')
    #a.bind_callback(IC)
    #b.bind_callback(IC)
    def ma():
        b.fullscreen = not b.fullscreen
    b.flipflop = ma
    b.keymap = {
        'F':b.flipflop,#need flip-flop function..
    }

    a.keymap={}
    IC.bind(a)
    IC.bind(b)
    #while not(a.should_close() or b.should_close()):
    #while BasicWindow.number>0:#really bad!
    #while a.window or b.window:#None if destroyed.
    while a.count:#a.count>0
        IC.cast()
        glfwPollEvents()
    #glfwTerminate()