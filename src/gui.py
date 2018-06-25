#! coding=utf-8
from tkinter import *
from tkinter.ttk import *
from PIL import ImageTk
from PIL import Image
from keras.preprocessing import image
from keras.applications.vgg19 import VGG19
from keras.applications.vgg19 import preprocess_input
from scipy.spatial.distance import cosine
import os
from os import listdir
import random
import glob
import numpy as np
import returnUserList

win = Tk()
win.geometry('800x600')
# win.resizable(0,0)
win.title("迷惘美")
win.configure(background='gray')
var = StringVar()


### some parameters
count = -1
srcw = 450
srch = 450


### PATHs
seed_path = '../images/seed_pic/'
Seed_pic_feature = '../data/seed_pic.npy'

### global variables
image_list = []
seed_dict = {}
class_dict = {}
y_test = []
x_test = []
model = VGG19(weights='imagenet', include_top=False)

### load seed to random show to the user ###
i=0
for class_name in sorted(os.listdir(seed_path)):
    class_dict[i] = class_name
    seed_dict[i] = []
    for img_path in sorted(os.listdir(seed_path+class_name)):
        if img_path.endswith('.jpg'):
            seed_dict[i].append(os.path.join(seed_path, class_name, img_path))
    i+=1


class Test():
    def __init__(self):

        global label
        welcome_pic = '../images/uriko.jpg'

        self.picA = Image.open(welcome_pic)
        s = self.picA.size
        ratio = 500/max(s[0],s[1])
        self.picA.thumbnail((int(s[0]*ratio),int(s[1]* ratio)),Image.ANTIALIAS)
        self.canvas = Canvas(win, width = 500, height = 500)
        self.img = ImageTk.PhotoImage(self.picA)
        self.imgArea = self.canvas.create_image(0, 0, anchor = 'nw', image = self.img)
        self.canvas.pack()
        self.but1 = Button(win, text=" Start !", command=lambda: self.changeImg())
        self.but1.place(x=10, y=500)

        label = Label(win, text="Welcom to 迷惘美, please press Start ! ")
        label.pack()


    def changeImg(self):
        global count
        global label
        global y_test
        global x_test
        global model
        
        count+=1
        ### after 8 rounds
        if count == 7:
            ### remove the last image if last image was selected 'Dislike' 
            if var.get() == 'Dislike':
                del image_list[-1]
            else:
                pass

            ### extract user images' feature
            for img_path in image_list:
                user_img = image.load_img(img_path,target_size=(224, 224))
                y_test.append(img_path)
                x = image.img_to_array(user_img)
                x = np.expand_dims(x, axis=0)
                if len(x_test) > 0:
                    x_test = np.concatenate((x_test,x))
                else:
                    x_test = x
            # 轉成 VGG 的 input 格式
            x_test = preprocess_input(x_test)
            # 萃取特徵
            features_test = model.predict(x_test)
            self.features_compress_test = features_test.reshape(len(y_test),7*7*512)


            self.canvas.destroy()
            self.but2.destroy()
            self.r1.destroy()
            self.r2.destroy()
            # self.but1.place(x=100, y=500)
            
            ### enter query section
            self.text()
        else:
            if count ==0:
                pass
            else:
                self.r1.destroy()
                self.r2.destroy()
            self.but1.destroy()

            index = random.randint(0,len(seed_dict[count])-1)
            self.picB = seed_dict[count][index]

            ### remove the last image if last image was selected 'Dislike' 
            if var.get() =='Dislike':
                del image_list[-1]
            else:
                pass
            
            image_list.append(self.picB)
            self.picB = Image.open(self.picB)
            s = self.picB.size
            ratio = 500/max(s[0],s[1])
            print(count)
            self.picB.thumbnail((int(s[0]*ratio),int(s[1]* ratio)),Image.ANTIALIAS)
            self.img = ImageTk.PhotoImage(self.picB)
            self.canvas.itemconfig(self.imgArea, image = self.img)
            label.config( text=" Please select Like or Dislike ! ")

            self.r1 = Radiobutton(win, text='Like',
                    variable=var, value='Like',
                    command=print_selection)
            self.r1.pack()
            self.r2 = Radiobutton(win, text='Dislike',
                                variable=var, value='Dislike',
                                command=print_selection)
            self.r2.pack()
            self.but2 = Button(win, text="Next !", command=lambda: self.changeImg())
            self.but2.place(x=10, y=500)

    def text(self):
        global xls_text, userLabel
        userLabel = []
        label = Label(win, text= " 輸入關鍵字：")
        label.pack(side='top')
        xls_text = StringVar(value='query here')
        xls = Entry(win, textvariable = xls_text, width='36')
        # xls_text.set(" ")
        xls.pack()
        self.but3 = Button(win, text="ok !", command=lambda: self.do_queryWord())
        self.but3.place(x=10, y=500)
        self.but3.pack()

        ### load seed_pic feature
        features_compress_seed = np.load(Seed_pic_feature)
        ### 準備計算各類次數
        user_image_class_count = {}
        for i in range(len(class_dict)):
            user_image_class_count[class_dict[i]] = 0
        user_image_class_count['other'] = 0

        # 計算 test image 與 seed pic 的距離
        for i in range(len(y_test)):
            distance = consine_distance(features_compress_seed,self.features_compress_test[i,:])
            # sorted_distance = np.sort(distance)
            top1,top2,top3 = np.argsort(distance)[0:3]

            if distance[top1] > 0.88:
                user_image_class_count['other'] += 1
            else:
                if distance[top3] < 0.89:
                    user_image_class_count[class_dict[top1]] += 3
                    user_image_class_count[class_dict[top2]] += 2
                    user_image_class_count[class_dict[top3]] += 1
                else:
                    if distance[top2] < 0.90:
                        user_image_class_count[class_dict[top1]] += 2
                        user_image_class_count[class_dict[top2]] += 1
                        user_image_class_count['other'] += 1
                    else:
                        user_image_class_count[class_dict[top1]] += 3
                        user_image_class_count['other'] += 1
        print('this user images class distribution: ',user_image_class_count)



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


def print_selection():
    label.config(text='you have selected ' + var.get())

def consine_distance(seed_vector,test_vector):
    dis = np.zeros(sum(len(v)for v in seed_dict.values()))
    index = 0
    for key, value in sorted(seed_dict.items()):
        for i in range(len(value)):
            tmp = cosine(seed_vector[index+i,:], test_vector)
            dis[index+i] = tmp
        index += len(value)
    dis = dis.reshape(8,-1)
    distance = np.mean(dis,axis=1)
    return distance

app = Test()
win.mainloop()