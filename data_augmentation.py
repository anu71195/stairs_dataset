import random
from scipy import ndarray
import skimage as sk
from skimage import transform
from skimage import util
import matplotlib.pyplot as plt
import numpy as np
import cv2
from PIL import Image
import os
from os import walk

def get_file_list(location):
	f = []
	for (dirpath, dirnames, filenames) in walk(location):
	    f.extend(filenames)
	    break
	return f;

def get_dataset(locations):
	file_list=[]
	for i in locations:
		file_list.append(get_file_list(i))
	return file_list

def give_path_to_images(file_list,locations):
	for i in range(len(file_list)):
		for j in range(len(file_list[i])):
			file_list[i][j]=locations[i]+"/"+file_list[i][j]
	return file_list


def augment_data(file_location):
	for i in file_location:
		for j in i:
			image=cv2.imread(j)
			cv2.imwrite("aug_"+j+"_noise",noisy(image))


def rotation(img):
	rows,cols,gar = img.shape
	M = cv2.getRotationMatrix2D((cols/2,rows/2),10,1)
	dst = cv2.warpAffine(img,M,(cols,rows))
	return dst

def noisy(image):  
  row,col,ch= image.shape
  mean = 5
  std =20.0
  return (image + np.random.normal(mean,std,image.shape))
   
def horizontal_flip(image_array: ndarray):
    # horizontal flip doesn't need skimage, it's easy as flipping the image array of pixels !
    return image_array[:, ::-1]

locations=[]
locations.append("dataset/no_stairs")
locations.append("dataset/stairs/down")
locations.append("dataset/stairs/up")

file_list=get_dataset(locations)
file_location=give_path_to_images(file_list,locations)
augment_data(file_location)

# image=cv2.imread("IMG_20190510_181157.jpg");
# cv2.imwrite("img_noise.jpg",noisy(image))
# cv2.imwrite("img_flip.jpg",horizontal_flip(image))
# cv2.imwrite("img_rot.jpg",rotation(image))
