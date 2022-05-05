from glfw.GLFW import *
from OpenGL.GL import *

glfwInit()
window = glfwCreateWindow(640, 480, 'a window', None, None)
glfwMakeContextCurrent(window)

x = glfwGetWindowAttrib(window, GLFW_TRANSPARENT_FRAMEBUFFER)
print(x)

class Man:
    def __init__(self):
        age=5
        self.window = glfwCreateWindow(640, 480, 'a window', None, None)
    @property
    def x(self):
        return glfwGetWindowPos(self.window)[0]
    @x.setter
    def x(self,x):
        height = glfwGetWindowPos(self.window)[1]
        glfwSetWindowPos(self.window, x,height)

a=Man()
print(dir(a))

print(a.x)
a.x+=5
print(a.x)
#138
#143
#works!