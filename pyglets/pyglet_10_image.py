from pyglet.gl import *
#https://pyglet.readthedocs.io/en/latest/programming_guide/graphics.html

from pyglet.graphics import vertex_list, vertex_list_indexed
#pyglet.graphics.vertex_list

window = pyglet.window.Window()

vertex_list_indexed1 = vertex_list_indexed(4,
    [0,1,2, 0,2,3],
    ('v2i', (0,0, 50,0, 50,50, 0,50) ),
    ('c3B', (0, 0, 255, 0, 255, 0, 255,0,0, 255,255,0)),
    #('t2f', (0,0, 1,0, 1,1, 0,1)),
    )

vertex_list_indexed2 = vertex_list_indexed(4,
    [0,1,2, 0,2,3],
    ('v2i', (90,90, 150,90, 150,150, 90,150) ),
    ('c3B', (0, 0, 255, 0, 255, 0, 255,0,0, 255,255,0)),
    #('t2f', (0,0, 1,0, 1,1, 0,1)),
    )

@window.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT)

    #draw() 1 required positional argument: 'mode'
    # GL_POINTS GL_LINE_STRIP GL_TRIANGLES
    vertex_list_indexed1.draw(GL_LINE_STRIP)
    vertex_list_indexed2.draw(GL_TRIANGLES)

pyglet.app.run()

#----
"""
ccc=vertex_list_indexed1.colors
print(ccc)
<pyglet.graphics.vertexattribute.c_ubyte_Array_12 object at 0x0000021AAE4226C0>
[i for i in ccc]
[0, 0, 255, 0, 255, 0, 255, 0, 0, 255, 255, 0]

>>> ccccc=vertex_list_indexed1.vertices
>>> [i for i in ccccc]
[0, 0, 50, 0, 50, 50, 0, 50]

and normals tex_coords for_coords..
"""
