from pyglet.gl import *
#https://pyglet.readthedocs.io/en/latest/programming_guide/graphics.html

from pyglet.graphics import vertex_list, vertex_list_indexed, Batch
#pyglet.graphics.vertex_list

from pyglet.window import key
from pyglet import clock

window = pyglet.window.Window()

#source1 = pyglet.media.load('sound/tetris.mp3',streaming=False)
source2 = pyglet.media.load('sound/drum_snare.mp3',streaming=False)
source3 = pyglet.media.load('sound/drum_hihat.mp3',streaming=False)
source4 = pyglet.media.load('sound/drum_crash.mp3',streaming=False)
source1 = pyglet.media.load('sound/drum_bass.mp3',streaming=False)

sources = (source1,source2,source3,source4)

class Player:
    def __init__(self):
        self.players = []
        self.fill(5)
    def fill(self,N=1):
        for i in range(N):
            self.players.append(pyglet.media.Player())
    def get(self):
        for i in self.players:
            if not i.playing:
                return i
        #was no available..
        self.fill()
        return self.players[-1]

    def play(self,num):
        source = sources[num-1]
        
        player = self.get()
        player.queue(source)
        player.play()
        print(len(self.players))


player = Player()

@window.event
def on_key_press(symbol,modifiers):    
    if symbol == key.A:        
        #print('The "1" key was pressed.')
        player.play(1)
    elif symbol == key.S:        
        #print('The "2" key was pressed.')
        player.play(2)
    elif symbol == key.D:        
        #print('The "3" key was pressed.')
        player.play(3)
    elif symbol == key.F:        
        #print('The "4" key was pressed.')
        player.play(4)

@window.event
def on_mouse_press(x, y, button, modifiers):
    player.play(1)
    
@window.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT)
    

pyglet.app.run()
