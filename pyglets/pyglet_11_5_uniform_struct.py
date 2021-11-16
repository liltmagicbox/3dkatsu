from pyglet.gl import *
window = pyglet.window.Window()




#======================================================

#from OpenGL.GL import shaders, GL_VERTEX_SHADER, GL_FRAGMENT_SHADER
from OpenGL.GL import *
from OpenGL.GL import shaders

#OpenGL.GL.shaders.glUniform2f
#OpenGL.GL.shaders.glVertexAttrib2fv
#OpenGL.GL.shaders.glGetShaderSource
#kinds.fine.

#===================================
#new shader, with attrb. note: vertex cord automatically location0.  1g3f atleast. not 0g3f.

#pyglet.graphics.draw(3, pyglet.gl.GL_POINTS, ('v2f', (0,0, 0.5,0.5, 0.5,0) ),('1g3f', (0,0,1, 0,1,0, 1,0,0, )) )

vertn = """
#version 410
layout (location = 0) in vec2 cord;
layout (location = 1) in vec3 col;

out vec3 fragcol;

//uniform vec3 color;
//uniform vec3 color2;

//---------------struct.
struct sStruct
{
 int foo;
 int bar;
};
uniform sStruct uniarray;

//layout (location = 2) uniform vec3 color; not working!
//layout (location = 4) uniform vec3 color2;
//layout (location = 8) uniform vec3 co;

void main() 
{
    gl_Position = vec4(cord, 0,1);
    //fragcol = (color+color2)/2;
    //fragcol = vec3(uniarray[0], 0.0,0.0);
    fragcol = vec3(uniarray.foo, 0.0,0.0);
    
}
"""

fragn = """
#version 410
in vec3 fragcol;
out vec4 outcolor;

void main() 
{
    outcolor = vec4(fragcol, 1);
}
"""


vshader = shaders.compileShader( vertn, GL_VERTEX_SHADER)
fshader = shaders.compileShader( fragn, GL_FRAGMENT_SHADER)
program = shaders.compileProgram( vshader,fshader)

#https://heinleinsgame.tistory.com/8


#>>> glGetUniformLocation(program, "color2") -1 however.

#https://www.khronos.org/opengl/wiki/Uniform_(GLSL)
#https://www.khronos.org/opengl/wiki/Interface_Block_(GLSL)
#explains struct use.

#https://stackoverflow.com/questions/56883308/glgetuniformlocation-returns-1-even-though-i-used-the-variable-in-shader
#See OpenGL 4.6 Core Profile Specification - 7.3.1 Program Interfaces, page 102:
# ...no observable effect ... compiler or linker cannot make a conclusive determination

#i set uniform color, but no use, so no location.  it's active only I use it!

#https://stackoverflow.com/questions/64199067/glgetuniformlocation-returns-1-for-an-array-of-struct-in-glsl
#Uniform Buffer Object?? too bad, but we may go so. better send every var.

#=============================================================
pyglet.gl.glPointSize(10)

from pyglet import clock

color = 1
@window.event
def on_mouse_press(x, y, button, modifiers):
    global color
    color = x/window.width

@window.event
def on_draw():
    global color
    glClear(GL_COLOR_BUFFER_BIT)
    #GL_TRIANGLES GL_POINTS... / v2f means vector 2, float. v3i vector int 3. kinds.
    glUseProgram(program)

    #cl = glGetUniformLocation(program, "color")
    #glUniform3f(cl, color, 0, 1.0)
    #cl2 = glGetUniformLocation(program, "color2")
    #print(cl,cl2)

    #ar = glGetUniformLocation(program, "uniarray[0]")    
    #glUniform3f(ar, 0, color, 1.0)    
    #found glGetUniform

    ar = glGetUniformLocation(program, "uniarray[55]")
    glUniform3f(ar, 0, color, 1.0)    
    
    pyglet.graphics.draw(3, pyglet.gl.GL_POINTS, ('v2f', (0,0, 0.5,0.5, 0.5,0) ),('1g3f', (0,0,1, 0,1,0, 1,0,0, )) )
    pyglet.graphics.draw(3, pyglet.gl.GL_POINTS, ('v2f', (-0.5,0, -0.5,-0.5, 0.5,0) ),('1g3f', (0,0,1, 0,1,0, 1,0,0, )) )

pyglet.app.run()
