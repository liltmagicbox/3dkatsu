#https://stackoverflow.com/questions/63534240/how-to-set-window-hint-for-glfw-in-python
import glfw
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader
import numpy as np

vertex_src = """
# version 330 core
in vec3 a_position;
void main() {
    gl_Position = vec4(a_position, 1.0);
}
"""

fragment_src = """
# version 330 core
out vec4 out_color;
void main() {
    out_color = vec4(1.0, 0.0, 0.0, 1.0);
}
"""

if not glfw.init():
    print("Cannot initialize GLFW")
    exit()

glfw.window_hint(glfw.CONTEXT_VERSION_MAJOR, 4)
glfw.window_hint(glfw.CONTEXT_VERSION_MINOR, 6)
glfw.window_hint(glfw.OPENGL_FORWARD_COMPAT, True)
glfw.window_hint(glfw.OPENGL_PROFILE, glfw.OPENGL_CORE_PROFILE)
window = glfw.create_window(320, 240, "OpenGL window", None, None)
if not window:
    glfw.terminate()
    print("GLFW window cannot be creted")
    exit()

glfw.set_window_pos(window, 100, 100)
glfw.make_context_current(window)
print(glfw.get_version())
print(bool(glDrawArraysIndirect) )#thats the point. after make contex tcurrent!
vertices = [-0.5, -0.5, 0.0,
            0.5, -0.5, 0.0,
            0.0, 0.5, 0.0]
colors = [1, 0, 0.0, 0.0,
          0.0, 1.0, 0.0,
          0.0, 0.0, 1.0]
vertices = np.array(vertices, dtype=np.float32)
colors = np.array(colors, dtype=np.float32)
shader = compileProgram(compileShader(
    vertex_src, GL_VERTEX_SHADER), compileShader(fragment_src, GL_FRAGMENT_SHADER))

buff_obj = glGenBuffers(1)
glBindBuffer(GL_ARRAY_BUFFER, buff_obj)
glBufferData(GL_ARRAY_BUFFER, vertices.nbytes, vertices, GL_STATIC_DRAW)

vao = glGenVertexArrays(1)
glBindVertexArray(vao)

position = glGetAttribLocation(shader, "a_position")
glEnableVertexAttribArray(position)
glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 0, ctypes.c_void_p(0))

glUseProgram(shader)
glClearColor(0, 0.1, 0.1, 1)


while not glfw.window_should_close(window):
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glDrawArrays(GL_TRIANGLES, 0, 3)
    glfw.poll_events()
    glfw.swap_buffers(window)

glfw.terminate()