from common import get_namekey
from material import Material
from shader import Shader
from texture import Texture
from vao import VAO
import numpy as np
import pyglet

from OpenGL.GL import *

#Mesh([0,0,0, 1,0,0, 0,1,0, 1,1,0], indices = [0,1,2, 1,2,3])
#Mesh([0,0,0, 1,0,0, 0,1,0], material = m)
#Mesh([0,0,0, 1,0,0, 0,1,0], material = Material('tex1') )

class Mesh:
	""" python object for internal usage ..and little to glTF"""

	#---namedict ver 0.2
	namedict = {}
	@classmethod
	def get(cls, name):
		if not 'default' in cls.namedict:            
			cls.default()
		return cls.namedict.get(name)
	@classmethod
	def set(cls, name: str, item) -> str:
		name = get_namekey(cls.namedict,name)
		cls.namedict[name]=item
		return name
	@classmethod
	def default(cls):
		cls([0,0,0, 1,0,0, 0,1,0],name='default')

	def __repr__(self):
		return f"mesh name:{self.name}, mat:{self.material}"
	def __init__(self, position, indices=None, material='default', name='mesh', **kwargs):		
		cls = self.__class__

		attributes = {}#position normal uv.. position only has priority		
		attributes['position'] = position
		for key, value in kwargs.items():
			attributes[key] = value
		
		if not indices:
			count = len(position)//3
			indices = list( range(count) )

		self.attributes = attributes
		self.indices = indices
		self.material = material

		#vao input nparr attrs{}, indices.
		#and VAO returns name, store it and when bind, VAO.get(name).
		vao_attrs = {}
		for key, value in attributes.items():
			vao_attrs[key] = np.array(value).astype('float32')#assume value [] or npfloat32 already.
		vao_indices = np.array(indices).astype('uint')
		self.VAO = VAO(vao_attrs,vao_indices).name#not like texture,shader, it created here, when init.		

		name = cls.set(name,self)
		self.name = name

	def bind(self):1
	def draw(self):
		#mat = Material.get(self.material)
		#mat.bind(m,v,p)		
		vao = VAO.get(self.VAO)
		vao.bind()
		vao.draw()
		
	@classmethod
	def from_dict(cls, mesh_dict):
		1
	def to_dict(self):
		1

# window = pyglet.window.Window()

# @window.event
# def on_draw():
#     gldraw()

# #@profile
# def gldraw():
#     #glClear(GL_COLOR_BUFFER_BIT)
#     glClearColor(0.0, 0.24, 0.5, 1.0)
#     glClear(GL_COLOR_BUFFER_BIT|GL_DEPTH_BUFFER_BIT)

if __name__ == "__main__":
    
    print(Shader.namedict)
    print(Texture.namedict)
    #mat.bind()    
    print(Shader.namedict)
    print(Texture.namedict)
    m = Mesh([0,0,0, 1,0,0, 0,1,0], material = Material('tex2') )
    print(m)
    
    a = Material.get('default')
    print(a,'get')

    m = Mesh([0,0,0, 1,0,0, 0,1,0] )
    mm = np.array([1,0,0,0, 0,1,0,0, 0,0,1,0, 0,0,0,1]).astype('float32')
    vm = mm
    pm = mm
    m.draw(mm,vm,pm)

    pyglet.app.run()