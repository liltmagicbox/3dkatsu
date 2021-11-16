from pyglet.gl import *
#https://pyglet.readthedocs.io/en/latest/programming_guide/graphics.html

from pyglet.graphics import vertex_list, vertex_list_indexed
#pyglet.graphics.vertex_list


from OpenGL.GL import *
from OpenGL.GL import shaders
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
#================================================================
vshader = shaders.compileShader( vertn, GL_VERTEX_SHADER)
fshader = shaders.compileShader( fragn, GL_FRAGMENT_SHADER)
program = shaders.compileProgram( vshader,fshader)
#glUseProgram(program) not here, SO strange!


window = pyglet.window.Window()


pic = pyglet.image.load('objs/cubemap/cubemap.png')
texture = pic.get_texture()
#glEnable(GL_TEXTURE_2D)
#glBindTexture(texture.target, texture.id)


from fastestobjread import OBJ

obj = OBJ('objs/cubemap/cubemap.obj')
#obj.multices

#--------------------------mesh data
faces = [1,3,2, 0,1,2]
vertex_count = 4
vertex_coordinate = (0,0, 1,0, 1,1, 0,1)
vertex_uv = (0,0, 1,0, 1,1, 0,1)
#--------------------------mesh data
faces = obj.idxs

vertex_count = len(obj.multices)
vertex_coordinate = []
vertex_uv = []

for multex in obj.multices:
    vert = multex[0]
    uv = multex[1]
    vertex_coordinate.extend(vert)
    vertex_uv.extend(uv)
nv = []
for cord in vertex_coordinate:
    nv.append(cord/0.5)
vertex_coordinate = nv

pyglet.gl.glPointSize(10)
#https://pyglet.readthedocs.io/en/latest/programming_guide/graphics.html#guide-graphics    
vertex_list_indexed1 = vertex_list_indexed(vertex_count,
    faces,
    #('v2f', vertex_coordinate ),
    ('0g3f', vertex_coordinate ),
    ('1g2f', vertex_uv),#1t2f strange, but not working! and also 1 works while 0,2 not.
    )

@window.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT)
    glUseProgram(program)

    vertex_list_indexed1.draw(GL_TRIANGLES)
    #vertex_list_indexed1.draw(GL_LINE_STRIP)
    #vertex_list_indexed1.draw(GL_POINTS)

pyglet.app.run()
