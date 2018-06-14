from keras.applications.vgg19 import VGG19
from keras.preprocessing import image
from keras.applications.vgg19 import preprocess_input, decode_predictions
import numpy as np
import os
import sys
from scipy.spatial.distance import cosine
import scipy

image_path = '/Users/kevin_mbp/Desktop/image/'
output_path = '/Users/kevin_mbp/Desktop/test_dir/output'
seed_path = '/Users/kevin_mbp/Desktop/test_dir/seed_pic/'

# 計算相似矩陣
def cosine_similarity(ratings):
    sim = ratings.dot(ratings.T)
    if not isinstance(sim, np.ndarray):
        sim = sim.toarray()
    norms = np.array([np.sqrt(np.diagonal(sim))])
    return (sim / norms / norms.T)
def consine_distance(seed_vector,test_vector):
    dis = np.zeros(80)
    for i in range(8):
        index_max = (i+1)*10-1
        for j in range(index_max-9,index_max+1,1):
            print(j)
            tmp = cosine(seed_vector[j,:],test_vector)
            dis[j] = tmp
    dis = dis.reshape(8,10)
    distance = np.mean(dis,axis=1)
    # for i in range(a):
    #     for j in range(a):
    #         distance[i,j] = cosine(u[i,:],v[j,:])
    return distance
def main():
    # 自 images 目錄找出所有 JPEG 檔案    
    y_test=[]
    x_test=[]
    seed_pic=[]
    for class_name in sorted(os.listdir(seed_path)):
        print('now is :',class_name)
        for img_path in sorted(os.listdir(seed_path+class_name)):
            if img_path.endswith('.jpg'):
                img = image.load_img(seed_path+class_name+'/'+img_path, target_size=(224, 224))
                x = image.img_to_array(img)
                x = np.expand_dims(x, axis=0)
                if len(seed_pic)>0:
                    seed_pic = np.concatenate((seed_pic,x))
                else:
                    seed_pic = x

    seed_pic = preprocess_input(seed_pic)

    for img_path in sorted(os.listdir(image_path)):
        # print(img_path)
        if img_path.endswith(".jpg"):
            img = image.load_img(image_path+img_path, target_size=(224, 224))
            y_test.append(img_path)
            x = image.img_to_array(img)
            x = np.expand_dims(x, axis=0)
            if len(x_test) > 0:
                x_test = np.concatenate((x_test,x))
            else:
                x_test=x
    
    # 轉成 VGG 的 input 格式
    x_test = preprocess_input(x_test)

    # include_top=False，表示會載入 VGG19 的模型，不包括加在最後3層的卷積層，通常是取得 Features (1,7,7,512)
    model = VGG19(weights='imagenet', include_top=False) 


    # 萃取特徵
    features_seed = model.predict(seed_pic)
    features_test = model.predict(x_test)
    # print(features_test.shape)
    # print(features_seed.shape)
    # features_total = np.concatenate((features_test,features_seed))
    # print(features_total.shape)
    # 計算相似矩陣
    
    features_compress_seed = features_seed.reshape(len(seed_pic),7*7*512)
    features_compress_test = features_test.reshape(len(y_test),7*7*512)

    # sim = cosine_similarity(features_compress)
    for i in range(len(y_test)):
        distance = consine_distance(features_compress_seed,features_compress_test[i,:])
        print(distance)
    # print(sim)
    # print(distance)
    # 依命令行參數，取1個樣本測試測試
    # inputNo = 1 # tiger, np.random.randint(0,len(y_test),1)[0]
    # top = np.argsort(-sim, axis=1)[:,0:5]
    # print(top)
    # top = np.argsort(distance, axis=1)[:,0:5]
    # print(top)
    # print(len(x_test),len(y_test))
    # 取得最相似的前3名序號
    # recommend = [y_test[i] for i in top]
    # print(recommend)

if __name__ == "__main__":
    main()