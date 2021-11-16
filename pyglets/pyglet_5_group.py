#group. gltexture acts differently, so need it maybe.

from pyglet.gl import *
#https://pyglet.readthedocs.io/en/latest/programming_guide/graphics.html

from pyglet.graphics import vertex_list, vertex_list_indexed, Batch
#pyglet.graphics.vertex_list

from pyglet import image
pic = image.load('pic2.jpg')
texture = pic.get_texture()

window = pyglet.window.Window()


class CustomGroup(pyglet.graphics.Group):
    def set_state(self):
        glEnable(texture.target)
        glBindTexture(texture.target, texture.id)

    def unset_state(self):
        glDisable(texture.target)

g = CustomGroup()

b = Batch()
#count mode group (indices) data
b.add_indexed(4, GL_TRIANGLES, g,
    [0,1,2, 0,2,3],
    ('v2i', (0, 0, 50,0, 50,50, 0,50) ),
    #('c3B', (0, 0, 255, 0, 255, 0, 255,0,0, 255,255,0)),
    ('t2f', (0,0, 1,0, 1,1, 0,1)),
    )

# FOR attrib.change: vlist = b.add(3, GL_TRIANGLES, None,
b.add(3, GL_LINE_STRIP, None,
      ('v2i', (100,100,  150,100, 100,150) ),      
      ('c3B', (0, 0, 255, 0, 255, 0, 255,0,0, )),
       )

@window.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT)

    #draw() 1 required positional argument: 'mode'
    # GL_POINTS GL_LINE_STRIP GL_TRIANGLES

    b.draw()

pyglet.app.run()
