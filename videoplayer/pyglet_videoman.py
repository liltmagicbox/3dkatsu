import pyglet
from pyglet.window import key

import moviepy.editor as mpy
import imageio as iio
from OpenGL.GL import *
from OpenGL.GL import shaders
import numpy as np
import os
import time






class TEXTURE_2X:
    def __init__(self, width,height, FORMAT = GL_RGB ):
        a = TEXTURE_NOMIPMAP(width,height, FORMAT)
        b = TEXTURE_NOMIPMAP(width,height, FORMAT)
        self.list = [a,b]
        self.idx = 0

        self.FORMAT = FORMAT
        self.width = width
        self.height = height
    def bind(self):#bind flips first. load last-drawn. ..actually bind to manytimes, flips too much.bad.
        texture = self.list[self.idx]
        texture.bind()#how clever!
    def unbind(self):
        glBindTexture(GL_TEXTURE_2D, 0)
    def update(self,data):# update exactly happend when new idx draw..yeah. it's the point!
        self.flip()
        texture = self.list[self.idx]
        texture.update(data)
    def flip(self):
        self.idx = (self.idx+1)%2






class TEXTURE_NOMIPMAP:
    def __init__(self, width,height, FORMAT = GL_RGB ):
        """format GL_RGB,GL_RGBA,GL_BGR,GL_BGRA"""
        texture = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, texture)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)#GL_NEAREST
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)            
        glTexImage2D(GL_TEXTURE_2D, 0, FORMAT, width, height, 0, FORMAT, GL_UNSIGNED_BYTE, None)#level, border=0
        glBindTexture(GL_TEXTURE_2D, 0)

        self.id = texture
        self.FORMAT = FORMAT
        self.width = width
        self.height = height
    
        #(1080, 1920, 3)
        #height,width,depth = frame.shape
        # if depth == 3:
        #     alpha = (np.ones(height*width,dtype='uint8')*255).reshape(height,width)
        #     frame = np.dstack( [ frame,alpha])    
        #if depth == 3:
            #IMG_MODE = GL_RGB
        #elif depth == 4:
            #IMG_MODE = GL_RGBA

    def update(self,data):
        """data np arr(height,width,depth4)
        NOTE: data will be data.tobyte()ed. if not remain permanent GPU RAM"""
        glBindTexture(GL_TEXTURE_2D, self.id)
        glTexSubImage2D(GL_TEXTURE_2D, 0, 0, 0, self.width, self.height, self.FORMAT, GL_UNSIGNED_BYTE, data.tobytes() )
        glBindTexture(GL_TEXTURE_2D, 0)
        #frame = frame[::-1,:]#reverse ..but slow! ..was not slow! #this remains object texsubiage2d, so ram over!
        #frame = np.flipud(frame) #but this too.
        #frame = frame.tobytes()#this saves old frame, rip..
        #frame = frame.copy() 1vs 0.3 slower. use tobytes.
    def update_ud(self,data):
        """ remember [::-1,:]"""
        glBindTexture(GL_TEXTURE_2D, self.id)
        glTexSubImage2D(GL_TEXTURE_2D, 0, 0, 0, self.width, self.height, self.FORMAT, GL_UNSIGNED_BYTE, data[::-1,:].tobytes() )
        glBindTexture(GL_TEXTURE_2D, 0)
    def bind(self):
        glBindTexture(GL_TEXTURE_2D, self.id)
    def unbind(self):
        glBindTexture(GL_TEXTURE_2D, 0)






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
    def __init__(self,audioname, streaming = False):
        """video requires streaming True."""
        self.source = pyglet.media.load(audioname,streaming=streaming)
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

    def seek_to(self,time):
        maxt = self.source.duration
        mint = 0
        newtime = rangesafe(time, mint, maxt)
        if newtime == maxt:
            newtime-=0.001
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
            #self.pause()not this too. control in video.
            self.seek(val)
            #time.sleep(1)
            #self.play()

            #self.seek_dt(val+0.1) not this
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
        if not audioname in os.listdir():
            clip.audio.write_audiofile(audioname, logger=None)
        clip = None

        self.audio = Audioplayer(audioname,False)

        #use get_data or iter_data (with _pos. get_next_data)
        video = iio.get_reader(videoname)
        size = video.get_meta_data()['size']
        fps = video.get_meta_data()['fps']
        duration = video.get_meta_data()['duration']
        framesa = video.count_frames()
        framesb = duration*fps
        idxmax = int(framesb)-1#why..?
        
        self.video = video
        self.size = size
        self.fps = fps
        self.duration = duration
        self.idxmax = idxmax
        
        self.isplaying = False #means audio plays.
        self.idx = 0
        self.idxlast = 0
        self.idxadder = 0#int
        self.frame = self.video.get_data(0)
        #self.texture =
        height,width,depth = self.frame.shape
        
        #self.texture = TEXTURE_NOMIPMAP(width,height)
        self.texture = TEXTURE_2X(width,height)

        #@self.audio.player.on_player_eos
        #self.audio.player.on_player_eos = ham
        
        #https://www.buzzphp.com/posts/how-to-play-music-continuously-in-pyglet-using-tkinter-at-the-same-time
        @self.audio.player.event
        def on_player_eos():#reach empty playlist.
            #print('nooooooo')
            self.isplaying = False
            #NOT self.stop or kinds.! audio player automatically stops, actually it WAS stoped and event occured.
            #fianally it stops it's end, and do nothing. when we play again, it starts as it is first time.
        #https://pyglet.readthedocs.io/en/latest/modules/media.html

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

    #def set_videotexture(self):
    #    print(self.idx)

    def _update_texture(self,frame):
        frame = frame[::-1,:]#reverse ..but slow! ..was not slow! #this remains object texsubiage2d, so ram over!
        self.texture.update(frame)
    #def _create_texture(self,frame ):#says rgba 20x faster..
    #    #frame = frame[::-1,:]#reverse
    #    width,height,depth = frame.shape
    #    self.texture = TEXTURE_NOMIPMAP(width,height)

    def update(self):
        """idx is frame idx. we get time from audio"""
        if self.isplaying:
            time = self.audio.get_time()
            frameidx = int( time * self.fps )
            self.idx = rangesafe(frameidx,0,self.idxmax)
            #print(self.idx==self.idxmax)#this detects its eos. 10s of True.haha.             
            #if self.idx==self.idxmax:#eos, isplaying off.
                #self.stop()#...but what about audio.. still little remained..?
                #NO, Eos must let be happened by audio player.

        self.idx = rangesafe(self.idx+self.idxadder,0,self.idxmax)
        if not self.idx == self.idxlast:
            self.update_frame()
            #NOTE: even 139max, overs 142 when play,pause fast.
        
    def update_frame(self):
        frameidx = self.idx
        self.idxlast = frameidx
        frame = self.video.get_data(frameidx)
        self.frame = frame
        self._update_texture(frame)
        
        #----get_data, ffmpeg dose..
        #self._skip_frames(index - self._pos - 1)
        #File "C:\Python39\lib\site-packages\imageio\plugins\ffmpeg.py", line 489, in _skip_frames
        #for i in range(n):
    def update_audio(self):
        #print( self.audio.get_time() ,'before')
        self.audio.pause()
        time.sleep(0.05)
        t = self.idx/self.fps
        #print(t,'seek')
        self.audio.seek_to(t)
        time.sleep(0.1)#preventing fast space-key slip.
        #print( self.audio.get_time() ,'after')
        self.audio.play()

    def play_pause(self):
        if self.isplaying:
            self.pause()
        else:
            self.play()
    def play(self):
        #this may not used again.  preventing play while playing av sync problem.
        self.isplaying = True
        #self.audio.play()#play while playing plays through, not play again. time but resets.
        #simple again.
        self.update_audio()

    def pause(self):
        self.isplaying = False
        self.audio.pause()

    def stop(self):#pause and audio seek to 0. for reach eos.
        """hope we  do not use it. this not resets audio. """
        self.isplaying = False
        self.audio.pause()
        self.audio.seek_to(0)

    def seek(self,val):#seems time correct.haha.
        """NOTE: pyglet player timer goes , not from sound. so both play-play or seek whileplaying occurs broken-sync.
        now seek by idx. fine. """

        frames = val*self.fps
        self.idx = int( rangesafe(self.idx+frames, 0, self.idxmax)  )
        
        #seek but when was playing..fine.
        if self.isplaying:
            self.update_audio()

    def seek_frame(self,val):
        self.idx = rangesafe(self.idx+val, 0, self.idxmax)
        print(self.idx)
        if self.isplaying:
            self.update_audio()

    def seek_frame_to(self,val):
        self.idx = rangesafe(val, 0, self.idxmax)
        print(self.idx)
        if self.isplaying:
            self.update_audio()


    
    #def key(self, symbol, modifiers):
    #    self.audio.key(symbol,modifiers)
    def on_key_press(self, symbol, modifiers):
        if symbol == key.P:
            self.play_pause()
        if symbol == key.SPACE:
            self.play_pause()
        if symbol == key.RIGHT:
            val = 1
            if modifiers & key.MOD_SHIFT:
                self.seek_frame(val)
            elif modifiers & key.MOD_CTRL:
                self.idxadder = val
                self.pause()#but not back.its too hard.
                #this is for, while playing, time by player became idx, overrules.
                #temp.pause and play again is too complex, requires another variable. so we didnt.
            else:
                val *= 5
                self.seek(val)
        if symbol == key.LEFT:
            val = -1
            if modifiers & key.MOD_SHIFT:
                self.seek_frame(val)
            elif modifiers & key.MOD_CTRL:
                #self.idxadder = val#actually its too slow.
                #self.pause()
                val *= 1
                self.seek(val)
            else:
                val *= 5
                self.seek(val)
        if symbol == key.UP:
            self.audio.volup(0.1)            
        if symbol == key.DOWN:
            self.audio.voldown(0.1)
        if symbol == key.T:
            t = self.audio.get_time()
            print(t)
        if symbol == key.F:
            print(self.idx)

    def on_key_release(self, symbol, modifiers):
        if symbol == key.RIGHT:
            self.idxadder = 0
            val = 1
            if modifiers & key.MOD_SHIFT:
                1
            elif modifiers & key.MOD_CTRL:
                self.idxadder = 0
        if symbol == key.LEFT:
            self.idxadder = 0
            val = -1
            if modifiers & key.MOD_SHIFT:
                1
            elif modifiers & key.MOD_CTRL:
                self.idxadder = 0

    def ratio_jump(self,ratio):
        newframe = int( self.idxmax * ratio )
        self.seek_frame_to(newframe)
