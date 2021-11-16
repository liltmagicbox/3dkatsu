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

#NOTE: legacy version 120 can use modelviewprojectionmat..
"""
        #version 120
        void main() 
        {
            gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
        }
"""


# Shaders (Vertex and Fragment shaders)
v_source = """
        #version 120
        void main() 
        {
            gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
        }
        """
f_source = """
#version 120
        void main() 
        {
            gl_FragColor = vec4(1, 0, 1, 1);
        }
"""
#outColor = vec4(1.0,0.0,1.0, 1.0);
#uniform vec3 triangleColor;


vshader = shaders.compileShader( v_source, GL_VERTEX_SHADER)
fshader = shaders.compileShader( f_source, GL_FRAGMENT_SHADER)
program = shaders.compileProgram( vshader,fshader)


#=============================================================
pyglet.gl.glPointSize(10)
glUseProgram(program)

@window.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT)
    #GL_TRIANGLES GL_POINTS... / v2f means vector 2, float. v3i vector int 3. kinds.
    pyglet.graphics.draw(3, pyglet.gl.GL_POINTS, ('v2f', (50.5, 50.5, 70, 70, 50,90)) )

pyglet.app.run()
