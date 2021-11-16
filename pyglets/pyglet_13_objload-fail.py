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
        ('v2f', (0,0, 1,0, 1,1, 0,0, 0,1, 1,1)),
        ('1g2f', (0,0, 1,0, 1,1, 0,0, 0,1, 1,1))
        )

pic = pyglet.image.load('image/eyebrow.png')
tex = pic.get_texture()
#pic2 = pyglet.image.load('image/ft.bmp')
#tex2 = pic2.get_texture()


#pic2 = pyglet.image.load('image/yum.png')
#tex2 = pic2.get_texture()


import pywavefront
from pywavefront import visualization

obj = pywavefront.Wavefront('objs/warhawk2.obj')
obj.parse()
print(dir(obj))
print(obj.vertices)
print(obj.materials)
print(obj.mtllibs)
print(obj.meshes)
for name,mat in obj.materials.items():
    print(name,mat,'no')
    print(obj.vertex_format)
    #print(obj.vertices)
    #print(obj.texture)
input('ham')
@window.event
def on_draw():
    visualization.draw(obj)
    # glClear(GL_COLOR_BUFFER_BIT)
    # glUseProgram(program)

    # #cl = glGetUniformLocation(program, "colol")
    # #glUniform3f(cl, 1.0, 0, 1.0)
    # size = glGetUniformLocation(program, "size")
    # glUniform2f(size, 1.0,0.0625)
    # off = glGetUniformLocation(program, "offset")
    # glUniform2f(off, offset[0],offset[1])
    
    

    # glEnable(GL_TEXTURE_2D)
    # #glBindTexture(tex.target, tex.id)
    # glBindTexture(tex.target, tex.id)#tex.target= created 'texture' in gpu
    
    # #cl = glGetUniformLocation(program, "tex1")    
    # #cl = glGetUniformLocation(program, "tex1")
    # #glUniform1i(glGetUniformLocation(tex.id, "tex1"), 0)
    # #glUniform1i(cl,0)
    
    # vert_list.draw(pyglet.gl.GL_TRIANGLES)
    # glDisable(tex.target)    
    
pyglet.app.run()
