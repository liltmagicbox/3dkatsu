from pyglet.gl import *
window = pyglet.window.Window()

from OpenGL.GL import *
from OpenGL.GL import shaders

#=====================================

#===============================
vertn = """
#version 410

layout (location = 0) in vec2 cord;
layout (location = 1) in vec2 uv;

out vec2 uvcord;

void main() 
{
    gl_Position = vec4(cord, 0,1);
    uvcord = uv;
}
"""

fragn = """
#version 410

in vec2 uvcord;

out vec4 outcolor;

uniform sampler2D tex1;


void main()
{
    //outcolor = vec4(uvcord,1,1 );
    outcolor = texture2D(tex1, uvcord);
}
"""


vshader = shaders.compileShader( vertn, GL_VERTEX_SHADER)
fshader = shaders.compileShader( fragn, GL_FRAGMENT_SHADER)
program = shaders.compileProgram( vshader,fshader)

#=============================================================
#pyglet.gl.glPointSize(10)

#v2f is vector 2 float, which has fixed input postion by pyglet. use 1g2f instead. [1th generic 2 of float]
#https://pyglet.readthedocs.io/en/latest/programming_guide/graphics.html#guide-graphics    
#vertex_list.colors[:3] = [255, 0, 0]
#'v2f/stream'

vert_list = pyglet.graphics.vertex_list(6,
        ('v2f', (0,0, 1,0, 1,1, 0,0, 0,1, 1,1, )),
        ('1g2f', (0,0, 1,0, 1,1, 0,0, 0,1, 1,1, ))
        )

pic = pyglet.image.load('image/9faces2.bmp')
tex = pic.get_texture()
#pic2 = pyglet.image.load('image/ft.bmp')
#tex2 = pic2.get_texture()


@window.event
def on_mouse_press(x, y, button, modifiers):
    global offset
    print(round(2*x/window.width),round(2*y/window.height))
    offset = (round(2*x/window.width),round(2*y/window.height))
    #offset = 4*x/window.width,4*y/window.height


from pyglet.window import key
@window.event
def on_key_press(symbol,modifiers):
    if symbol == key.NUM_1:
        1


@window.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT)
    glUseProgram(program)

    #cl = glGetUniformLocation(program, "colol")
    #glUniform3f(cl, 1.0, 0, 1.0)

    glEnable(GL_TEXTURE_2D)
    glBindTexture(tex.target, tex.id)#tex.target= created 'texture' in gpu

    vert_list.draw(pyglet.gl.GL_TRIANGLES)
    glDisable(tex.target)    
    
pyglet.app.run()
