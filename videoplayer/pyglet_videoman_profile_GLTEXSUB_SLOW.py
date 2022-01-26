import pyglet
import moviepy.editor as mpy
import imageio as iio
from OpenGL.GL import *
from OpenGL.GL import shaders
import numpy as np
#=============================== PLAYER

# https://zulko.github.io/moviepy/getting_started/videoclips.html
# # VIDEO CLIPS
# clip = VideoClip(make_frame, duration=4) # for custom animations (see below)
# clip = VideoFileClip("my_video_file.mp4") # or .avi, .webm, .gif ...
# clip = ImageSequenceClip(['image_file1.jpeg', ...], fps=24)
# clip = ImageClip("my_picture.png") # or .jpeg, .tiff, ...
# clip = TextClip("Hello !", font="Amiri-Bold", fontsize=70, color="black")
# clip = ColorClip(size=(460,380), color=[R,G,B])

# # AUDIO CLIPS
# clip = AudioFileClip("my_audiofile.mp3") # or .ogg, .wav... or a video !
# clip = AudioArrayClip(numpy_array, fps=44100) # from a numerical array
# clip = AudioClip(make_frame, duration=3) # uses a function make_frame(t)

def rangesafe(value,vmin,vmax):
    if value < vmin:
        value = vmin
    elif value > vmax:
        value = vmax
    return value

class Audioplayer:
    def __init__(self,audioname):
        self.source = pyglet.media.load(audioname,streaming=False)
        self.player = pyglet.media.Player()
        #self.player.queue(self.source)

        #p.source
        #<pyglet.media.codecs.base.StaticMemorySource object at 0x00000118C55E6DC0>
    def play(self):
        if self.player.playing:
            pass
        if self.player.source == None: #seems source vanishes when play ends.
            self.player.queue(self.source)
            self.player.play()
        else:
            self.player.play()
    def pause(self):
        self.player.pause()

    def play_pause(self):
        if self.player.playing:            
            self.pause()
        else:
            self.play()
    def get_time(self):
        return self.player.time
    def get_maxtime(self):
        return self.source.duration

    def volup(self, val=0.1):
        vol = self.player.volume +val
        self.player.volume = rangesafe(vol, 0,1)
    def voldown(self, val=0.1):
        vol = self.player.volume -val
        self.player.volume = rangesafe(vol, 0,1)
        
    def seek(self,time):
        newtime = self.player.time + time
        maxt = self.source.duration
        mint = 0
        newtime = rangesafe(newtime, mint, maxt)
        if newtime == maxt: #it skips playing =False state change.
            #self.player.source = None #not working
            newtime-=0.001 #this prevents such. #best way till..
            #or
            #self.pause()
            #self.seek(0)
            #not working, infloop?
        self.player.seek(newtime)


    def key(self, symbol, modifiers):
        if symbol == key.P:
            self.play_pause()
        if symbol == key.SPACE:
            self.play_pause()
        if symbol == key.RIGHT:
            val = 1
            if modifiers & key.MOD_SHIFT:
                pass
            if modifiers & key.MOD_CTRL:
                val *= 5
            self.seek(val)
        if symbol == key.LEFT:
            val = -1
            if modifiers & key.MOD_CTRL:
                val *= 5
            self.seek(val)
        if symbol == key.UP:
            self.volup(0.1)            
        if symbol == key.DOWN:
            self.voldown(0.1)

        if symbol == key.T:
            t = self.get_time()
            print(t)

    

class MultiPlayer:
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


