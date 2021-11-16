from pyglet.gl import *
#https://pyglet.readthedocs.io/en/latest/programming_guide/graphics.html

from pyglet.graphics import vertex_list, vertex_list_indexed, Batch
#pyglet.graphics.vertex_list

from pyglet import image
pic = image.load('pic2.jpg')
#texture = pic.get_texture()


window = pyglet.window.Window()

b = Batch()


#>>> bb.scale 1.0
#>>> bb.opacity 255
#>>> bb.rotation 0

#bb = pyglet.sprite.Sprite(pic, x=50,y=50)
bb = pyglet.sprite.Sprite(pic)
#bb.rotation = 33#degree ,point = x,y
#bb.opacity = 30 worksa fine!

#pyglet.sprite.Sprite(pic, x=50,y=50,batch = b)
#batch however not working, maybe position??

#note: sprite requires .delete() for video memory. batch del..
#NOW batch working great. fine.
#update(x=None, y=None, rotation=None, scale=None, scale_x=None, scale_y=None)

#https://pyglet.readthedocs.io/en/latest/modules/sprite.html
#bb.color= (255,0,0) blend works fine. by-add calc. 0 for black, 255 for pass

#The sprite can change its rendering group, however this can be an expensive operation.
#huh.

#a.get_data()
#<pyglet.image.codecs.wic.c_byte_Array_497600 object at 0x000001FAFEBA2DC0>
#d=pic.get_data('RGB')
#>>> d
#>>> d[0] 96
#>>> d[:90]
#b'``````aaa```aacaac`ac`ac`ac`ac``b__a^^`]]_\\\\^\\\\^]]_]]_]]_\\\\^\\\\^\\\\^[[]ZZ\\\\\\^[[][[]ZZ\\ZZ\\ZZ\\'


sp=[]
for i in range(10):
    x,y = i*30,i*20
    sp.append(pyglet.sprite.Sprite(pic, x,y, batch = b) )

@window.event
def on_draw():
    for i in sp:
        i.rotation += 30
    glClear(GL_COLOR_BUFFER_BIT)
    bb.draw()

pyglet.app.run()

