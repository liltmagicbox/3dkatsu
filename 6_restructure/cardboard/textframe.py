
from tkinter import *
from tkinter import ttk

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