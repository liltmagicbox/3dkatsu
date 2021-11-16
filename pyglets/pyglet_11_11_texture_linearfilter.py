from pyglet.gl import *
window = pyglet.window.Window()

from OpenGL.GL import *
from OpenGL.GL import shaders

#=====================================
#glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
#occurs bad act, donno why. anyway not use it!

#===============================
vertn = """
#version 410

layout (location = 0) in vec3 cord;
layout (location = 1) in vec2 uv;

out vec2 uvcord;

void main() 
{
    gl_Position = vec4(cord,1);
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
    //if (outcolor.a ==0.3) discard;
    if (outcolor.a ==0) outcolor.a = 0.1;
    
    //outcolor = vec4(outcolor.r*outcolor.a, outcolor.g*outcolor.a, outcolor.b*outcolor.a, outcolor.a);
}
"""


vshader = shaders.compileShader( vertn, GL_VERTEX_SHADER)
fshader = shaders.compileShader( fragn, GL_FRAGMENT_SHADER)
program = shaders.compileProgram( vshader,fshader)

#=============================================================
#vertex_list.colors[:3] = [255, 0, 0]
#'v2f/stream'
vert_list = pyglet.graphics.vertex_list(6,
        ('v3f', (0,0,0, 1,0,0, 1,1,0, 0,0,0, 0,1,0, 1,1,0)),
        ('1g2f', (0,0, 1,0, 1,1, 0,0, 0,1, 1,1))
        )
vert_list2 = pyglet.graphics.vertex_list(6,
        ('v3f', (0,0,1, 1,0,-0.1, 1,1,-0.1, 0,0,-0.1, 0,1,-0.1, 1,1,-0.1)),
        ('1g2f', (0,0, 1,0, 1,1, 0,0, 0,1, 1,1))
        )
#v2f is vector 2 float, which has fixed input postion by pyglet. use 1g2f instead. [1th generic 2 of float]
#https://pyglet.readthedocs.io/en/latest/programming_guide/graphics.html#guide-graphics    

pyglet.gl.glPointSize(10)

pic = pyglet.image.load('honey.png')
tex = pic.get_texture()
pic2 = pyglet.image.load('onpa.png')
tex2 = pic2.get_texture()




glUseProgram(program)
glEnable(GL_TEXTURE_2D)
glEnable(GL_DEPTH_TEST)
glEnable(GL_BLEND)
glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
#glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR_MIPMAP_LINEAR)
#occurs bad act, donno why. anyway not use it!

cl = glGetUniformLocation(program, "tex1")
glUniform1i(cl,0)
    
@window.event
def on_draw():
    #glClear(GL_COLOR_BUFFER_BIT)
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    
    #glEnable(tex.target)
    #glEnable(GL_TEXTURE_2D)
    #glBindTexture(tex.target, tex.id)

    

    
    glBindTexture(tex.target, tex2.id)    
    vert_list2.draw(pyglet.gl.GL_TRIANGLES)

    glBindTexture(tex.target, tex.id)    
    vert_list.draw(pyglet.gl.GL_TRIANGLES)

    
    
    

    #glBindTexture(tex.target, tex2.id)
    #print(tex.id, tex2.id)
    #print(tex2.target)
    
    #vert_list.draw(pyglet.gl.GL_TRIANGLES)
    #glDisable(tex.target)

    #glBindTexture(tex2.target, tex2.id)
    #glUniform1i(cl,0)

    #vert_list.draw(pyglet.gl.GL_TRIANGLES)
    
pyglet.app.run()