class Videoplayer:
    def __init__(self,videoname):
        clip = mpy.VideoFileClip(videoname)
        audioname = f"tmp_{videoname}.mp3"
        #clip.audio.write_audiofile(audioname, bitrate = '192k',logger=None)
        clip.audio.write_audiofile(audioname, logger=None)
        clip = None

        self.audio = Audioplayer(audioname)

        #use get_data or iter_data (with _pos. get_next_data)
        video = iio.get_reader(videoname)
        size = video.get_meta_data()['size']
        fps = video.get_meta_data()['fps']
        duration = video.get_meta_data()['duration']
        framesa = video.count_frames()
        framesb = duration*fps
        maxfps = int(framesb)
        
        self.video = video
        self.size = size
        self.fps = fps
        self.duration = duration
        self.maxfps = maxfps
        
        self.isplaying = False
        self.idx = 0
        self.frame = self.video.get_data(0)
        #self.texture =
        self._create_texture(self.frame)

    def get_time(self):
        return self.audio.get_time()
    def get_idx(self):
        return self.idx
    def get_frame(self):
        """returns np array"""
        return self.frame
    def get_texture(self):
        """updated by update"""
        return self.texture

    def _create_texture(self,frame, rgb = 'RGBA'):#says rgba 20x faster..
        frame = frame[::-1,:]#reverse
        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)#GL_NEAREST
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)

        #(1080, 1920, 3)
        height,width,depth = frame.shape
        
        IMG_MODE = GL_RGB
        if rgb == 'RGB':
            IMG_MODE = GL_RGB
        elif rgb == 'BGR':
            IMG_MODE = GL_BGR
        elif rgb == 'BGRA':
            IMG_MODE = GL_BGRA
        #if depth == 3:
            #IMG_MODE = GL_RGB
        #elif depth == 4:
            #IMG_MODE = GL_RGBA
        glTexImage2D(GL_TEXTURE_2D, 0, IMG_MODE, width, height, 0, IMG_MODE, GL_UNSIGNED_BYTE, frame )#level, border=0
        glBindTexture(GL_TEXTURE_2D, 0)
        self.IMG_MODE = IMG_MODE
        self.texture = texture
        self.width = width
        self.height = height

    @profile
    def _update_texture(self,frame):
        #np.flipud
        frame = frame[::-1,:]#reverse ..but slow!
        #frame = np.flipud(frame)
        texture = self.texture
        IMG_MODE = self.IMG_MODE
        width = self.width
        height = self.height
        glBindTexture(GL_TEXTURE_2D, texture)
        #fff= frame.tobytes()#was the man!
        #print(frame.dtype)# it works!yeah!!!
        glTexSubImage2D(GL_TEXTURE_2D, 0, 0, 0, width, height, IMG_MODE, GL_UNSIGNED_BYTE, frame )
        glBindTexture(GL_TEXTURE_2D, 0)
        
    
    def update(self):
        """idx is frame idx. we get time from audio"""
        time = self.audio.get_time()        
        frameidx = int( time * self.fps )
        if not self.idx == frameidx:
            if frameidx <= self.maxfps:
                self.idx = frameidx                
                frame = self.video.get_data(frameidx)
                self.frame = frame
                self._update_texture(frame)
                #NOTE: even 139max, overs 142 when play,pause fast.
        #print(frameidx)

        

    def play_pause(self):
        if self.isplaying:
            self.pause()
        else:
            self.play()    
    def play(self):
        self.isplaying = True
        self.audio.play()
        #self.video.play() use update_frame and get_frame each.
    def pause(self):
        self.isplaying = False
        self.audio.pause()
        #self.video.pause()

    def key(self, symbol, modifiers):
        self.audio.key(symbol,modifiers)


#=============================== PLAYER


if __name__ == '__main__':
    window = pyglet.window.Window()
    window.set_vsync(False)
    
    vertn = """
    #version 410
    layout (location = 0) in vec2 cord;
    layout (location = 1) in vec2 uv;
    out vec2 uvcord;

    void main() 
    {
        gl_Position = vec4(cord, 0,1);
        uvcord = uv;
    }
    """

    fragn = """
    #version 410
    in vec2 uvcord;
    out vec4 outcolor;
    uniform sampler2D tex1;

    void main()
    {
        outcolor = texture2D(tex1, uvcord);
    }
    """


    vshader = shaders.compileShader( vertn, GL_VERTEX_SHADER)
    fshader = shaders.compileShader( fragn, GL_FRAGMENT_SHADER)
    program = shaders.compileProgram( vshader,fshader)

    vert_list = pyglet.graphics.vertex_list(6,
        ('v2f', (0,0, 1,0, 1,1, 0,0, 1,1, 0,1)),
        ('1g2f', (0,0, 1,0, 1,1, 0,0, 1,1, 0,1))
        )



    from pyglet.window import key

    @window.event
    def on_key_press(symbol, modifiers):
        #sym 48-57 0-9  , 97-122 a-z
        #key no a but A
        #normal 16, shift17, ctrl 18, alt 20
        #MOD normal 24, shift 25, ctrl 26, alt 28.
        # ^^^ if capslocked.hahaha.
        #if symbol == key.W:
        #print(symbol,modifiers)
        #MOD_ALT         Not available on Mac OS X
        #10 & 101 0  if modifiers & MOD_SHIFT:
        a.key(symbol,modifiers)

    @window.event
    def on_mouse_press(x, y, button, modifiers):
        print(button)
        if button == 1:
            a.play()
        if button == 4:
            a.pause()
        if button == 2:
            a.play_pause()


    def update(dt):
        if not dt==0:
            1
            #print(1/dt)
        a.update()
    #pyglet.clock.schedule(update)
    pyglet.clock.schedule_interval(update, 0.01)
        
    @window.event
    def on_draw():
        glClear(GL_COLOR_BUFFER_BIT)    
        glUseProgram(program)

        glBindTexture(GL_TEXTURE_2D, a.texture)
        vert_list.draw(pyglet.gl.GL_TRIANGLES)

    #a = Audioplayer('summer.mp3')
    a = Videoplayer('bibitokita.mp4')
    pyglet.app.run()