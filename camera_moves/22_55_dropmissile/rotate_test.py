from matplotlib import pyplot as plt
#x = range(10) #~10, [0,1,2,3,4,5,6,7,8,9]
#y = [i*i for i in x]

import numpy as np

p1 = 1,0, '#000000'

#------------z roatee
deg = 30
point_z = np.cos(np.radians(deg)), np.sin(np.radians(deg)), '#0000ff' #x,y,color
#print('rot z', np.cos(np.radians(deg)))
print('z', point_z)
#----------- rotate via x axis
deg = 60
point_x = point_z[0], point_z[1]*np.cos(np.radians(deg)), '#ff0000' #x,y,color
#----------- rotate via Y axis
deg = 60
point_y = point_z[0]*np.cos(np.radians(deg)), point_x[1], '#00ff00' #x,y,color
# y axis formula has error! see 3d.



points = [p1, point_z, point_x, point_y]
lines = points

for line in lines:
	x,y = [],[]
	x.append(0)
	y.append(0)
	x.append(line[0])
	y.append(line[1])
	color = line[2]
	plt.plot(x,y, '-*', color= color)
plt.axis( (0,1.2, 0,1.2))
plt.show()







#3D==----============================

def cos(deg):
	return np.cos(np.radians(deg))
def sin(deg):
	return np.sin(np.radians(deg))


print('3D')
p1 = 1,0,0, '#000000'

#------------z roatee
deg = 30
#point_z = np.cos(np.radians(deg)), np.sin(np.radians(deg)), 0, '#0000ff' #x,y,color #old
previous_point = p1
px,py,pz = previous_point[0],previous_point[1] , previous_point[2]
#remained z value.
nx = px*cos(deg)-py*sin(deg)
ny = px*sin(deg)+py*cos(deg)
nz = pz
point_z = nx, ny, nz, '#0000ff' #x,y,color #new c-sin

#print('rot z', cos(deg))
print('point_z', point_z)
print('len', np.sqrt( point_z[0]**2+point_z[1]**2+point_z[2]**2) )

#----------- rotate via x axis
deg = 60
previous_point = point_z
px,py,pz = previous_point[0],previous_point[1] , previous_point[2]
#remained y value.
#nx = py*cos(deg)-pz*sin(deg)
#ny = py*sin(deg)+py*cos(deg)
#nz = py*cos(deg)-pz*sin(deg)
#---donno why but it's ok.
nx = px
ny = py*cos(deg)
nz = py*sin(deg)
point_x = nx,ny,nz,   '#ff0000' #x,y,color

print('point_x', point_x)
print('len', np.sqrt( point_x[0]**2+point_x[1]**2+point_x[2]**2) )

#----------- rotate via Y axis
deg = 60
previous_point = point_x
px,py,pz = previous_point[0],previous_point[1] , previous_point[2]
#remained y value.
#nx = px*cos(deg)+pz*sin(deg)
#ny = px*sin(deg)-pz*cos(deg)
#nz = pz*sin(deg)
nx = px*cos(deg) - pz*sin(deg)
nz = px*sin(deg) + pz*cos(deg)
ny = py

point_y = nx,ny,nz,   '#00ff00' #x,y,color
#point_y = point_z[0]*cos(deg),  point_x[1],   point_x[2]*sin(deg),   '#00ff00' #x,y,color
print('point_x', point_y)
print('len', np.sqrt( point_y[0]**2+point_y[1]**2+point_y[2]**2) )





points = [p1, point_z, point_x, point_y]
lines = points



fig = plt.figure()
ax = fig.add_subplot(projection='3d')

for i, line in enumerate(lines):
	x,y,z = [],[],[]
	x.append(0)
	y.append(0)
	z.append(0)
	x.append(line[0])
	y.append(line[1])
	z.append(line[2])
	color = line[3]
	#plt.plot(x,y, '-*', color= color)
	#ax.plot(x, y, z, label='parametric curve')
		
	ax.plot(x, y, z, '-*', color = color)
#ax.legend()
#plt.axis( (0,1.2, 0,1.2, ))
ax.set_xlim3d(0, 1.2)
ax.set_ylim3d(0, 1.2)
ax.set_zlim3d(0, 1.2)
ax.set_xlabel('$X$')
ax.set_ylabel('$Y$')
ax.set_zlabel('$Z$')
plt.show()




fig = plt.figure()
ax = fig.add_subplot(projection='3d')

for i, line in enumerate(lines):
	x,y,z = [],[],[]
	x.append(0)
	y.append(0)
	z.append(0)
	x.append(line[0])
	y.append(line[1])
	z.append(line[2])
	
	#---- for trace
	if i>0:
		x.append(lines[i-1][0])
		y.append(lines[i-1][1])
		z.append(lines[i-1][2])

	color = line[3]
	#plt.plot(x,y, '-*', color= color)
	#ax.plot(x, y, z, label='parametric curve')
		
	ax.plot(x, y, z, '-*', color = color)
#ax.legend()
#plt.axis( (0,1.2, 0,1.2, ))
ax.set_xlim3d(0, 1.2)
ax.set_ylim3d(0, 1.2)
ax.set_zlim3d(0, 1.2)

plt.show()

