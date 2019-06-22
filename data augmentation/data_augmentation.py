import random
from scipy import ndarray
import skimage as sk
from skimage import transform
from skimage import util
import matplotlib.pyplot as plt
import numpy as np
import cv2
from PIL import Image

# def random_rotation(image_array: ndarray):
#     # pick a random degree of rotation between 25% on the left and 25% on the right
#     random_degree = random.uniform(-25, 25)
#     return sk.transform.rotate(image_array, random_degree)

# def random_noise(image_array: ndarray):
#     # add random noise to the image
#     return sk.util.random_noise(image_array)


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


image=cv2.imread("IMG_20190510_181157.jpg");
# cv2.imwrite("img_noise.jpg",noisy(image))
# cv2.imwrite("img_flip.jpg",horizontal_flip(image))
cv2.imwrite("img_rot.jpg",rotation(image))


cv2.waitKey(0)