#=============================== PLAYER


if __name__ == '__main__':
    window = pyglet.window.Window()
    window.set_vsync(False)
    
    #pyglet.have_avbin=False
    #pyglet.options['audio'] = ('pulseaudio', 'alsa', 'openal', 'silent') #this sound offs.

    
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
        ('v2f', (0,0, 426,0, 426,240, 0,0, 426,240, 0,240)), #1 for shader, 100~value for pyglet-native
        ('t2f', (0,0, 1,0, 1,1, 0,0, 1,1, 0,1))#for pyglet-native
        #('1g2f', (0,0, 1,0, 1,1, 0,0, 1,1, 0,1)) #for shader avobe.
        )



    
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
        a.on_key_press(symbol,modifiers)

    @window.event
    def on_key_release(symbol, modifiers):
        #sym 48-57 0-9  , 97-122 a-z
        #key no a but A
        #normal 16, shift17, ctrl 18, alt 20
        #MOD normal 24, shift 25, ctrl 26, alt 28.
        # ^^^ if capslocked.hahaha.
        #if symbol == key.W:
        #print(symbol,modifiers)
        #MOD_ALT         Not available on Mac OS X
        #10 & 101 0  if modifiers & MOD_SHIFT:
        a.on_key_release(symbol,modifiers)

    @window.event
    def on_mouse_press(x, y, button, modifiers):
        w,h = window.get_size()
        print(x/w,y/h,button)
        if button == 1:
            a.play_pause()#this brings av err. while playing plays..
        if button == 4:#RIGHT. to SEEK.
            ratio = x/w
            a.ratio_jump(ratio)            
            
        # if button == 2:
        #     a.play_pause()

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
        #glUseProgram(program)

        glEnable(GL_TEXTURE_2D)#for pyglet-native
        #glBindTexture(GL_TEXTURE_2D, a.texture.id)
        #a.set_videotexture()
        a.texture.bind()
        vert_list.draw(pyglet.gl.GL_TRIANGLES)

    #a = Audioplayer('summer.mp3')
    a = Videoplayer('bibitokita.mp4')
    pyglet.app.run()

#next:
# buffer image / mp3 direct ram load pyglet.