from keras.applications.vgg19 import VGG19
from keras.preprocessing import image
from keras.applications.vgg19 import preprocess_input, decode_predictions
import numpy as np
import os
import sys
from scipy.spatial.distance import cosine
import scipy
from PIL import ImageFile
ImageFile.LOAD_TRUNCATED_IMAGES = True
from tqdm import tqdm

# image_path = '/Users/kevin_mbp/Desktop/image/user_images/'
# output_path = '/Users/kevin_mbp/Desktop/test_dir/output/'
# seed_path = '/Users/kevin_mbp/Desktop/test_dir/seed_pic/'

image_path = '/media/Data/IR2018/IG_pic/'
seed_path = '/home/mirlab/IR2018/seed_pic/'
output_path = '/home/mirlab/IR2018/image_user_output/'

# image_path = './image/'
# output_path = './output'
# seed_path = './seed_pic/'

seed_pic_dict = {}

# 計算相似矩陣
def cosine_similarity(ratings):
    sim = ratings.dot(ratings.T)
    if not isinstance(sim, np.ndarray):
        sim = sim.toarray()
    norms = np.array([np.sqrt(np.diagonal(sim))])
    return (sim / norms / norms.T)
def consine_distance(seed_vector,test_vector):
    dis = np.zeros(sum(len(v)for v in seed_pic_dict.values()))
    index = 0
    for key, value in sorted(seed_pic_dict.items()):
        for i in range(len(value)):
            tmp = cosine(seed_vector[index+i,:], test_vector)
            dis[index+i] = tmp
        index += len(value)
    dis = dis.reshape(8,-1)
    distance = np.mean(dis,axis=1)
    return distance
def main():

    # 讀取 seed pics
    seed_pic = []
    class_dict = {}
    i=0
    for class_name in sorted(os.listdir(seed_path)):
        print('now is :',class_name)
        class_dict[i] = class_name

        for img_path in sorted(os.listdir(seed_path+class_name)):
            if img_path.endswith('.jpg'):
                try:
                    seed_pic_dict[i]
                except :
                    seed_pic_dict[i] = [str(img_path)]
                else:
                    seed_pic_dict[i].append(str(img_path))
                img = image.load_img(seed_path+class_name+'/'+img_path, target_size=(224, 224))
                x = image.img_to_array(img)
                x = np.expand_dims(x, axis=0)
                if len(seed_pic)>0:
                    seed_pic = np.concatenate((seed_pic,x))
                else:
                    seed_pic = x
        i+=1
    seed_pic = preprocess_input(seed_pic)

    # include_top=False，表示會載入 VGG19 的模型，不包括加在最後3層的卷積層，通常是取得 Features (1,7,7,512)
    model = VGG19(weights='imagenet', include_top=False) 

    # 萃取特徵
    features_seed = model.predict(seed_pic)
    features_compress_seed = features_seed.reshape(len(seed_pic),7*7*512)

    # 自user目錄找出所有 JPEG 檔案    
    for user_name in sorted(os.listdir(image_path)):
        y_test=[]
        x_test=[]
        print('now is ',user_name)
        for img_path in sorted(os.listdir(image_path+user_name)):
            # print(img_path)
            if img_path.endswith(".jpg"):
                try:
                    img = image.load_img(os.path.join(image_path, user_name,img_path),target_size=(224, 224))
                except:
                    print('Bad pic: ',os.path.join(image_path, user_name,img_path))
                else:

                    # img = image.load_img(image_path+'/'+user_name+'/'+img_path, target_size=(224, 224))
                    y_test.append(img_path)
                    x = image.img_to_array(img)
                    x = np.expand_dims(x, axis=0)
                    if len(x_test) > 0:
                        x_test = np.concatenate((x_test,x))
                    else:
                        x_test=x
        
        # 轉成 VGG 的 input 格式
        x_test = preprocess_input(x_test)
        # 萃取特徵
        features_test = model.predict(x_test)
        features_compress_test = features_test.reshape(len(y_test),7*7*512)

        # 準備計算各類次數
        user_image_class_count = {}
        for i in range(len(class_dict)):
            user_image_class_count[class_dict[i]] = 0
        user_image_class_count['other'] = 0

        # 計算 test image 與 seed pic 的距離
        for i in range(len(y_test)):
            distance = consine_distance(features_compress_seed,features_compress_test[i,:])
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

        # print('this user images class distribution: ',user_image_class_count)
        f = open(output_path+'output_new_policy3.txt','a')
        f.write(user_name+' :\n')
        f.write(str(user_image_class_count))
        f.write('\n')
        f.close()

        # user vector



if __name__ == "__main__":
    main()