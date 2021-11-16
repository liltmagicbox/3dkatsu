from pyglet.gl import *

window = pyglet.window.Window()


@window.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT)
    #GL_TRIANGLES GL_POINTS... / v2f means vector 2, float. v3i vector int 3. kinds.
    pyglet.graphics.draw(3, pyglet.gl.GL_TRIANGLES, ('v2f', (50.5, 50.5, 70, 70, 50,90)) )

pyglet.app.run()
