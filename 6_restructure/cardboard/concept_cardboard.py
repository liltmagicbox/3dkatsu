import time

class EventHolder:
    def __init__(self):
        self._events = []
        self._t0 = time.time()
    def flush(self):
        events = self._events
        self._events = []
        return events
    def push(self, event):
        self._events.append(event)

class Event:
    def __init__(self):
        self._time = time.time()
    #===api
    @property
    def time(self):
        return self._time

# class Event:
# _button
# _state
# _coordinates
class KeyEvent(Event):
    def __init__(self, key,state,coords):
        self._key = key
        self._state = state
        self._coords = coords
    #===api



#===================================================

class Card_basic:
    #def __init__(self, width=100,height=100):
    def __init__(self, size):
        #self._width =width
        #self._height =height
        self._size = size
        
        self._image = None
        self._color = '#fb0'
    #===api
    # @property
    # def width(self):
    #     return self._width
    # @property
    # def height(self):
    #     return self._height
    @property
    def size(self):
        return self._size
        #return self._width,self._height

    @property
    def color(self):
        return self._color
    @color.setter
    def color(self,value):
        self._color = value
    #-----------
    def set_image(self, imgdir):
        self._image = imgdir


class Card_board(Card_basic):
    def __init__(self, pos=(0,0), size=(50,50) ):
        #x,y = pos
        self._pos = pos
        #width,height = size
        #super().__init__(width,height)
        super().__init__(size)
        #self._x = x
        #self._y = y
        self._floating=False        
    #===api
    # @property
    # def x(self):
    #     return self._x
    # @property
    # def y(self):
    #     return self._y
    # @x.setter
    # def x(self,value):
    #     self._x = value
    # @y.setter
    # def y(self,value):
    #     self._y = value
    @property
    def pos(self):
        return self._pos
        #return (self._x,self._y)
    @pos.setter
    def pos(self,value):
        #x,y = value
        #self._x,self._y = x,y
        self._pos = value

    def lift(self):
        self._floating=True
    def land(self):
        self._floating=False
    # def move(self,x,y):
    #     self._x = x
    #     self._y = y
    def hit_test(self, hx,hy):
        x,y = self.pos
        w,h = self.size
        w,h = int(w/2),int(h/2)
        if x-w <= hx <= x+w and y-h <= hy <= y+h:
            return True
        return False

class Card_tk(Card_board):
    def draw(self,canvas):
        x,y = self.pos
        w,h = self.size
        w,h = int(w/2),int(h/2)
        
        rectangle = canvas.create_rectangle(
            x-w, y-h, x+w, y+h,
            outline="#fb0",
            fill = self.color)

        text = canvas.create_text((x,y), text="Label tea\nfasdfxt")        
        #bbox = canvas.bbox(text)#(-17, 43, 37, 58)
        #print(bbox)
        # rectangle=canvas.create_rectangle(x-w, y-h, x+w, y+h,
        #     outline="yellow",
        #     fill="white", width=1)
        
        #parent.create_image(10, 10, anchor=tk.NW, image=img)
        self.canvas = canvas
        self.rectangle = rectangle
        self.text = text
    
    # @color.setter
    # def color(self,value):
    #     self._color = value
    #     self.canvas.itemconfig(self.rectangle, fill='cyan')
    #     #self.canvas.itemconfig(self.rectangle, outline='red')
    
    # @property
    # def pos(self):
    #     return (self._x,self._y)
    # @pos.setter
    # def pos(self,value):
    #     x,y = value
    #     self._x,self._y = x,y
    
    #print(super(Card_board))
    #@super.pos.setter
    # @Card_board.pos.setter
    # def pos(self, value):
    #     self._pos = value
    #     #print(value)
    #     #Card_board.pos(value) not for instanced!
    #     x0, y0, x1, y1 = self.canvas.coords(self.rectangle)
    #     x,y = value
    #     x0+=x
    #     y0+=y
    #     x1+=x
    #     y1+=y
    #     self.canvas.coords(self.rectangle, x0, y0, x1, y1)


    def lift(self):
        super().lift()
        self.canvas.itemconfig(self.rectangle, outline='red')
    def land(self):
        super().land()
        self.canvas.itemconfig(self.rectangle, outline='yellow')
    # def move(self,x,y):
    #     super().move(x,y)
    #     self.canvas.itemconfig(self.rectangle, outline='yellow')

