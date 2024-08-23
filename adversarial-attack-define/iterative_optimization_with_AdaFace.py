import argparse
from absl import app, flags, logging
from absl.flags import FLAGS
import cv2
import os
import numpy as np
import tensorflow as tf
import random
import matplotlib.pyplot as plt
import time
from tensorflow.keras.models import load_model
from sklearn.preprocessing import normalize
from sys import exit
import os.path
from os import path
import pathlib


def l2_norm(x, axis=1):
    """l2 norm"""
    norm = np.linalg.norm(x, axis=axis, keepdims=True)
    output = x / norm

    return output


def preprocessing_and_normalization(img):
    
    mean = 0.5
    std = 0.5
    img = tf.keras.preprocessing.image.img_to_array(img)
    bgr_img = ((img[:,:,::-1] / 255.) - mean) / std   # img[:,:,::-1] is turning RGB to BGR, the rest is min max normalization
    bgr_img = np.expand_dims(bgr_img, axis=0)
    return bgr_img   

def Get_images_array(img_folder, mode):
    
    arr = [] 

    folders = os.listdir(img_folder)   

    j = 0
    for dirl in os.listdir(img_folder): 
        i = 0
        print('======================================='+str(dirl)+'========================================')
        arr.append([])
        for file in os.listdir(os.path.join(img_folder,dirl)):

            if any([file.endswith(x) for x in ['.jpeg', '.jpg', '.png']]):                    
                image_path=os.path.join(img_folder,dirl,file)
                arr[j].append(image_path)                
                
            i += 1
        j += 1
    return arr

parser = argparse.ArgumentParser(description='Generating adversarial attacks')

parser.add_argument('--input', '-im',
                    dest="input",
                    type=str,
                    help='dir of the directory where are all images')
                    


parser.add_argument('--output', '-om',
                    dest="output",
                    type=str,
                    help='dir of the directory where will be saved all features')

args= parser.parse_args()

model = load_model('adaface_ir101_webface12m_rgb.h5') #load weights on local

image_arr = Get_images_array(args.input,1)

counter_img_per_identity = 0

counter_total_img = 0

processing = 0

for i in range (len(image_arr)): 

    for j in range(0,len(image_arr[i])): 

        counter_img_per_identity+=1

        print("Number of img per identity {}".format(counter_img_per_identity))

        sample_name = image_arr[i][j].split('\\')[-1].split('.jpg')[0]

        identity = image_arr[i][j].split('\\')[-2]

        path_save_folder = os.path.join(args.output,identity)

        path_feat = os.path.join(path_save_folder,sample_name+'.npy')

        file = pathlib.Path(path_feat)

        if  file.exists (): 

            print("File exist {}".format(str(path_feat)))

            pass

        else:

            print("File was not!")

            processing +=1

            print("Processing {}".format(processing))

            img2 = tf.keras.preprocessing.image.load_img(image_arr[i][j], target_size=(112, 112))

            img2 = preprocessing_and_normalization(img2)

            image2 = tf.Variable(img2) 

            with tf.GradientTape() as gtape:

                embeds2 = l2_norm(model(image2))

                emb_conv = np.array(embeds2)

                if not os.path.isdir(path_save_folder):

                    os.makedirs(path_save_folder,exist_ok=True)

                np.save(path_feat,emb_conv)





