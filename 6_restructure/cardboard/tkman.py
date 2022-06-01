#import tkinter as tk
from tkinter import *
from tkinter import filedialog

import os

root = Tk()
root.geometry("640x480+300+300")
root.title('text board')
#root.resizable(False,False)


menu = Menu(root)
root.config(menu=menu)

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
#filemenu.add_command(label="Exit", command=callback)



root.bind('<Control-s>', callback_save)
root.bind('<Control-o>', callback_open)


class TextFrame:
    def __init__(self, root, side):
        self.frame = Frame(root)#width,
        self.text = Text(root, height = 50, width = 30)
        #self.button = Button(self.frame, text = "Save", )
        self.pack(side)
    def pack(self, side):
        self.frame.pack( side = side )#expand=NO, fill=NONE)
        self.text.pack(side = side)

    def save(self,fdir):
        if fdir=='':
            return
        textline = self.text.get(1.0, END)
        splited_lines = textline.splitlines(True)

        fullstring = ''.join(textline)
        with open(fdir, 'w' , encoding = 'utf-8') as f:
            f.write(fullstring)

    def load(self,fdir):
        if fdir=='':
            return
        self.text.delete( 1.0, END)
        with open(fdir, 'r', encoding='utf-8') as f:
            textline = f.read()
            if textline.endswith('\n'):
                textline=textline[:-1]
        self.text.insert(END, textline)

"""
#Board
#  boxs=[]
#    press(x,y):None
#    unpress(x,y):None
보드
보드에 마우스입력가능
박스생성가능
마우스입력이 박스에 맞으면 박스를 이동모드로
미우스 이동시 박스를 해당위치까지 이동.
#떼면 ㅇ이도옴드중지.
"""

class Box:
    def __init__(self, parent, x,y):
        self.x = x
        self.y = y
        self.width = 100
        self.height = 100
        self.rect = parent.create_rectangle(
            x-25, y-25, x+25, y+25,
            outline="#fb0",
            fill="#fb0")
        #canvas.move(rect,0,10)
        # self.canvas = Canvas(
        #     parent,
        #     width=self.width,
        #     height=self.height,
        #     bg='red')

        #img = tk.PhotoImage(file="mega.png")
        #image = canvas.create_image(10, 10, anchor=tk.NW, image=img)

    def movement(self):
        self.canvas.move(self.rectangle, self.x, self.y)
        self.canvas.after(100, self.movement)

        #self.canvas.place(relx=0.0, rely=1.0, anchor=SW)
        #self.canvas.place(x=30, y=50)
        self.pack()
    def pack(self):
        self.canvas.pack()



class Board:
    def __init__(self, root, side):
        self.frame = Frame(root)#width,
        self.canvas = Canvas(self.frame, bg='green')
        #self.canvas = Canvas(self.frame, width=400, height=500, bg='red')
        
        def callback(event):
            #print ("clicked at", event.x, event.y)
            x,y = event.x, event.y
            b = Box(self.canvas,x,y)
            self.rects.append(b)

        def callback_m(event):
            for rect in self.rects:
                self.canvas.move(rect.rect,0,10)

        def callback2(event):
            print(self.rects)
            #<ButtonPress event state=Mod1 num=2 x=205 y=181>
            for rect in self.rects:
                self.canvas.move(rect.rect,10,10)
        self.canvas.bind("<Button-1>", callback)
        self.canvas.bind("<Button-2>", callback2)
        self.canvas.bind("<Motion>", callback_m)
        self.rects=[]

        #canvas.configure(bg='cyan')
        #self.button = Button(self.frame, text = "Save", bg='blue')
        self.pack(side)
    def pack(self, side):
        self.frame.pack(side=side, fill=BOTH, expand=YES)
        self.canvas.pack(side=LEFT, fill=BOTH, expand=YES)#expand=NO, fill=NONE)
        #self.button.pack(side = side)


textf = TextFrame(root, LEFT)
boxf = Board(root, RIGHT)
root.mainloop()
exit()





# Create text widget and specify size.
T = Text(root, height = 5, width = 52)
 
# Create label
l = Label(root, text = "Fact of the Day")
l.config(font =("Courier", 14))
 
Fact = """A man can be arrested in
Italy for wearing a skirt in public."""


# Create button for next text.
b1 = Button(root, text = "Save", )
 
# Create an Exit button.
b2 = Button(root, text = "Exit",
            command = root.destroy)
 
l.pack()
T.pack()
b1.pack()
b2.pack()
 
# Insert The Fact.
T.insert(END, Fact)
