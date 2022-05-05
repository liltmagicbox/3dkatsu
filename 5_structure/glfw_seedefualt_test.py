from glfw.GLFW import *
from OpenGL.GL import *
import time

glfwInit()
window = glfwCreateWindow(640, 480, 'a window', None, None)
glfwMakeContextCurrent(window)
monitor = glfwGetWindowMonitor(window)
#glfwSetWindowMonitor(window, None, 100, 100, 400, 400, 0)
#mode = glfwGetVideoMode(monitor)
#monitor = glfwGetPrimaryMonitor()

x = glfwGetWindowAttrib(window, GLFW_TRANSPARENT_FRAMEBUFFER)
print(x)

def seeframebuffer_different():
	b = glfwGetFramebufferSize (window)#(640, 480)
	print(b)

	#glfwSetWindowContentScaleCallback
	print(glfwGetWindowContentScale(window))#dpi_now vs dpi_default 1.01.0
	#https://www.glfw.org/docs/3.3/window_guide.html#GLFW_SCALE_TO_MONITOR
	#notthathelpful..

def full_scr_and_return_back():
	#monitor = glfwGetWindowMonitor(window)#errs.why??
	mode = glfwGetVideoMode(monitor)
	#mode = glfwGetVideoMode(monitor)
	width,height = mode.size
	ref = mode.refresh_rate
	#glfwSetWindowMonitor(window, None, 0, 0, 300,300, 60)

	glfwSetWindowMonitor(window, monitor, 0, 0, width,height, ref)
	
	time.sleep(5)
	glfwSetWindowMonitor(window, None, 100, 100, 400, 400, 0)
	time.sleep(5)
#exit()

#x = glfwGetWindowAttrib(window, GL_MULTISAMPLE)

#https://www.khronos.org/registry/OpenGL-Refpages/gl4/html/glEnable.xhtml
#glIsEnabled or glGet

#2 only True.
#GL_DITHER,
#GL_MULTISAMPLE,

glcaps = [
GL_BLEND,
#GL_CLIP_DISTANCE,
GL_DEPTH_TEST,
GL_DITHER,
GL_MULTISAMPLE,
GL_FRAMEBUFFER_SRGB,
GL_CULL_FACE,

#GL_FOG,
#GL_LIGHTING,
GL_POINT_SMOOTH,
GL_LINE_SMOOTH,
#GL_LINE_STIPPLE,
GL_POLYGON_SMOOTH,
GL_SCISSOR_TEST,# discard frag of outside scissor rect. good of monocular view..
GL_STENCIL_TEST,#, do stencil testing and update the stencil buffer.
GL_TEXTURE_CUBE_MAP

]

#https://www.glfw.org/docs/3.3/input_guide.html#input_key
#key_name = glfwGetKeyName(GLFW_KEY_W, 0)
#print(key_name)#w

for i in glcaps:	
	x = glIsEnabled(i)
	#y = glGet(i)
	print(x, i)

window2 = glfwCreateWindow(640, 480, 'a window', None, None)
glfwMakeContextCurrent(window2)
glDisable(GL_MULTISAMPLE)
x = glIsEnabled(GL_MULTISAMPLE)
print(x)
glEnable(GL_BLEND)
x = glIsEnabled(GL_BLEND)
x = glIsEnabled(GL_BLEND)
print(x)

glfwMakeContextCurrent(window)
x = glIsEnabled(GL_MULTISAMPLE)
print(x)

from PIL import Image
fdir = 'favicon.ico'
img = Image.open(fdir)
glfwSetWindowIcon(window, 1, img)

from general import timef
tt=timef()
for i in range(1000):
	glfwMakeContextCurrent(window)#40ms
	#glClearColor(1,0,0,0)#4ms
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)#4.6ms
	w = glfwGetCurrentContext()
	print(w,'1')
	#glClear(GL_COLOR_BUFFER_BIT)#4.3ms.
	#glPointSize(10)
	#glIsEnabled(GL_MULTISAMPLE)#4ms
	#glfwWindowShouldClose(window)#1ms
	#glfwMakeContextCurrent(window2)
	glfwWindowShouldClose(window2)
	w = glfwGetCurrentContext()
	print(w,'2')
	#glIsEnabled(GL_MULTISAMPLE)
print( timef()-tt )
#0.08944470000000004
#90ms for 2000 times of current context.
#5ms for enabled check

#78 82 90

#====================result
#80ms for 1000times swap(2000 total)
#40ms for 1000
#..x10 slow!
#if window 25.. 1ms takes.
#0.1ms for 2 windows. quite heavy.
#..actually we not divide 2.

#check closed: or glEnable kinds:
#5ms fo 1000 times.

#ow(640, 480, 'a window', None, window) not working!

