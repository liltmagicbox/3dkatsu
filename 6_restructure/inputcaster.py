class InputCaster:
    def __init__(self):
        self.list = []
        self.targets = []
    def bind(self, inputdevice):
        """def bind_callback in inputdevice."""
        inputdevice.bind_callback(self)
        #self.dict = inputdevice.keymap
        self.targets.append(inputdevice)
    def input(self, abskey, value, name,UUID):
        e = (abskey, value, name,UUID)
        self.list.append(e)
        # if abskey == 'F' and value == 1:
        #     print('ff')
        #     self.dict[abskey]()

    def cast(self):
        for target in self.targets:
            keys = list(target.keymap)
            for i in self.list:
                abskey = i[0]
                if abskey in keys:
                    funcs = target.keymap.get(abskey)
                    funcs()
                    #if hasattr(target, funcs):
                    #    func = getattr(target, funcs)
                    #    func()
        #print('cast: ',i)
        self.list=[]












#==============================================

#more abskeys for glfw:
"""
M_BUTTON_
M_SCROLL
CURSOR_POS
CURSOR_ENTER
FILEDROP
WINDOW_POS
"""

map_mods = {
    0: "",
    1: "SHIFT",
    2: "CTRL",
    4: "ALT",
    
    3: "CTRL+SHIFT",
    5: "ALT+SHIFT",
    6: "CTRL+ALT",
    7: "CTRL+ALT+SHIFT",
    8: "SUPER",#not that want..
}

map_mouse = {
    0: "M_LEFT",
    1: "M_RIGHT",
    2: "M_MIDDLE",
}

map_keyboard = {
32 : "SPACE" ,
39 : "'"  ,     #/* ' */,
44 : ","  ,     #/* , */,
45 : "-"  ,     #/* - */,
46 : "."  ,     #/* . */,
47 : "/"  ,     #/* / */,
48 : "0" ,
49 : "1" ,
50 : "2" ,
51 : "3" ,
52 : "4" ,
53 : "5" ,
54 : "6" ,
55 : "7" ,
56 : "8" ,
57 : "9" ,
59 : ";"  ,     #/* ; */,
61 : "="  ,     #/* = */,
65 : "A" ,
66 : "B" ,
67 : "C" ,
68 : "D" ,
69 : "E" ,
70 : "F" ,
71 : "G" ,
72 : "H" ,
73 : "I" ,
74 : "J" ,
75 : "K" ,
76 : "L" ,
77 : "M" ,
78 : "N" ,
79 : "O" ,
80 : "P" ,
81 : "Q" ,
82 : "R" ,
83 : "S" ,
84 : "T" ,
85 : "U" ,
86 : "V" ,
87 : "W" ,
88 : "X" ,
89 : "Y" ,
90 : "Z" ,
91 : "["  ,
92 : "BACKSLASH"  ,     #/* \ */,
93 : "]"  ,
96 : "`"  ,
161 : "WORLD1"  ,     #/* non-US #1 */,
162 : "WORLD2"  ,     #/* non-US #2 */,
256 : "ESCAPE" ,
257 : "ENTER" ,
258 : "TAB" ,
259 : "BACKSPACE" ,
260 : "INSERT" ,
261 : "DELETE" ,

262 : "RIGHT" ,
263 : "LEFT" ,
264 : "DOWN" ,
265 : "UP" ,

266 : "PAGEUP" ,
267 : "PAGEDOWN" ,
268 : "HOME" ,
269 : "END" ,
280 : "CAPSLOCK" ,
281 : "SCROLLLOCK" ,
282 : "NUMLOCK" ,
283 : "PRINTSCREEN" ,
284 : "PAUSE" ,

290 : "F1" ,
291 : "F2" ,
292 : "F3" ,
293 : "F4" ,
294 : "F5" ,
295 : "F6" ,
296 : "F7" ,
297 : "F8" ,
298 : "F9" ,
299 : "F10" ,
300 : "F11" ,
301 : "F12" ,
302 : "F13" ,
303 : "F14" ,
304 : "F15" ,
305 : "F16" ,
306 : "F17" ,
307 : "F18" ,
308 : "F19" ,
309 : "F20" ,
310 : "F21" ,
311 : "F22" ,
312 : "F23" ,
313 : "F24" ,
314 : "F25" ,

320 : "NUM0" ,
321 : "NUM1" ,
322 : "NUM2" ,
323 : "NUM3" ,
324 : "NUM4" ,
325 : "NUM5" ,
326 : "NUM6" ,
327 : "NUM7" ,
328 : "NUM8" ,
329 : "NUM9" ,
330 : "NUM." ,
331 : "NUM/" ,
332 : "NUM*" ,
333 : "NUM-" ,
334 : "NUM+" ,
335 : "NUMENTER" ,
336 : "NUM=" ,

340 : "SHIFT" ,
341 : "CTRL" ,
342 : "ALT" ,
343 : "SUPER" ,

344 : "RIGHTSHIFT" ,
345 : "RIGHTCONTROL" ,
346 : "RIGHTALT" ,
347 : "RIGHTSUPER" ,
348 : "MENU" ,
}
