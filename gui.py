from tkinter import *
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import ImageTk
from PIL import Image
import os
from os import listdir
import random
import glob


def helloCallBack():
   messagebox.showinfo( "Hello Python", "Hello World")
 
def show():
    panelA = None
    panelB = None
    srcw = 450
    srch = 450
    image_list = []
    images = glob.glob('/Users/kevin_mbp/Desktop/IG/image/*.jpg')

    for i in range(3):
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
        panelA.pack(side = "right", padx=10, pady=10)
        
        # while the second panel will store the edge map
        panelB = Label(image = picB,text = 'out')
        panelB.image = picB
        panelB.pack(side = "right", padx=10, pady=10)
        
    # otherwise, update the image panels
    else:
        # update the pannels
        panelA.configure(image = picA)
        panelA.image = picA
        panelB.configure(image = picB)
        panelB.image = picB

def main():
    window = tk.Tk()
    window.title("IR")
    window.geometry('1080x720')
    btn_select_image = Button(window, text="hit me",activeforeground = 'red', command = show)
    btn_select_image.pack(side = "top", fill = "both", expand = "yes", padx = "10", pady = "10")
    window.mainloop()

if __name__ == '__main__':
    main()