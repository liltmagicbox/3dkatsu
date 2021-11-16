import os
if os.name == "nt":
    ffholdingdir = os.path.join( os.getcwd(), "ffmpeg" )
    ffholdingdir = ';'+ffholdingdir
    os.environ["PATH"] += ffholdingdir
    
else:
    os.environ["LD_LIBRARY_PATH"] += ":" + os.path.join( os.getcwd(), "ffmpeg" )

from pyglet.gl import *
#https://pyglet.readthedocs.io/en/latest/programming_guide/graphics.html

from pyglet.graphics import vertex_list, vertex_list_indexed, Batch
#pyglet.graphics.vertex_list

from pyglet.window import key


#--ffmpegs
pyglet.options['search_local_libs'] = True
print( 'ffhasve',pyglet.media.have_ffmpeg() )


#---
#explosion = pyglet.media.load('explosion.wav', streaming=False)
source = pyglet.media.load('star.mp4', streaming = True)


w = source.video_format.width
h = source.video_format.height

window = pyglet.window.Window(w,h)
#window = pyglet.window.Window()

a = source.get_next_video_frame()
#window.width, window.height = a.width , a.height

player = pyglet.media.Player()
player.queue(source)

player.play()
@window.event
def on_draw():
    #glClear(GL_COLOR_BUFFER_BIT)
    player.texture.blit(0, 0)
    #t is internal format of either GL_TEXTURE_2D or GL_TEXTURE_RECTANGLE_ARB


pyglet.app.run()
