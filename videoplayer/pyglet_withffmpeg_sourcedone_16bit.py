#https://gist.github.com/akey7/94ff0b4a4caf70b98f0135c1cd79aff3
#https://python-sounddevice.readthedocs.io/en/0.3.10/


import numpy as np
# Samples per second
sps = 44100
# Frequency / pitch
freq_hz = 440.0
# Duration
duration_s = 2.0
# Attenuation so the sound is reasonable
atten = 0.3
# NumpPy magic to calculate the waveform
each_sample_number = np.arange(duration_s * sps)
waveform = np.sin(2 * np.pi * each_sample_number * freq_hz / sps)
waveform *= atten




import pyglet
print(pyglet.media.codecs.have_ffmpeg(),'ffmpeg')

#data = ((waveform+1)*128).astype('uint8')

data = ((waveform+1)*16384).astype('uint16')#.tobytes() #16384 is magic number
#4096*2*2 16384  == 2^14

#audio_format = pyglet.media.sources.base.AudioFormat( 2,16,44100 ) #oldver
audio_format = pyglet.media.codecs.base.AudioFormat( 1,16,44100 )

#sss = pyglet.media.codecs.base.StaticMemorySource(data,audio_format)
#this not creates self._data. see base.py

sss = pyglet.media.codecs.base.StaticMemorySource(data,audio_format)
#we now input manuaaly!hahah
sss._data = data
sss._duration = len(sss._data) / sss.audio_format.bytes_per_second
sss.play() #behold, hear the sin wave..

#source = pyglet.media.load('sound.mp3',streaming=False)
#vsource = pyglet.media.load("spe.mp4" ,streaming=True)




#1.stream mp4 (read vid, updates texture-that'sthe problem)
#2. stream mp4 vid=None, (but still reads mp4, but not texture update maybe)
#3. static mp3 from mp4. read full vid, 60MB/s 5seconds 300MB. slow.

print('loading')
filename = "bibitokita.mp4"
#s1 = pyglet.media.codecs.wmf.WMFSource(filename,None) #before-ff.
s1 = pyglet.media.load(filename ,streaming=True)
s1.video_format = None

s2 = pyglet.media.codecs.StaticSource(s1) #this 60MB/s 5seconds for 300MBmp4
s2.play()

#s1.play() #this 2mb/s interval 5s. 4mb/10s.. 0.4MB/s.


#works great
#test:
#from pyglet.media.codecs import ffmpeg_lib
#we set all avutil kinds dll in py37 dir.
#no.err.
