from pyglet.gl import *
#https://pyglet.readthedocs.io/en/latest/programming_guide/graphics.html

from pyglet.graphics import vertex_list, vertex_list_indexed
#pyglet.graphics.vertex_list

window = pyglet.window.Window()


pic = pyglet.image.load('yum128.png')
texture = pic.get_texture()
glEnable(GL_TEXTURE_2D)
#glBindTexture(texture.target, texture.id)

faces = [1,3,2, 0,1,2]
vertex_count = 4
vertex_coordinate = (0,0, 50,0, 50,50, 0,50)
vertex_uv = (0,0, 1,0, 1,1, 0,1)


#v3f n3f nt2f(n texture id kinds)
#texture unit 0 GL_TEXTURE0 for 0 or void, fine.
#https://pyglet.readthedocs.io/en/latest/programming_guide/graphics.html#guide-graphics    
vertex_list_indexed1 = vertex_list_indexed(vertex_count,
    faces,
    ('v2f', vertex_coordinate ),
    ('t2f', vertex_uv),
    )

@window.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT)
    vertex_list_indexed1.draw(GL_TRIANGLES)

pyglet.app.run()
