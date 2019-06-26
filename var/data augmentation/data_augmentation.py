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

def horizontal_flip(image_array: ndarray):
    # horizontal flip doesn't need skimage, it's easy as flipping the image array of pixels !
    return image_array[:, ::-1]

def gaussian_noisy(image):  
  row,col,ch= image.shape
  mean = 20
  sigma =40**0.5
  noise=np.random.normal(mean,sigma,image.shape)
  print(image)
  print(noise)
  print(image+noise)
  return (image + noise)

def salt_pepper(image):
  row,col,ch = image.shape
  s_vs_p = 0.5
  amount = 0.1
  out = np.copy(image)
  # Salt mode
  num_salt = np.ceil(amount * image.size * s_vs_p)
  coords = [np.random.randint(0, i - 1, int(num_salt))
          for i in image.shape]
  out[coords] = 1

  # Pepper mode
  num_pepper = np.ceil(amount* image.size * (1. - s_vs_p))
  coords = [np.random.randint(0, i - 1, int(num_pepper))
          for i in image.shape]
  out[coords] = 0
  return out

def poisson(image):
    vals = len(np.unique(image))
    vals = 2 ** np.ceil(np.log2(vals))
    noisy = np.random.poisson(image * vals) / float(vals)
    return noisy  

def speckle(image):
  row,col,ch = image.shape
  gauss = np.random.randn(row,col,ch)
  gauss = gauss.reshape(row,col,ch)
  print(gauss)        
  noisy = image + image * gauss
  print(image)
  print(noisy)
  return noisy
   


def plotnoise(img, modei, r, c, i):
    plt.subplot(r,c,i)
    if (modei is not None):
        gimg = util.random_noise(img, mode=modei)
        filename="image"+str(modei)+".jpg"
        print(filename)
        cv2.imwrite(filename,gimg*255)
        plt.imshow(gimg)
    else:
        plt.imshow(img)
    plt.title(modei)
    plt.axis("off")




image=cv2.imread("IMG_20190513_173038_0_rotate.jpg");


img=image

plt.figure(figsize=(18,24))
r=4
c=2
plotnoise(img, "gaussian", r,c,1)
plotnoise(img, "localvar", r,c,2)
plotnoise(img, "poisson", r,c,3)
plotnoise(img, "salt", r,c,4)
plotnoise(img, "pepper", r,c,5)
plotnoise(img, "s&p", r,c,6)
plotnoise(img, "speckle", r,c,7)
plotnoise(img, None, r,c,8)
plt.show()


# noisy_image=speckle(image)
# # print(noisy_image)


# fig=plt.figure(figsize=(1,2))
# fig.add_subplot(1,1,1)
# plt.imshow(image)


# cv2.imwrite("img_noise.jpg",noisy_image)
# image=cv2.imread("img_noise.jpg")
# # print(image)
# fig.add_subplot(1,2,2)
# plt.imshow(noisy_image)
# plt.show()
# # cv2.imwrite("img_noise.jpg",noisy(image))
# # cv2.imwrite("img_flip.jpg",horizontal_flip(image))



# cv2.waitKey(0)