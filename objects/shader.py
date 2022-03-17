from OpenGL.GL import *
from OpenGL.GL import shaders

import pyglet

vertn = """
#version 410 core

layout (location = 0) in vec3 pos;
layout (location = 1) in vec2 uv;

out vec2 uvcord;

//gl_VertexID
//uniform int idx;
//uniform mat4 Model[252]; //253 max.. why not 255? 250 to remember easy
uniform mat4 Model;
uniform mat4 View;
uniform mat4 Projection;

void main() 
{
    //gl_Position = Projection * View * Model[gl_InstanceID] * vec4(pos,1);
    //gl_Position = Projection * View * Model * vec4(pos * ,1);
    gl_Position = Projection * View * Model * vec4(pos, 1);
    uvcord = uv;
}
"""

fragn = """
#version 410 core

in vec2 uvcord;

out vec4 outcolor;

uniform sampler2D color;
//uniform sampler2D tex1;

void main()
{
    outcolor = texture2D(color, uvcord);
    //outcolor = vec4(uvcord,1,1 );
    //outcolor = mix(texture(tex0, uvcord), texture(tex1, uvcord), 0.4);
}
"""

from common import get_namekey

# class Car:
#     i=0
#     def __init__(self):
#         print('carrr')
#         self.__class__.i+=1
#     def pp(self):
#         print(self.__class__)
#         print(self.__class__.i)

# c=Car()
# c.pp()


class Shader:
    last = -1

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
       cls(vertn,fragn,name='default')

    def __init__(self, vertstr, fragstr, name='shader'):
        assert bool(glCreateShader)#sometimes compile error occurs, before window() 
        vshader = shaders.compileShader( vertn, GL_VERTEX_SHADER)
        fshader = shaders.compileShader( fragn, GL_FRAGMENT_SHADER)
        program = shaders.compileProgram( vshader,fshader)
        glDeleteShader(vshader)
        glDeleteShader(fshader)
        self.ID= program

        self.loc={}
        
        name = self.__class__.set(name,self)
        self.name = name

    def __repr__(self):
        return f"Shader name:{self.name}"    

    def bind(self):
        #shader has own input dict,
        #if bind, reset all values, specially texture = -1.
        #if texture -1, try to load Factor, 0.5 or [0.5,0.5,0.5], or really 0.5, finally.
        cls = self.__class__
        if cls.last != self.ID:
            glUseProgram(self.ID)
            cls.last = self.ID
    def unbind(self):
        glUseProgram(0)
        cls = self.__class__
        cls.last = -1#not forget it!

    def get_loc(self, uniform_name):
        loc = self.loc.get(uniform_name)
        if not loc:
            program = self.ID
            loc = glGetUniformLocation(program, uniform_name)
            self.loc[uniform_name] = loc
        return loc

    def set_int(self, uniform_name, value):
        loc = self.get_loc(uniform_name)
        glUniform1i(loc,value)
    def set_float(self, uniform_name, value):
        loc = self.get_loc(uniform_name)
        glUniform1f(loc,value)
    def set_vec3(self, uniform_name, x,y,z):
        loc = self.get_loc(uniform_name)
        glUniform3f(loc, x,y,z)
        # if (len(args) == 1 and type(args[0]) == glm.vec3):
        #     glUniform3fv(glGetUniformLocation(self.ID, name), 1, glm.value_ptr(args[0]))
        # elif (len(args) == 3 and all(map(lambda x: type(x) == float, args))):
        #     glUniform3f(glGetUniformLocation(self.ID, name), *args)        
    def set_mat4(self, uniform_name, mat):
        """we need bind the shader first!"""
        loc = self.get_loc(uniform_name)
        glUniformMatrix4fv(loc,1,False, mat)# True for row major.ha.[1,2,3,4, ,]
        #glUniformMatrix4fv(loc, 1, GL_FALSE, glm.value_ptr(mat))
        #location count transpose data


if __name__ == "__main__":
    window = pyglet.window.Window()
    s = Shader(vertn,fragn)    
    print(s)
