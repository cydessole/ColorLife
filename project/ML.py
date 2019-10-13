import os
from math import ceil,floor,log
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image
from keras.models import load_model
from keras.preprocessing.image import array_to_img, img_to_array, load_img
from skimage.color import rgb2lab, lab2rgb, rgb2gray, xyz2lab
from skimage.io import imsave
from skimage.transform import  resize
from keras import backend as K
import tensorflow as tf


def closest_power(x):
    up=abs(np.power(2,ceil(log(x,2)))-x)
    down=abs(np.power(2,floor(log(x,2)))-x)
    if up==min(down,up) and up!=down :
        value= np.power(2,ceil(log(x,2)))
    else:
        value= np.power(2,floor(log(x,2)))
    if value >256 :
        return 256
    else :
        return value

def closest_power_abs(x):
    up=abs(np.power(2,ceil(log(x,2)))-x)
    down=abs(np.power(2,floor(log(x,2)))-x)
    if up==min(down,up) and up!=down :
        value= np.power(2,ceil(log(x,2)))
    else:
        value= np.power(2,floor(log(x,2)))
    return value

def model_predict(Photo,model,graph):
    im = Image.open(Photo)
    width, height = im.size
    width_2=closest_power_abs(width)
    height_2=closest_power_abs(height)
    print(width_2,height_2)
    color_me=[]
    color_me.append(img_to_array(load_img(Photo,target_size=(width_2,height_2))))
    color_me = np.array(color_me, dtype=float)
    color_me = rgb2lab(1.0/255*color_me)[:,:,:,0]
    color_me = color_me.reshape(color_me.shape+(1,))
    with graph.as_default():
        output = model.predict(color_me)
        output = output * 128
        for i in range(len(output)):
            cur = np.zeros((width_2, height_2, 3))
            cur[:,:,0] = color_me[i][:,:,0]
            cur[:,:,1:] = output[i]
            cur=resize(cur,(height,width))
            Photo_color=lab2rgb(cur)
            return Photo_color
