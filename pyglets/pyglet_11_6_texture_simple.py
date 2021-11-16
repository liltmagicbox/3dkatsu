from pyglet.gl import *
window = pyglet.window.Window()

from OpenGL.GL import *
from OpenGL.GL import shaders

#=====================================
vertn = """
#version 410

layout (location = 0) in vec2 cord;
layout (location = 1) in vec2 uv;

out vec2 fragUV;

void main() 
{
    gl_Position = vec4(cord, 0,1);
    fragUV = uv;
    
}
"""
vert2n = """
#version 410

layout (location = 0) in vec2 cord;

out vec3 fragcol;

uniform sampler2d tex1;

void main() 
{
    gl_Position = vec4(cord, 0,1);
    vec4 textured =  texture(tex1, cord);
    fragcol = textured;
    
}
"""

fragn = """
#version 410
in vec2 fragUV;
out vec4 outcolor;

void main() 
{
    outcolor = vec4(fragUV, 0, 1);
}
"""


vshader = shaders.compileShader( vertn, GL_VERTEX_SHADER)
fshader = shaders.compileShader( fragn, GL_FRAGMENT_SHADER)
program = shaders.compileProgram( vshader,fshader)

#=============================================================
pyglet.gl.glPointSize(10)


@window.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT)

    glUseProgram(program)
    
    tex1 = glGetUniformLocation(program, "tex1")
    #glUniform3f(cl2, 0, 1.0,color)
    
    pyglet.graphics.draw(3, pyglet.gl.GL_TRIANGLES, ('v2f', (0,0, 1,0, 1,1)), ('1g2f', (0,0, 1,0, 1,1)) )

pyglet.app.run()
