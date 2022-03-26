#https://github.com/totex/PyOpenGL_tutorials/blob/master/main.py

#import glfw

from glfw import _GLFWwindow as GLFWwindow
from glfw.GLFW import *
from OpenGL.GL import *
import OpenGL.GL.shaders
##from OpenGL.GL import shaders
import numpy


SCR_WIDTH = 800
SCR_HEIGHT = 600

def main():
    if not glfwInit():
        return
    glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 4)
    glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 3)
    glfwWindowHint(GLFW_OPENGL_PROFILE, GLFW_OPENGL_CORE_PROFILE)
    #window = glfw.create_window(800, 600, "My OpenGL window", None, None)
    #glfwWindowHint(GLFW_CONTEXT_VERSION_MAJOR, 3)
    #glfwWindowHint(GLFW_CONTEXT_VERSION_MINOR, 1)
    
    glfwWindowHint(GLFW_DOUBLEBUFFER, GLFW_TRUE)#for vsync. we do d.buffer atleast!!

    window = glfwCreateWindow(SCR_WIDTH, SCR_HEIGHT, "My OpenGL window", None, None)
    if not window:
        glfwTerminate()
        return
    glfwMakeContextCurrent(window)
    glfwSetFramebufferSizeCallback(window, framebuffer_size_callback)
    glfwSetCursorPosCallback(window, mouse_callback)
    glfwSetScrollCallback(window, scroll_callback)

    glfwSetInputMode(window, GLFW_CURSOR, GLFW_CURSOR_DISABLED)
    glEnable(GL_DEPTH_TEST)

    # initialize glfw
    #            positions        colors
    triangle = [-0.5, -0.5, 0.0, 1.0, 0.0, 0.0,
                 0.5, -0.5, 0.0, 0.0, 1.0, 0.0,
                 0.0,  0.5, 0.0, 0.0, 0.0, 1.0]

    triangle = numpy.array(triangle, dtype = numpy.float32)

    vertex_shader = """
    #version 330
    in vec3 position;
    in vec3 color;
    out vec3 newColor;
    void main()
    {
        gl_Position = vec4(position, 1.0f);
        newColor = color;
    }
    """

    fragment_shader = """
    #version 330
    in vec3 newColor;
    out vec4 outColor;
    void main()
    {
        outColor = vec4(newColor, 1.0f);
    }
    """
    shader = OpenGL.GL.shaders.compileProgram(OpenGL.GL.shaders.compileShader(vertex_shader, GL_VERTEX_SHADER),
                                             OpenGL.GL.shaders.compileShader(fragment_shader, GL_FRAGMENT_SHADER))


    VAO = glGenVertexArrays(1) # create a VA. if 3, 3of VA got. #errs if no window.
    glBindVertexArray(VAO)
    
    VBO = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, VBO)
    glBufferData(GL_ARRAY_BUFFER, 72, triangle, GL_STATIC_DRAW)

    position = glGetAttribLocation(shader, "position")
    glVertexAttribPointer(position, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(0))    
    glEnableVertexAttribArray(position)

    color = glGetAttribLocation(shader, "color")
    glVertexAttribPointer(color, 3, GL_FLOAT, GL_FALSE, 24, ctypes.c_void_p(12))
    #glVertexAttribPointer(attr_index, size, datatype, normalized, stride * fsize, offset)
    glEnableVertexAttribArray(color)

    glUseProgram(shader)


    glClearColor(0.2, 0.3, 0.2, 1.0)
    timebefore=0
    while not glfwWindowShouldClose(window):
        timenow = glfwGetTime()
        print(timenow-timebefore)
        timebefore = timenow

        
        processInput(window)
        #if glfwGetKey(window, GLFW_KEY_ESCAPE) == GLFW_PRESS:        

        #glClear(GL_COLOR_BUFFER_BIT)
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        
        glDrawArrays(GL_TRIANGLES, 0, 3)

        #dbuffer True, use swapbuffer. interval0 if fullspeed test.
        #dbuffer False, use glFlush, the old way maybe.fine.
        #glfwSwapInterval(1)# 10 160ms tooslow, 1 16ms, 0 fastest
        glfwSwapBuffers(window)#requires dbuffer True.
        #glFlush()#when not using vsync #-- we found, flush returns anytime, not after exc.
        
        
        glfwPollEvents()

    glfwTerminate()



# process all input: query GLFW whether relevant keys are pressed/released this frame and react accordingly
# ---------------------------------------------------------------------------------------------------------
def processInput(window) -> None:
    global deltaTime
    #GLFW_KEY_ESCAPE
    if (glfwGetKey(window, GLFW_KEY_ESCAPE) == GLFW_PRESS):
        #glfwSetWindowShouldClose(window, True)
        glfwSetWindowShouldClose(window,True)


    if (glfwGetKey(window, GLFW_KEY_W) == GLFW_PRESS):
        camera.ProcessKeyboard(Camera_Movement.FORWARD, deltaTime)
    if (glfwGetKey(window, GLFW_KEY_S) == GLFW_PRESS):
        camera.ProcessKeyboard(Camera_Movement.BACKWARD, deltaTime)
    if (glfwGetKey(window, GLFW_KEY_A) == GLFW_PRESS):
        camera.ProcessKeyboard(Camera_Movement.LEFT, deltaTime)
    if (glfwGetKey(window, GLFW_KEY_D) == GLFW_PRESS):
        camera.ProcessKeyboard(Camera_Movement.RIGHT, deltaTime)

# glfw: whenever the window size changed (by OS or user resize) this callback function executes
# ---------------------------------------------------------------------------------------------
def framebuffer_size_callback(window: GLFWwindow, width: int, height: int) -> None:
#def framebuffer_size_callback(window, width: int, height: int) -> None:

    # make sure the viewport matches the new window dimensions note that width and 
    # height will be significantly larger than specified on retina displays.
    glViewport(0, 0, width, height)

# glfw: whenever the mouse moves, this callback is called
# -------------------------------------------------------
#def mouse_callback(window, xpos: float, ypos: float) -> None:
def mouse_callback(window: GLFWwindow, xpos: float, ypos: float) -> None:
    return
    global lastX, lastY, firstMouse

    if (firstMouse):

        lastX = xpos
        lastY = ypos
        firstMouse = False

    xoffset = xpos - lastX
    yoffset = lastY - ypos # reversed since y-coordinates go from bottom to top

    lastX = xpos
    lastY = ypos

    camera.ProcessMouseMovement(xoffset, yoffset)

# glfw: whenever the mouse scroll wheel scrolls, this callback is called
# ----------------------------------------------------------------------
def scroll_callback(window: GLFWwindow, xoffset: float, yoffset: float) -> None:
#def scroll_callback(window, xoffset: float, yoffset: float) -> None:
    camera.ProcessMouseScroll(yoffset)

if __name__ == "__main__":
    #print(glfw.poll_events,'ggee')
    print(glfwPollEvents,'eee')
    main()