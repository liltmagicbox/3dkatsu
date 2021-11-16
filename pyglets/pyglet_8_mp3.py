from pyglet.gl import *
#https://pyglet.readthedocs.io/en/latest/programming_guide/graphics.html

from pyglet.graphics import vertex_list, vertex_list_indexed, Batch
#pyglet.graphics.vertex_list

from pyglet.window import key

window = pyglet.window.Window()



source = pyglet.media.load('fla.mp3',streaming=True)
#player.queue(source)
player = pyglet.media.Player()

source2 = pyglet.media.load('pya.mp3')

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
        nplayer = pyglet.media.Player()
        nplayer.queue(source2)
        print('ccc')
        nplayer.seek(0)
        nplayer.play()
        nplayer.delete()
        #now we got instant effect player lol

#while pressing madly 48MB to 46MB idle.
#never changes if delete.
            
#maybe directmedia.kinds.. anyway no memory added.
##    if symbol == key.D:
##        for i in range(1000):
##            nplayer = pyglet.media.Player()
##            nplayer.queue(source2)
##        print('huh')
        

@window.event
def on_draw():
    glClear(GL_COLOR_BUFFER_BIT)
    

pyglet.app.run()



"""
AudioFormat(channels=2, sample_size=16, sample_rate=48000)

>>> cc=source.get_audio_data(10)
>>> cc
<pyglet.media.codecs.base.AudioData object at 0x000001BE630F7A90>
>>> cc.data
<ctypes.c_char_Array_43968 object at 0x000001BE630FFA40>
>>> cc.length
43968
>>> cc.timestamp
0.0
>>> cc.duration
0.916
>>> cc.get_string_data()


d[:100]
b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x0
>>> cc.data[0]
b'\x00'
>>> cc.data[-100]
b'\xff'

b'\xff'.decode()
... not utf-8..

see
https://docs.python.org/ko/3/howto/unicode.html
but not well.
i think  x00 means 0x00 , 0, xff means 255.



>>> cc=source.get_audio_data(2)
>>> len(cc.data)
46080
>>> cc=source.get_audio_data(1)
>>> len(cc.data)
46080
>>> cc=source.get_audio_data(0)


for i in cc.data:
	if not i in d:
		d.append(i)

>>> d.sort()
>>> d
[b'\x00', b'\x01', b'\x02', b'\x03', b'\x04', b'\x05', b'\x06', b'\x07', b'\x08',
 b'\t', b'\n', b'\x0b', b'\x0c', b'\r', b'\x0e', b'\x0f',
 b'\x10', b'\x11', b'\x12', b'\x13', b'\x14', b'\x15', b'\x16', b'\x17', b'\x18',
 b'\x19',
 b'\x1a', b'\x1b', b'\x1c', b'\x1d', b'\x1e', b'\x1f',
 b' ', b'!', b'"', b'#', b'$', b'%', b'&', b"'", b'(', b')', b'*', b'+', b',',
 b'-', b'.', b'/',

 b'0', b'1', b'2', b'3', b'4', b'5', b'6', b'7', b'8', b'9',
 b':', b';', b'<', b'=', b'>', b'?', b'@',

 b'A', b'B', b'C', b'D', b'E', b'F', b'G', b'H', b'I', b'J', b'K', b'L', b'M', b'N',
 b'O', b'P', b'Q', b'R', b'S', b'T', b'U', b'V', b'W', b'X', b'Y', b'Z',

 b'[', b'\\', b']', b'^', b'_', b'`', b'a', b'b', b'c', b'd', b'e', b'f',
 b'g', b'h', b'i', b'j', b'k', b'l', b'm', b'n', b'o', b'p', b'q', b'r',
 b's', b't', b'u', b'v', b'w', b'x', b'y', b'z', b'{', b'|', b'}', b'~',
 b'\x7f', b'\x80', b'\x81', b'\x82', b'\x83', b'\x84', b'\x85', b'\x86', b'\x87', b'\x88', b'\x89', b'\x8a', b'\x8b', b'\x8c', b'\x8d', b'\x8e', b'\x8f', b'\x90', b'\x91', b'\x92', b'\x93', b'\x94', b'\x95', b'\x96', b'\x97', b'\x98', b'\x99', b'\x9a', b'\x9b', b'\x9c', b'\x9d', b'\x9e', b'\x9f', b'\xa0', b'\xa1', b'\xa2', b'\xa3', b'\xa4', b'\xa5', b'\xa6', b'\xa7', b'\xa8', b'\xa9', b'\xaa', b'\xab', b'\xac', b'\xad', b'\xae', b'\xaf', b'\xb0', b'\xb1', b'\xb2', b'\xb3', b'\xb4', b'\xb5', b'\xb6', b'\xb7', b'\xb8', b'\xb9', b'\xba', b'\xbb', b'\xbc', b'\xbd', b'\xbe', b'\xbf', b'\xc0', b'\xc1', b'\xc2', b'\xc3', b'\xc4', b'\xc5', b'\xc6', b'\xc7', b'\xc8', b'\xc9', b'\xca', b'\xcb', b'\xcc', b'\xcd', b'\xce', b'\xcf', b'\xd0', b'\xd1', b'\xd2', b'\xd3', b'\xd4', b'\xd5', b'\xd6', b'\xd7', b'\xd8', b'\xd9', b'\xda', b'\xdb', b'\xdc', b'\xdd', b'\xde', b'\xdf', b'\xe0', b'\xe1', b'\xe2', b'\xe3', b'\xe4', b'\xe5', b'\xe6', b'\xe7', b'\xe8', b'\xe9', b'\xea', b'\xeb', b'\xec', b'\xed', b'\xee', b'\xef', b'\xf0', b'\xf1', b'\xf2', b'\xf3', b'\xf4', b'\xf5', b'\xf6', b'\xf7', b'\xf8', b'\xf9', b'\xfa', b'\xfb', b'\xfc', b'\xfd', b'\xfe', b'\xff']
	    
..surely 0-255value. fine.
but why.
16bit stereo 48000..?

"""
