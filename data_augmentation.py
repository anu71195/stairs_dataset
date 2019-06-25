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
import shutil
from os import walk
import matplotlib
from matplotlib import pyplot as plt


def check_create_directory(directories,new_dataset_preposition):
	for directory_loc in directories:
		directory_loc=directory_loc.split("/")
		directory=new_dataset_preposition
		for loc_part in directory_loc:
			directory=directory +(loc_part+"/")
			print(directory)
			if not os.path.exists(directory):
				os.makedirs(directory)

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

def give_path_to_images(file_list,locations,new_dataset_preposition,clear_augment_dataset):
	if clear_augment_dataset:
		try:
			shutil.rmtree(new_dataset_preposition+"dataset")
		except:
			pass
	check_create_directory(locations,new_dataset_preposition)

	for i in range(len(file_list)):
		for j in range(len(file_list[i])):
			file_list[i][j]=locations[i]+"/"+file_list[i][j]
	return file_list


def augment_data_1(file_location,new_dataset_preposition,min_degree,max_degree,mean_array,std_array,noises):
	max_degree+=1;#in python the maxima is open bound not close bound so adding 1 to max degree
	for i in file_location:
		for j in i:
			print(j)
			image=cv2.imread(j)

			for degrees in range(min_degree,max_degree):
				new_j=new_dataset_preposition+j.split(".")[0]+"_"+str(degrees)+"_rotate.jpg"
				print(new_j)
				cv2.imwrite(new_j,rotation(image,degrees))

			flip_image=horizontal_flip(image)
			for degrees in range(min_degree,max_degree):
				new_j=new_dataset_preposition+j.split(".")[0]+"_flip_"+str(degrees)+"_rotate.jpg"
				print(new_j)
				cv2.imwrite(new_j,rotation(flip_image,degrees))

			for noise in noises:
				print(noise)
				if(noise=="gaussian"):	
					for mean in mean_array:
						for std in std_array:

							noisy_image=gaussian(image,mean,std)
							for degrees in range(min_degree,max_degree):
								new_j=new_dataset_preposition+j.split(".")[0]+"_"+str(mean)+"_"+str(std)+"_"+noise+"_noise_"+str(degrees)+"_rotate.jpg"
								print(new_j)
								cv2.imwrite(new_j,rotation(noisy_image,degrees))


							flip_image=horizontal_flip(noisy_image)
							for degrees in range(min_degree,max_degree):
								new_j=new_dataset_preposition+j.split(".")[0]+"_"+str(mean)+"_"+str(std)+"_"+noise+"_noise_flip_"+str(degrees)+"_rotate.jpg"
								print(new_j)
								cv2.imwrite(new_j,rotation(flip_image,degrees))

				elif(noise=="s&p"):					
					noisy_image=salt_pepper(image)
					for degrees in range(min_degree,max_degree):
						new_j=new_dataset_preposition+j.split(".")[0]+"_"+noise+"_noise_"+str(degrees)+"_rotate.jpg"
						print(new_j)
						cv2.imwrite(new_j,rotation(noisy_image,degrees))


					flip_image=horizontal_flip(noisy_image)
					for degrees in range(min_degree,max_degree):
						new_j=new_dataset_preposition+j.split(".")[0]+"_"+noise+"_noise_flip_"+str(degrees)+"_rotate.jpg"
						print(new_j)
						cv2.imwrite(new_j,rotation(flip_image,degrees))
					  
				elif(noise=="poisson"):
					pass;
				elif(noise=="speckle"):
					pass;


def rotation(img,degrees):
	rows,cols,gar = img.shape
	M = cv2.getRotationMatrix2D((cols/2,rows/2),degrees,1)
	dst = cv2.warpAffine(img,M,(cols,rows))
	return dst

def gaussian(image,mean,var):  
  row,col,ch= image.shape
  print(mean,var)
  return (image + np.random.normal(mean,var,image.shape))

def salt_pepper(image):
  row,col,ch = image.shape
  s_vs_p = 0.5
  amount = 0.1
  # Salt mode
  num_salt = np.ceil(amount * image.size * s_vs_p)
  coords = [np.random.randint(0, i - 1, int(num_salt))
          for i in image.shape]
  image[coords] = 1

  # Pepper mode
  num_pepper = np.ceil(amount* image.size * (1. - s_vs_p))
  coords = [np.random.randint(0, i - 1, int(num_pepper))
          for i in image.shape]
  image[coords] = 0
  return image
   
def horizontal_flip(image_array: ndarray):
    # horizontal flip doesn't need skimage, it's easy as flipping the image array of pixels !
    return image_array[:, ::-1]




def augment_data(file_location,new_dataset_preposition,min_degree,max_degree,mean_array,std_array,noises):
	max_degree+=1;#in python the maxima is open bound not close bound so adding 1 to max degree
	fig=plt.figure(figsize=(18,24))
	counter=1
	for i in file_location:
		for j in i:
			print(j)
			image=(cv2.imread(j))/255.0

			for degrees in range(min_degree,max_degree):
				new_j=new_dataset_preposition+j.split(".")[0]+"_"+str(degrees)+"_rotate.jpg"
				print(new_j)
				rotated_image=rotation(image,degrees)
				cv2.imwrite(new_j,rotated_image*255.0)
				plt.subplot(4,2,counter)
				plt.imshow(rotated_image)
				counter+=1

			flip_image=horizontal_flip(image)
			for degrees in range(min_degree,max_degree):
				new_j=new_dataset_preposition+j.split(".")[0]+"_flip_"+str(degrees)+"_rotate.jpg"
				print(new_j)
				rotated_image=rotation(flip_image,degrees)
				cv2.imwrite(new_j,rotated_image*255.0)


			for noise in noises:
				noisy_image = util.random_noise(image, mode=noise)
				for degrees in range(min_degree,max_degree):
					new_j=new_dataset_preposition+j.split(".")[0]+"_"+noise+"_noise_"+str(degrees)+"_rotate.jpg"
					print(new_j)
					rotated_image=rotation(noisy_image,degrees)
					cv2.imwrite(new_j,rotated_image*255.0)
					plt.subplot(4,2,counter)
					plt.imshow(rotated_image)
					counter+=1


				flip_image=horizontal_flip(noisy_image)
				for degrees in range(min_degree,max_degree):
					new_j=new_dataset_preposition+j.split(".")[0]+"_"+noise+"_noise_flip_"+str(degrees)+"_rotate.jpg"
					print(new_j)
					rotated_image=rotation(flip_image,degrees)
					cv2.imwrite(new_j,rotated_image*255.0)


			plt.show()
			exit()
















#it is expected that no changes in the directory names are made in the dataset including the directory dataset




new_dataset_preposition="augmented_"
noises=["gaussian","localvar","s&p","poisson","speckle","salt","pepper"]
clear_augment_dataset=1;
min_degree=-0
max_degree=0
mean_array=np.arange(-3,4,3)
std_array=np.arange(80,126,15)

locations=[]
locations.append("dataset/stairs/up")
locations.append("dataset/no_stairs")
locations.append("dataset/stairs/down")

print("gathering image list...\n")
file_list=get_dataset(locations)

print("gathering image locations...\n")
file_location=give_path_to_images(file_list,locations,new_dataset_preposition,clear_augment_dataset)

print("augmenting data....\n")
augment_data(file_location,new_dataset_preposition,min_degree,max_degree,mean_array,std_array,noises)

