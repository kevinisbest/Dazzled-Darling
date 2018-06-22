from tkinter import *
from tkinter import ttk
from PIL import ImageTk
from PIL import Image
import os
from os import listdir
import random
import glob
win=Tk()
win.geometry('1000x600')
win.resizable(0,0)
win.title("IR ttk GUI")
label=Label(win, text="Hello World!")
count=0

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

    if panelA is None or panelB is None:
        panelA = Label(image = picA,text = 'out')
        panelA.image = picA
        panelA.pack(side = "left", )
        
        # while the second panel will store the edge map
        panelB = Label(image = picB,text = 'out')
        panelB.image = picB
        panelB.pack(side = "right")
        
    # otherwise, update the image panels
    else:
        # update the pannels
        panelA.configure(image = picA)
        panelA.image = picA
        panelB.configure(image = picB)
        panelB.image = picB

button=Button(win, text="OK",command=show)
label.pack()
button.pack()
win.mainloop()