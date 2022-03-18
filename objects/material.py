from shader import Shader
from texture import Texture
#from globject import VAO, Shader, Texture
#from assetobject import Mesh, Material, Skeleton, Skeleton_anim,
#from gameobject import Level, World, Controller, GUI

import pyglet

from common import get_namekey

class Material:
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
       cls('default')#texture, override.

    def __repr__(self):
        name = self.name        
        shader = self.shader
        inputs = self.inputs
        return f"Material name:{name}, sha:{shader}, inputs:{inputs}"
    def __init__(self, texture = None, name='material', shader='default', **kwargs):
        """default shader not bsdf but a texture
        input texture only can be Texture.
        shader is name, not Shader."""

        #----for fast single texture material override
        #assume we use: m = Material('texname')

        if texture:
            if isinstance(texture, Texture):
                texture = texture.name
            name = texture
            name = self.__class__.set(name,self) # name->name_0 name_0->name_1
            self.name = name
            self.shader = shader
            self.inputs = {"color":texture}
            return#cut here. class init return None fine.


        name = self.__class__.set(name,self) # name->name_0 name_0->name_1
        self.name = name

        #shader = Shader.get(shader)
        self.shader = shader
        
        inputs = {}
        for key, value in kwargs.items():# str or Texture seems texture. or, value.
            if isinstance(value, str):
                key= key+'Texture'
            elif isinstance(value, (list,tuple) ):#hopefully vec3
                value = list(value)
                #key= key+'Factor'
            elif isinstance(value, (int,float) ):
                value = float(value)
                #key= key+'Factor'
            inputs[key] = value

        self.inputs = inputs

	#def copy(self):
    def xxfrom_json(self, jsonpath):#too complexed.
	    shadername = material_dict['shader']
	    shader = Shader.load('shadername')#fs,vs..?
    def xxfrom_dict(self, material_dict):
	    shadername = material_dict['shader']
	    shader = Shader.get('shadername')
	    self.shader = shader		
	    textures = material_dict['texture']
	    for channel , texname in textures.items():
            texture = Texture.get(texname)
            self.textures[channel] = texture

    def bind(self, M,V,P):
        """gl objects stored as name
        texture: ofname(str)
        float: float
        vec3: [x,y,z]. not nparray. for json save.
        """
        shader = Shader.get(self.shader)        
        shader.bind()
        shader.set_mat4('Projection',P)
        shader.set_mat4('View',V)
        shader.set_mat4('Model',M)

        inputs = self.inputs
        unit=-1
        for key, value in inputs.items():
            #if isinstance(value, Texture):
            if 'Texture' in key:
                unit+=1
                shader.set_int(key,unit)
                texture = Texture.get(value)
                texture.bind(unit)
                print(unit,value)
            #else:#seems factor
            elif isinstance(value, float):
                shader.set_float(key,value)
            elif isinstance(value, list):
                #shader.set_vec3(key,value)
                x,y,z = value
                shader.set_vec3(key, x,y,z)# the only way, or we need ndarray..                


mat=Material(name='default')
print(mat)

mat=Material()
print(mat)



#mat=Material( texture=checker) #we can not trace thisway.
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
mat=Material(name='home', color='default')
mat=Material(name='home', color=[1,0,0], metallic=1.0, normal='default', shine='default')
print(mat)
print('-0----')

#maybe, if tex load fail, we can get default. prevents err-stop.

if __name__ == "__main__":
    window = pyglet.window.Window()
    print(Shader.namedict)
    print(Texture.namedict)
    #mat.bind(m,v,p)
    print(Shader.namedict)
    print(Texture.namedict)
    
    a = Material.get('default')
    print(a,'get')
