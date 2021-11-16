from pyglet.gl import *
#https://pyglet.readthedocs.io/en/latest/programming_guide/graphics.html

from pyglet.graphics import vertex_list, vertex_list_indexed, Batch
#pyglet.graphics.vertex_list

window = pyglet.window.Window()


b = Batch()
#count mode group (indices) data
b.add_indexed(4, GL_LINE_STRIP, None,
    [0,1,2, 0,2,3],
    ('v2i', (0, 0, 50,0, 50,50, 0,50) ),
    ('c3B', (0, 0, 255, 0, 255, 0, 255,0,0, 255,255,0)),
    )

b.add(3, GL_TRIANGLES, None,
      ('v2i', (100,100,  150,100, 100,150) )
       )

@window.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT)

    #draw() 1 required positional argument: 'mode'
    # GL_POINTS GL_LINE_STRIP GL_TRIANGLES
    b.draw()

pyglet.app.run()
