from pyglet.gl import *
#https://pyglet.readthedocs.io/en/latest/programming_guide/graphics.html

from pyglet.graphics import vertex_list, vertex_list_indexed, Batch
#pyglet.graphics.vertex_list

from pyglet.window import key

window = pyglet.window.Window()


class sman:
    def __init__(self, filename):
        self.source = pyglet.media.load(f'sound/{filename}.mp3',streaming=False)

        self.players = []
        self.add()
    
    def add(self):
        players = self.players
        source = self.source

        player = pyglet.media.Player()
        player.queue(source)
        player.seek(0)
        players.append(player)
        
    def play(self,after=None):
        players = self.players
        nplayer = players.pop()
        nplayer.play()
        nplayer.delete()
        self.add()
        if after:
            after.play()

source = pyglet.media.load('sound/fire_m4a1.mp3',streaming=False)
#player.queue(source)
player = pyglet.media.Player()

@window.event
def on_key_press(symbol,modifiers):
    
    if symbol == key.P:        
        print('The "P" key was pressed.')
        player.queue(source)
        player.play()
    if symbol == key.A:        
        print('The "A" key was pressed.')
        player.queue(source2)
        player.play()
    if symbol == key.B:
        print('ha')
        player.seek(0)
        player.play()
        
    if symbol == key.C:
        #for i in range(20):
        #nplayer = pyglet.media.Player()
        #nplayer.queue(source)
        #nplayer.seek(0)
        #nplayer.play()
        #nplayer.delete()

        fire()

s = sman('fire_m4a1')
r = sman('shell')
from pyglet import clock

def cal(dt):
    global r
    #print(dt,'cacll')
    r.play()

@window.event
def on_mouse_press(x, y, button, modifiers):
    #fire()
    s.play()
    #r.play()
    #clock.schedule_once(cal, 0.7)#1-10ms added.
    
    


@window.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT)
    

pyglet.app.run()
