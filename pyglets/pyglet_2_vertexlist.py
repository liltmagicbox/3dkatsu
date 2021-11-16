from pyglet.gl import *
#https://pyglet.readthedocs.io/en/latest/programming_guide/graphics.html

from pyglet.graphics import vertex_list
#pyglet.graphics.vertex_list

window = pyglet.window.Window()


"""
vertex_list(count, *data)
    Create a :py:class:`~pyglet.graphics.vertexdomain.VertexList`
    not associated with a batch, group or mode.

`count` : int
            The number of vertices in the list.

`data` : data items
            Attribute formats and initial data for the vertex list.  See the
            module summary for details.


vertex_list_1vertices = vertex_list(1,
    ('v2f', (10, 15)),
    )

vertex_list_2vertices = pyglet.graphics.vertex_list(2,
    ('v2i', (10, 15, 30, 35)),
    )
vertex_list_2vertices = pyglet.graphics.vertex_list(2,
    ('v2i', (10, 15, 30, 35)),
    ('c3B', (0, 0, 255, 0, 255, 0))
    )


vertex_list_3vertices = pyglet.graphics.vertex_list(3,
    ('v2i', (10, 15, 30, 35, 40, 45)),
    ('c3B', (0, 0, 255, 0, 255, 0, 255,0,0))#not B! 'b' is Signed byte
    )

"""

vertex_list1 = vertex_list(3,
    ('v2i', (10, 15, 40, 10, 40, 45)),
    ('c3B', (0, 0, 255, 0, 255, 0, 255,0,0))
                           )

@window.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT)

    #draw() 1 required positional argument: 'mode'
    # GL_POINTS GL_LINE_STRIP GL_TRIANGLES
    vertex_list1.draw(GL_LINE_STRIP)

pyglet.app.run()
