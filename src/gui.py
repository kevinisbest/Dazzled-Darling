#! coding=utf-8
from tkinter import *
from tkinter.ttk import *
from PIL import ImageTk
from PIL import Image
import os
from os import listdir
import random
import glob
import returnUserList

win = Tk()
win.geometry('800x600')
# win.resizable(0,0)
win.title("迷惘美")
win.configure(background='gray')

count = -1
srcw = 450
srch = 450

Dir_path = '/Users/chengho/Dazzled-Darling'

image_list = []
# images = glob.glob('/Users/chengho/Dazzled-Darling/image/*.jpg')
images = glob.glob( Dir_path + '/image/*.jpg')

var = StringVar()

class Test():
    def __init__(self):

        global label
        welcome_pic_path= Dir_path + '/uriko.jpg'

        self.picA = Image.open(welcome_pic_path)
        s = self.picA.size
        print(s)
        ratio = 500/max(s[0],s[1])
        print(ratio)
        self.picA.thumbnail((int(s[0]*ratio),int(s[1]* ratio)),Image.ANTIALIAS)
        self.canvas = Canvas(win, width = 500, height = 500)
        self.img = ImageTk.PhotoImage(self.picA)
        self.imgArea = self.canvas.create_image(0, 0, anchor = 'nw', image = self.img)
        self.canvas.pack()
        self.but1 = Button(win, text=" Next !", command=lambda: self.changeImg())
        self.but1.place(x=10, y=500)

        label = Label(win, text="Welcom to 迷惘美, please select Like or Dislike")
        label.pack()

        global r1, r2

        r1 = Radiobutton(win, text='Like',
                    variable=var, value='Like',
                    command=print_selection)
        r1.pack()
        r2 = Radiobutton(win, text='Dislike',
                            variable=var, value='Dislike',
                            command=print_selection)
        r2.pack()

    def changeImg(self):
        global count
        count+=1
        # self.but1.destroy()
        if count ==7:
            self.canvas.destroy()
            self.but1.destroy()
            # self.but1.place(x=100, y=500)
            r1.destroy()
            r2.destroy()
            self.text()
        else:
            self.picB = random.sample(images, 1)[0]
            image_list.append(self.picB)
            self.picB = Image.open(self.picB)
            # self.picB = self.picB.resize( (srcw, srch), Image.BILINEAR )
            s = self.picB.size
            ratio = 500/max(s[0],s[1])
            print(count)
            self.picB.thumbnail((int(s[0]*ratio),int(s[1]* ratio)),Image.ANTIALIAS)
            self.img = ImageTk.PhotoImage(self.picB)
            self.canvas.itemconfig(self.imgArea, image = self.img)
            # self.but2 = Button(win, text="A !", command=lambda: self.changeImg())
            # self.but2 = Button(win, text="Next !", command=lambda: self.changeImg())
            # self.but2.place(x=10, y=500)
    def text(self):
        print('del')
        global xls_text, userLabel
        userLabel = []
        label = Label(win, text="輸入關鍵字：")
        label.pack(side='top')
        xls_text = StringVar(value='query here')
        xls = Entry(win, textvariable = xls_text, width='36')
        # xls_text.set(" ")
        xls.pack()
        self.but3 = Button(win, text="ok !", command=lambda: self.do_queryWord())
        self.but3.place(x=10, y=500)
        self.but3.pack()

    def do_queryWord(self):
        # print('do_somthing')
        query = xls_text.get()
        print(query)
        ### reset status
        for label in userLabel:
        	label.destroy()
        
        ### print return list
        returnList = returnUserList.main(query)
        for i, user in enumerate(returnList):
        	tmp = Label(win, text=str(i+1) + ': ' + user)
        	tmp.pack()
        	userLabel.append(tmp)



def show():
    global count
    count = count + 1
    panelA = None
    panelB = None
    srcw = 450
    srch = 450
    image_list = []
    images = glob.glob(Dir_path + '/image/*.jpg')
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
        panelA = Label(image = picA,text = 'out')
        panelA.image = picA
        panelA.pack(side = "left" )
        
        panelB = Label(image = picB,text = 'out')
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



# button=tk.Button(win, text="show",command=show)

# button.pack()
app = Test()
win.mainloop()