Card = Card_tk

class ItemHolder:
    def __init__(self):
        self._items = []
    def add(self, item):
        self._items.append(item)
    @property
    def items(self):
        return self._items

class Board_tk(ItemHolder):
    def __init__(self):
        super().__init__()
        self.color = 'green'
        self._grabbing=None
    
    def bind(self, parent):
        self.canvas = Canvas(parent, bg=self.color)
        self.canvas.pack(side=RIGHT, fill=BOTH, expand=YES)
        initx,inity = 50,50
        for item in self.items:
            if item.pos == (0,0):
                item.pos = initx,inity
                initx,inity = initx+50,inity+10
            item.draw(self.canvas)

        self.bind_callback()

    def grab(self,item):
        item.lift()
        self._grabbing=item
    
    def bind_callback(self):
        
        def callback_press(event):
            for item in reversed(self.items):
                if item.hit_test(event.x,event.y):
                    self.grab(item)
                    break
        def callback_rel(event):
            if self._grabbing:
                item = self._grabbing
                item.land()
            self._grabbing = None

        def callback_m(event):
            if self._grabbing:
                item = self._grabbing
                x,y = event.x,event.y
                item.pos = x,y

                w,h = item.size
                ww,hh = int(w/2),int(h/2)
                x0, y0, x1, y1 = self.canvas.coords(item.rectangle)
                x0=x-ww
                y0=y-hh
                x1=x+ww
                y1=y+hh
                self.canvas.coords(item.rectangle, x0, y0, x1, y1)
                #self.canvas.coords(item.text, 200,200)
                self.canvas.coords(item.text, x,y)
                


        #self.canvas.bind("<Button-1>", callback)
        #<ButtonPress event state=Mod1 num=2 x=205 y=181>
        #<ButtonPress event state=Shift|Control|Mod1 num=3 x=234 y=261>
        #self.canvas.bind("<Button>", callback)
        self.canvas.bind("<ButtonPress>", callback_press)
        self.canvas.bind("<ButtonRelease>", callback_rel)
        self.canvas.bind("<Motion>", callback_m)


from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import os
from textframe import TextFrame

class Window(Tk):
    #https://www.pythontutorial.net/tkinter/tkinter-toplevel/
    def __init__(self):
        super().__init__()
        self.geometry("640x480+100+300")
        self.title('Main Window')        
    def bind(self):
        self.bind_textf()
        self.bind_menu()
        self.bind_board()

    def bind_board(self):
        b=Board_tk()
        for i in range(5):
            c=Card()
            b.add(c)
        b.bind(self)
        self.board = b

    def bind_textf(self):
        textf = TextFrame(self,LEFT)
        self.textf = textf

    def bind_menu(self):
        textf = self.textf
        menu = Menu(self)
        self.config(menu=menu)
        def callback_save(e=None):
            fdir = filedialog.asksaveasfilename(
                initialdir = os.getcwd(),
                title = "save",
                filetypes = ( ("txt file", "*.txt"),("all files", "*.*") )
                )
            textf.save(fdir)
        def callback_open(e=None):
            fdir = filedialog.askopenfilename(
                initialdir = os.getcwd(),
                title = "open",
                filetypes = ( ("txt file", "*.txt"),("all files", "*.*") )
                )
            textf.load(fdir)

        filemenu = Menu(menu)
        menu.add_cascade(label="File", menu=filemenu, underline=0)
        filemenu.add_command(label="Open", command=callback_open, underline=0)
        filemenu.add_command(label="Save", command=callback_save, underline=0)
        filemenu.add_separator()


w=Window()
w.bind()
w.mainloop()