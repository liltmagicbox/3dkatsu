#https://codeloop.org/python-modern-opengl-drawing-triangle/
#https://www.youtube.com/watch?v=chaIYg7_7KM
#with pip install pyopengl


#---------------------------------
#https://pyglet.readthedocs.io/en/latest/programming_guide/graphics.html
from pyglet.gl import *

from pyglet.graphics import vertex_list, vertex_list_indexed, Batch

window = pyglet.window.Window()


#======================================================

#from OpenGL.GL import shaders, GL_VERTEX_SHADER, GL_FRAGMENT_SHADER
from OpenGL.GL import *
from OpenGL.GL import shaders

#OpenGL.GL.shaders.glUniform2f
#OpenGL.GL.shaders.glVertexAttrib2fv
#OpenGL.GL.shaders.glGetShaderSource
#kinds.fine.



# Shaders (Vertex and Fragment shaders)
v_source = """
#version 410
in vec2 position;
void main()
{
	gl_Position = vec4(0.7,0.7, 0.0, 1.0);
}
"""
f_source = """
#version 410
out vec4 outColor;
void main()
{
	outColor = vec4(1.0,0.0,1.0, 1.0);
}
"""
#outColor = vec4(1.0,0.0,1.0, 1.0);
#uniform vec3 triangleColor;


vshader = shaders.compileShader( v_source, GL_VERTEX_SHADER)
fshader = shaders.compileShader( f_source, GL_FRAGMENT_SHADER)
program = shaders.compileProgram( vshader,fshader)


#=============================================================
b = Batch()
#count mode group (indices) data
b.add_indexed(4, GL_TRIANGLES, None,
    [0,1,2, 0,2,3],
    ('v2i', (50, 50, 300,50, 300,300, 50,300) ),
    #('c3B', (0, 0, 255, 0, 255, 0, 255,0,0, 255,255,0)),
    )

@window.event
def on_draw():
    global program
    #glClearColor(0.2,0.3,0.2,1.0)
    glClear(GL_COLOR_BUFFER_BIT)

    glUseProgram(program)
    b.draw()
    glUseProgram(0)


pyglet.app.run()


#-------------------------------

