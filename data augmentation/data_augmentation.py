import random
from scipy import ndarray
import skimage as sk
from skimage import transform
from skimage import util
import matplotlib.pyplot as plt
import numpy as np
import cv2
from PIL import Image
import matplotlib 
from matplotlib import pyplot as plt


def rotation(img):
	rows,cols,gar = img.shape
	M = cv2.getRotationMatrix2D((cols/2,rows/2),10,1)
	dst = cv2.warpAffine(img,M,(cols,rows))
	return dst

def noisy(image):  
  row,col,ch= image.shape
  mean = 20
  sigma =40**0.5
  noise=np.random.normal(mean,sigma,image.shape)
  print(image)
  print(noise)
  print(image+noise)
  return (image + noise)
   
def horizontal_flip(image_array: ndarray):
    # horizontal flip doesn't need skimage, it's easy as flipping the image array of pixels !
    return image_array[:, ::-1]


image=cv2.imread("IMG_20190510_181157.jpg");
noisy_image=noisy(image)
print(noisy_image)


fig=plt.figure(figsize=(1,2))
fig.add_subplot(1,1,1)
plt.imshow(image)


cv2.imwrite("img_noise.jpg",noisy_image)
image=cv2.imread("img_noise.jpg")
print(image)
fig.add_subplot(1,2,2)
plt.imshow(image)
plt.show()
# cv2.imwrite("img_noise.jpg",noisy(image))
# cv2.imwrite("img_flip.jpg",horizontal_flip(image))



cv2.waitKey(0)