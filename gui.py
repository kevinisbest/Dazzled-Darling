from tkinter import ttk
from PIL import ImageTk
from PIL import Image
import tkinter as tk
import os
from os import listdir
import random
import glob
win=tk.Tk()
win.geometry('1000x600')
# win.resizable(0,0)
win.title("IR ttk GUI")
label=tk.Label(win, text="Hello World!")
label.pack()
count=0
srcw = 450
srch = 450

image_list = []
images = glob.glob('/Users/kevin_mbp/Desktop/IG/image/*.jpg')

var = tk.StringVar()

class Test():
    def __init__(self):

        self.picA = random.sample(images, 1)[0]
        
        image_list.append(self.picA)
        self.picA = Image.open(self.picA)
        self.picA = self.picA.resize( (srcw, srch), Image.BILINEAR )

        self.canvas = tk.Canvas(win, width = 800, height = 480)
        self.img = ImageTk.PhotoImage(self.picA)
        self.imgArea = self.canvas.create_image(0, 0, anchor = 'nw', image = self.img)
        self.canvas.pack()
        self.but1 = tk.Button(win, text="press me", command=lambda: self.changeImg())
        self.but1.place(x=10, y=500)
    def changeImg(self):
        self.picB = random.sample(images, 1)[0]
        image_list.append(self.picB)
        self.picB = Image.open(self.picB)
        self.picB = self.picB.resize( (srcw, srch), Image.BILINEAR )
        self.img = ImageTk.PhotoImage(self.picB)
        self.canvas.itemconfig(self.imgArea, image = self.img)
        self.but2 = tk.Button(win, text="press me", command=lambda: self.changeImg())
        self.but2.place(x=10, y=500)


def show():
    global count
    count = count + 1
    panelA = None
    panelB = None
    srcw = 450
    srch = 450
    image_list = []
    images = glob.glob('/Users/kevin_mbp/Desktop/IG/image/*.jpg')
    label.config(text = 'count '+str(count))
    
    picA = random.sample(images, 1)[0]
    image_list.append(picA)
    picB = random.sample(images, 1)[0]
    image_list.append(picB)

    picA = Image.open(picA)
    picB = Image.open(picB)
    
    # print('image size:',edged.size)
    picA = picA.resize( (srcw, srch), Image.BILINEAR )
    picA = ImageTk.PhotoImage(picA)

    picB = picB.resize( (srcw, srch), Image.BILINEAR )
    picB = ImageTk.PhotoImage(picB)

    if panelA is None and panelB is None:
        panelA = tk.Label(image = picA,text = 'out')
        panelA.image = picA
        panelA.pack(side = "left" )
        
        panelB = tk.Label(image = picB,text = 'out')
        panelB.image = picB
        panelB.pack(side = "right")
        
    # otherwise, update the image panels
    else:
        # update the pannels
        panelA.configure(image = picA)
        panelA.image = picA
        panelA.pack(side = "left" )
        panelB.configure(image = picB)
        panelB.image = picB
        panelB.pack(side = "right")

def update_image():
    global tkimg1
    tkimg1 = ImageTk.PhotoImage(Image.open('temp.png'))
    label.config( image = tkimg1)
    label.after(1000, update_image)
    print ("Updated")
def print_selection():
    label.config(text='you have selected ' + var.get())

r1 = tk.Radiobutton(win, text='Left',
                    variable=var, value='A',
                    command=print_selection)
r1.pack()
r2 = tk.Radiobutton(win, text='Right',
                    variable=var, value='B',
                    command=print_selection)
r2.pack()

# button=tk.Button(win, text="show",command=show)

# button.pack()
app = Test()
win.mainloop()