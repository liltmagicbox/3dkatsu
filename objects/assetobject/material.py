from shader import Shader
from texture import Texture
#from globject import VAO, Shader, Texture
#from assetobject import Mesh, Material, Skeleton, Skeleton_anim,
#from gameobject import Level, World, Controller, GUI

def set_namedict(namedict, name,item):
	if name in namedict:
		baridx = name.rfind('_')
		if baridx == -1:
			name = name+'_0'
			name,namedict = set_namedict(namedict,name,item)
		else:
			front = name[:baridx]
			back = name[baridx+1:]
			if back.isdecimal():#digit 3^3, numeric 3.3E06
				i = int(back)+1
				name = f"{front}_{i}"
				name,namedict = set_namedict(namedict,name,item)
			else:
				name = name+'_0'
				name,namedict = set_namedict(namedict,name,item)
	namedict[name] = item
	return name, namedict



def get_namekey(namedict, name):
	if name in namedict:
		baridx = name.rfind('_')
		if baridx == -1:
			name = name+'_0'
			name = get_namekey(namedict,name)
		else:
			front = name[:baridx]
			back = name[baridx+1:]
			if back.isdecimal():#digit 3^3, numeric 3.3E06
				i = int(back)+1
				name = f"{front}_{i}"
				name = get_namekey(namedict,name)
			else:
				name = name+'_0'
				name = get_namekey(namedict,name)
	return name

namedict = {}
name = 'first_0'
item = 'ham'
name = get_namekey(namedict, name)
namedict[name]=item
print(name,'na')

name = 'first'
name = get_namekey(namedict, name)
namedict[name]=item
print(name,'na')

name = 'first'
name = get_namekey(namedict, name)
namedict[name]=item
print(name,'na')

class Material:
	namedict = {}
	@classmethod
	def get(cls, name):
		return cls.namedict.get(name)
		#return cls.namedict.get(name, 'default') this prevents if none, load Factor.
	@classmethod
	def set(cls, name: str, item) -> str:
		name = get_namekey(cls.namedict,name)
		cls.namedict[name]=item
		return name

	def __repr__(self):
		name = self.name
		shader = self.shader
		inputs = self.inputs
		return f"Material name:{name}, sha:{shader}, inputs:{inputs}"
	
	def __init__(self, texture = None, name='Mat', shader='default', **kwargs):
		"""default shader not bsdf but a texture
		input texture only can be Texture.
		shader is name, not Shader."""
		name = Material.set(name,self) # name->name_0 name_0->name_1
		self.name = name

		if isinstance(shader, str):
			shader = Shader.get(shader)
		self.shader = shader
		
		inputs = {}
		for key, value in kwargs.items():# str or Texture seems texture. or, value.
			if isinstance(value, str):
				value = Texture.get(value)
				#key= key+'Texture'
			elif isinstance(value, Texture):
				pass
				#key= key+'Texture'
			elif isinstance(value, (list,tuple) ):#hopefully vec3
				value = list(value)
				#key= key+'Factor'
			elif isinstance(value, (int,float) ):
				value = float(value)
				#key= key+'Factor'
			inputs[key] = value

		self.inputs = inputs
		#----for fast single texture material
		if texture:
			if isinstance(texture, str):
				texture = Texture.get(texture)
			self.inputs = {"color":texture}
		

	#def copy(self):
	def from_json(self, jsonpath):#too complexed.
		shadername = material_dict['shader']
		shader = Shader.load('shadername')#fs,vs..?
	def from_dict(self, material_dict):
		shadername = material_dict['shader']
		shader = Shader.get('shadername')
		self.shader = shader		
		textures = material_dict['texture']
		for channel , texname in textures.items():
			texture = Texture.get(texname)
			self.textures[channel] = texture

	def bind(self):
		shader = self.shader
		shader.bind()
		inputs = self.inputs
		for i, key in enumerate(inputs):
			# 'Texture' in key
			value = inputs[key]
			if isinstance(value, Texture):
				shader.set_int(key,i)
				texture = value
				texture.bind(i)
			#else:#seems factor
			elif isinstance(value, float):
				shader.set_float(key,value)
			elif isinstance(value, list):
				#shader.set_vec3(key,value)
				x,y,z = value
				shader.set_vec3(key, x,y,z)


mat=Material(name='default')
print(mat)

mat=Material()
print(mat)

mat=Material( texture=checker) #we can not trace thisway.
mat=Material( texture='checker')#this is the way!
mat=Material('checker')
print(mat)
mat=Material(name='home')
print(mat)
mat=Material()
print(mat)
mat=Material()
print(mat)
mat=Material()
print(mat)

mat=Material(name='home',shader='bsdf', color=[1,0,0], metallic=1.0, normal='max')
print(mat)
print('-0----')