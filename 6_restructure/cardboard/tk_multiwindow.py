from tkinter import *
from tkinter import ttk

class MainWindow(Tk):
    #https://www.pythontutorial.net/tkinter/tkinter-toplevel/
    def __init__(self):
        super().__init__()
        self.geometry("640x480+300+300")
        self.title('Main Window')

        def open_window():
            window = SubWindow(self)
            #window.grab_set()#this holds all inputs.
        ttk.Button(self,
                text='Open a window',
                command=open_window).pack(expand=True)

class SubWindow(Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.geometry("200x100")
        self.title('Sub Window')

        ttk.Button(self,
                text='Close',
                command=self.destroy).pack(expand=True)

m=MainWindow()
m.mainloop()