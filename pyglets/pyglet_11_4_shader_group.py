#group. gltexture acts differently, so need it maybe.

from pyglet.gl import *
#https://pyglet.readthedocs.io/en/latest/programming_guide/graphics.html

from pyglet.graphics import vertex_list, vertex_list_indexed, Batch
#pyglet.graphics.vertex_list

from pyglet import image
pic = image.load('pic2.jpg')
texture = pic.get_texture()

window = pyglet.window.Window()


class CustomGroup(pyglet.graphics.Group):
    def set_state(self):
        glEnable(texture.target)
        glBindTexture(texture.target, texture.id)

    def unset_state(self):
        glDisable(texture.target)

g = CustomGroup()







#======================================================

#from OpenGL.GL import shaders, GL_VERTEX_SHADER, GL_FRAGMENT_SHADER
from OpenGL.GL import *
from OpenGL.GL import shaders

#pyglet.graphics.draw(3, pyglet.gl.GL_POINTS, ('v2f', (0,0, 0.5,0.5, 0.5,0) ),('1g3f', (0,0,1, 0,1,0, 1,0,0, )) )


vertn = """
#version 410
layout (location = 0) in vec2 cord;
layout (location = 1) in vec3 col;

out vec3 fragcol;

void main() 
{
    gl_Position = vec4(cord, 0,1);
    fragcol = col;
    
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



class ShaderGroups(pyglet.graphics.Group):
    def set_state(self):
        glUseProgram(program)

    def unset_state(self):
        glUseProgram(default)

gs = ShaderGroups()

b = Batch()
#count mode group (indices) data
b.add_indexed(4, GL_TRIANGLES, g,
    [0,1,2, 0,2,3],
    ('v2i', (0, 0, 50,0, 50,50, 0,50) ),
    #('c3B', (0, 0, 255, 0, 255, 0, 255,0,0, 255,255,0)),
    ('t2f', (0,0, 1,0, 1,1, 0,1)),
    )

# FOR attrib.change: vlist = b.add(3, GL_TRIANGLES, None,
b.add(3, GL_TRIANGLES, gs,
      ('v2i', (100,100,  150,100, 100,150) ),      
      ('c3B', (0, 0, 255, 0, 255, 0, 255,0,0, )),
       )

@window.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT)

    #draw() 1 required positional argument: 'mode'
    # GL_POINTS GL_LINE_STRIP GL_TRIANGLES

    b.draw()

pyglet.app.run()
