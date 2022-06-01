#move a sprite
# move an Image on the canvas with tkinter
 
import tkinter as tk
 
# Create the window with the Tk class
root = tk.Tk()
 
# Create the canvas and make it visible with pack()
canvas = tk.Canvas(root, width=800, height=800)
canvas.pack() # this makes it visible
 
# Loads and create image (put the image in the folder)
img = tk.PhotoImage(file="mega.png")
image = canvas.create_image(10, 10, anchor=tk.NW, image=img)
x,y=100,100
image = canvas.create_rectangle(
            x-25, y-25, x+25, y+25,
            outline="#fb0",
            fill="#fb0")
 
def move(event):
    """Move the sprite image with a d w and s when click them"""
    if event.char == "a":
        canvas.move(image, -10, 0)
    elif event.char == "d":
        canvas.move(image, 10, 0)
    elif event.char == "w":
        canvas.move(image, 0, -10)
    elif event.char == "s":
        canvas.move(image, 0, 10)
 
# This bind window to keys so that move is called when you press a key
root.bind("<Key>", move)
 
# this creates the loop that makes the window stay 'active'
root.mainloop()
1
2
3
4
5
6
7
8
9
10
11
12
13
14
15
16
17
18
19
20
21
22
23
24
25
26
27
28
29
30
31
32
# move an Image on the canvas with tkinter
 
import tkinter as tk
 
# Create the window with the Tk class
root = tk.Tk()
 
# Create the canvas and make it visible with pack()
canvas = tk.Canvas(root, width=800, height=800)
canvas.pack() # this makes it visible
 
# Loads and create image (put the image in the folder)
img = tk.PhotoImage(file="mega.png")
image = canvas.create_image(10, 10, anchor=tk.NW, image=img)
 
 
def move(event):
    """Move the sprite image with a d w and s when click them"""
    if event.char == "a":
        canvas.move(image, -10, 0)
    elif event.char == "d":
        canvas.move(image, 10, 0)
    elif event.char == "w":
        canvas.move(image, 0, -10)
    elif event.char == "s":
        canvas.move(image, 0, 10)
 
# This bind window to keys so that move is called when you press a key
root.bind("<Key>", move)
 
# this creates the loop that makes the window stay 'active'
root.mainloop()