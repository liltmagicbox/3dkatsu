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
#OLD FIXED FRAG SHADER.
#NOTE: legacy version 120 can use modelviewprojectionmat..

verto = """
#version 120
void main() 
{
    gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
}
"""

frago = """
#version 120
void main() 
{
    gl_FragColor = vec4(1, 0, 1, 1);
}
"""
#===================================



#===================================
#NEW SHADER_ standalone
vertns = """
#version 410
void main() 
{
    gl_Position = vec4(0.5, 0.5, 0.0, 1);
    
}
"""

fragns= """
#version 410
void main() 
{
    gl_FragColor = vec4(1, 0, 1, 1);
}
"""
#===================================
#new shader, with attrb. note: vertex cord automatically location0.  1g3f atleast. not 0g3f.

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



#=============================================================
pyglet.gl.glPointSize(10)


@window.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT)
    #GL_TRIANGLES GL_POINTS... / v2f means vector 2, float. v3i vector int 3. kinds.
    glUseProgram(program)
    #pyglet.graphics.draw(3, pyglet.gl.GL_POINTS, ('v2f', (0,0, 0.5,0.5, 0.5,0) ) ) #for old shader
    pyglet.graphics.draw(3, pyglet.gl.GL_POINTS, ('v2f', (0,0, 0.5,0.5, 0.5,0) ),('1g3f', (0,0,1, 0,1,0, 1,0,0, )) )
    #glUseProgram(0)# means we do not use shader, draw nothing!
    pyglet.graphics.draw(3, pyglet.gl.GL_POINTS, ('v2f', (-0.5,0, -0.5,-0.5, 0.5,0) ),('1g3f', (0,0,1, 0,1,0, 1,0,0, )) )

pyglet.app.run()
