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
#vertex_list.colors[:3] = [255, 0, 0]
#'v2f/stream'
vert_list = pyglet.graphics.vertex_list(3,
        ('v2f', (0,0, 1,0, 1,1)),
        ('1g2f', (0,0, 1,0, 1,1))
        )
#v2f is vector 2 float, which has fixed input postion by pyglet. use 1g2f instead. [1th generic 2 of float]
#https://pyglet.readthedocs.io/en/latest/programming_guide/graphics.html#guide-graphics    
@window.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT)
    glUseProgram(program)

    vert_list.draw(pyglet.gl.GL_TRIANGLES)
    
pyglet.app.run()