from general import timef, Plotter
from glfw.GLFW import *

tt = timef()
lower=5
def key_callback(window, key, scancode, action, mods):
	global tt, lower
	t = timef()
	dt = t-tt
	#print(dt)
	tt = t
	lower = min(lower ,dt)
	print(lower)


0.02102389999999943
0.9192301999999977
0.025007300000005728
0.00017159999999449838
0.02971610000000169

#multi finger
0.00011360000000060211
4.779999999993123e-05
4.880000000007101e-05
3.96000000000285e-05
0.013023899999999422

#1 finger 10 or 6ms is fastest.

#0.1ms
#4.880000000007101e-05
#0.00004
#0.04ms!

glfwInit()
window = glfwCreateWindow(640, 480, 'a window', None, None)
glfwSetKeyCallback(window, key_callback)

import time
while True:
	glfwPollEvents()
	1

# X = []
# Y = []
# st=timef()
# for i in range(1000000000000):
# 	t=timef()-st
# 	X.append(t)
# 	Y.append(state)
# 	if t>1:
# 		print(t)
# 		break

# p = Plotter()

# p.plot(X,Y)
# p.show()



