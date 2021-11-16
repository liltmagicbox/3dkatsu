#group. gltexture acts differently, so need it maybe.

from pyglet.gl import *
#https://pyglet.readthedocs.io/en/latest/programming_guide/graphics.html

from pyglet.graphics import vertex_list, vertex_list_indexed, Batch
#pyglet.graphics.vertex_list

from pyglet import image
pic = image.load('pic2.jpg')
texture = pic.get_texture()

window = pyglet.window.Window()
#-----------------texture use group. one skips gl texture use fine.
class CustomGroup(pyglet.graphics.Group):
    def set_state(self):
        glEnable(texture.target)
        glBindTexture(texture.target, texture.id)

    def unset_state(self):
        glDisable(texture.target)

class CustomGroup_texture(pyglet.graphics.Group):
    def __init__(self,texture):#need super kinds. became complexed..
        self.texture = texture
    def set_state(self):
        glEnable(texture.target)
        glBindTexture(texture.target, texture.id)

    def unset_state(self):
        glDisable(texture.target)
#g = CustomGroup_texture(texture)

#g = CustomGroup()
#---------------there was textgure group! acts like as i imagined
g = pyglet.graphics.TextureGroup(texture)


class CustomGroup2(pyglet.graphics.Group):
    def set_state(self):
        print('ha')

    def unset_state(self):
        print('hu')

notex = CustomGroup2()


b = Batch()
#count mode group (indices) data
b.add_indexed(4, GL_TRIANGLES, g,
    [0,1,2, 0,2,3],
    ('v2i', (0, 0, 50,0, 50,50, 0,50) ),
    #('c3B', (0, 0, 255, 0, 255, 0, 255,0,0, 255,255,0)),
    ('t2f', (0,0, 1,0, 1,1, 0,1)),
    )

# FOR attrib.change: vlist = b.add(3, GL_TRIANGLES, None,
b.add(3, GL_LINE_STRIP, notex,
      ('v2i', (100,100,  150,100, 100,150) ),      
      ('c3B', (0, 0, 255, 0, 255, 0, 255,0,0, )),
       )




#-----------------ordered group. use with parent kinds..
background = pyglet.graphics.OrderedGroup(0)
foreground = pyglet.graphics.OrderedGroup(1)



class CustomGroup3(pyglet.graphics.Group):
    def set_state(self):
        print(self.parent)

    def unset_state(self):
        print('foreground')
frontgroup = CustomGroup3(parent = foreground)
#frontgroup.parent = foreground

b2=Batch()
b2.add(3, GL_TRIANGLES, frontgroup,
      ('v2i', (280,280,  350,280, 280,350) ),      
      ('c3B', (255, 0, 255, 255, 255, 0, 255,0,0, )),
       )
b2.add(3, GL_TRIANGLES, foreground,
      ('v2i', (250,250,  350,250, 250,350) ),      
      ('c3B', (0, 0, 255, 0, 255, 0, 255,0,0, )),
       )
b2.add(3, GL_TRIANGLES, background,
      ('v2i', (200,200,  350,200, 200,350) ),      
      #('c3B', (0, 0, 255, 0, 255, 0, 255,0,0, )),
       )



@window.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT)

    #draw() 1 required positional argument: 'mode'
    # GL_POINTS GL_LINE_STRIP GL_TRIANGLES

    #b.top_groups[0].set_state() NEVER DO THIS! group auto called.
    b.draw()
    b2.draw()
    #b.top_groups[0].unset_state()NEVER..

pyglet.app.run()
