from pyglet.gl import *
from pyglet.graphics import vertex_list, vertex_list_indexed, Batch
from pyglet import image

animation = pyglet.image.load_animation('him.gif')
bin = pyglet.image.atlas.TextureBin()
animation.add_to_texture_bin(bin)
sprite = pyglet.sprite.Sprite(img=animation)

window = pyglet.window.Window()


#---my gifkinds.
pic = image.load('pic2.jpg')
#bb = pyglet.sprite.Sprite(pic)


class mysp(pyglet.sprite.Sprite):
    def __init__(self,pic,x,y):
        super(mysp,self).__init__(pic,x,y)
        self.maha=0
    def draw(self):
        print('ha')
        print(self.scale)
        self.maha+=1
        print(self.maha)
        #self.rotation = self.maha
        self.update(x=None, y=None, rotation=self.maha, scale=None, scale_x=None, scale_y=None)

        #self.draw() NOT this. recursive error.
        super().draw() #grab super's method, maybe fine with it.        
bb = mysp(pic,400,300)
bb.scale = 0.5

#---
@window.event
def on_draw():
    window.clear()    
    sprite.draw()
    bb.draw()
    

pyglet.app.run()
