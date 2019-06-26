import random
from scipy import ndarray
import skimage as sk
from skimage import transform,util
import matplotlib.pyplot as plt
import numpy as np
import cv2
import os
import shutil
from os import walk
import matplotlib
from matplotlib import pyplot as plt
from PIL import Image, ExifTags
import piexif
import pickle
import time
import math

def check_create_directory(directories,new_dataset_preposition):#for given argument directories a list of directory.... all the non-existential directories are created
	for directory_loc in directories:
		directory_loc=directory_loc.split("/")
		directory=new_dataset_preposition
		for loc_part in directory_loc:
			directory=directory +(loc_part+"/")
			print("creating " +directory)
			if not os.path.exists(directory):
				os.makedirs(directory)

def get_file_list(location):#collect all the file names from the given location/directory
	f = []
	for (dirpath, dirnames, filenames) in walk(location):
	    f.extend(filenames)
	    break
	return f;

def get_dataset(locations):#collect all the file names from each location/directory from the list of location given as an argument
	file_list=[]
	for i in locations:
		file_list.append(get_file_list(i))
	return file_list

def give_path_to_images(file_list,locations,new_dataset_preposition,clear_augment_dataset):#catenate the string file name with its path and deleting the older augmented dataset directories if clear_augment_dataset is set to true
	if clear_augment_dataset:
		try:
			print("Emptying "+new_dataset_preposition+"dataset...\n")
			shutil.rmtree(new_dataset_preposition+"dataset")
		except:
			pass
	check_create_directory(locations,new_dataset_preposition)

	for i in range(len(file_list)):
		for j in range(len(file_list[i])):
			file_list[i][j]=locations[i]+"/"+file_list[i][j]
	return file_list



#right not augment_data is used instead of this function, the function is incomplete but s&p and guassian noises code is added where its different parameters likemean and variance for gaussian and 
#s&p ratio and amount parameters can be manipulated
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
					noisy_image=salt_pepper(image,0.5,0.1)
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


def rotation(img,degrees):#rotating the given image with the degrees given as an argument
	rows,cols,gar = img.shape
	M = cv2.getRotationMatrix2D((cols/2,rows/2),degrees,1)
	dst = cv2.warpAffine(img,M,(cols,rows))
	return dst

def gaussian(image,mean,var):  #adding gaussian noise to the image with given parameter mean and var
  row,col,ch= image.shape
  print(mean,var)
  return (image + np.random.normal(mean,var,image.shape))

def salt_pepper(image,s_vs_p,amount):#adding salt_pepper noise to the image
  row,col,ch = image.shape

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


#extracts the gpsinfo from the image by the filename given as the input
def extract_metadata(filename):
	# print(filename)
	#opening the image with the name given by the variable filename
	img = Image.open(filename)

	#reading the metadata
	exif = { ExifTags.TAGS[k]: v for k, v in img._getexif().items() if k in ExifTags.TAGS }
	return exif;
	print(exif)
	# return exif;
	#creating initial empty dictionary
	gpsinfo={}

	#looping over every information given about the gps form the metadata
	for key in exif['GPSInfo'].keys():

		#getting the key from the metadata
		decode = ExifTags.GPSTAGS.get(key,key)

		#storing the data with the key in gpsinfo
		gpsinfo[decode]=exif['GPSInfo'][key]

	print(gpsinfo)
	#returning the gpsinfo
	return gpsinfo



def image_resize(image, width = None, height = None, inter = cv2.INTER_AREA):
    # initialize the dimensions of the image to be resized and
    # grab the image size
    dim = None
    (h, w) = image.shape[:2]

    # if both the width and height are None, then return the
    # original image
    if width is None and height is None:
        return image

    # check to see if the width is None
    if width is None:
        # calculate the ratio of the height and construct the
        # dimensions
        r = height / float(h)
        dim = (int(w * r), height)

    # otherwise, the height is None
    else:
        # calculate the ratio of the width and construct the
        # dimensions
        r = width / float(w)
        dim = (width, int(h * r))
    dim=(width,height);
    # resize the image
    resized = cv2.resize(image, dim, interpolation = inter)  
    
    #returning the resized image
    return resized

def add_metadata(exiff,filename):#this function seems not working so instead the metadata is stored in a dictionary which iis stored in a pickle file
	print(exiff)
	img=Image.open(filename)
	img.save("augmented_dataset/no_stairs/final.png",exif=piexif.dump(exiff))

def save_image_fit_resolution(image,location):##expects floating valued image and save the image as seen by the cv2.imshow 
	plt.imshow(image)
	plt.axis('off')
	plt.savefig(location,bbox_inches='tight',pad_inches = 0)

def save_image_same_resolution(image,location):##expects floating valued image and save the image the same resolution given by the image which is the parameters to this function
	cv2.imwrite(location,image*255)

def augment_data(file_location,new_dataset_preposition,degree_range,noises,width=None,height=None):#all the augmentation is done in this function
	metadata={}
	total_files=0;
	counter=0;#keep track of number of files created

	#getting total number of files
	for i in file_location:
		total_files=total_files+len(i)
	print("Number of files=",total_files,"\n")

	#getting total number of files which will be created
	total_images_created=total_files*2*len(degree_range)*(len(noises)+1)
	print("number of files that will be created=",total_images_created,"\n")
	estd_time=time.time()

	for i in file_location:
		for j in i:

			image=(cv2.imread(j))/255.0
			if(width!=None and height!=None):
				image=image_resize(image,width,height)
			exif=extract_metadata(j)#extrcting metadata from the file given by name stored in j
			#normal image for every degree mentioned in degree_range one image will be created 
			for degrees in degree_range:
				counter+=1;
				if(counter%5==0 or counter==total_images_created):
					current_time=time.time()-estd_time
					print("                                                    ",end="\r")
					print((counter/total_images_created)*100,"% \tEstimated time = ",math.floor((current_time*(total_images_created-counter))/counter )," seconds",end="\r");
				new_j=new_dataset_preposition+j.split(".")[0]+"_"+str(degrees)+"_rotate.jpg"
				# print(new_j)
				rotated_image=rotation(image,degrees)
				save_image_same_resolution(rotated_image,new_j)
				metadata[new_j]=exif;

			#flipped image of normal image 
			flip_image=horizontal_flip(image)
			#flipped image of normal image image for every degree mentioned in degree_ranged one image will be created
			for degrees in degree_range:
				counter+=1;
				if(counter%5==0 or counter==total_images_created):
					current_time=time.time()-estd_time
					print("                                                    ",end="\r")
					print((counter/total_images_created)*100,"% \tEstimated time = ",math.floor((current_time*(total_images_created-counter))/counter)," seconds",end="\r");
				new_j=new_dataset_preposition+j.split(".")[0]+"_flip_"+str(degrees)+"_rotate.jpg"
				# print(new_j)
				rotated_image=rotation(flip_image,degrees)
				save_image_same_resolution(rotated_image,new_j)
				metadata[new_j]=exif;


			#for every noise mentioned in noises for image and fliped image for every degree mentioned in degree_ranged one image will be created
			for noise in noises:
				noisy_image = util.random_noise(image, mode=noise)
				for degrees in degree_range:
					counter+=1;
					if(counter%5==0 or counter==total_images_created):
						current_time=time.time()-estd_time
						print("                                                    ",end="\r")
						print((counter/total_images_created)*100,"% \tEstimated time = ",math.floor((current_time*(total_images_created-counter))/counter)," seconds",end="\r");
					new_j=new_dataset_preposition+j.split(".")[0]+"_"+noise+"_noise_"+str(degrees)+"_rotate.jpeg"
					# print(new_j)
					rotated_image=rotation(noisy_image,degrees)
					save_image_same_resolution(rotated_image,new_j)
					metadata[new_j]=exif;



				flip_image=horizontal_flip(noisy_image)
				for degrees in degree_range:
					counter+=1;
					if(counter%5==0 or counter==total_images_created):
						current_time=time.time()-estd_time
						print("                                                    ",end="\r")
						print((counter/total_images_created)*100,"% \tEstimated time = ",math.floor((current_time*(total_images_created-counter))/counter)," seconds",end="\r");
					new_j=new_dataset_preposition+j.split(".")[0]+"_"+noise+"_noise_flip_"+str(degrees)+"_rotate.jpg"
					# print(new_j)
					rotated_image=rotation(flip_image,degrees)
					save_image_same_resolution(rotated_image,new_j)
					metadata[new_j]=exif;
	fp=open("metadata.pkl","wb")
	pickle.dump(metadata, fp, pickle.HIGHEST_PROTOCOL)






#save_image_fit_resolution is slover than save_image_same_resolution
#it is expected that no changes in the directory names are made in the dataset including the directory dataset



total_time=time.time()
width=640
height=640
new_dataset_preposition="augmented_"
noises=["gaussian","localvar","s&p","poisson","speckle","salt","pepper"]
clear_augment_dataset=0;#setting this true will delete all the previous augmented data if created
degree_range=np.arange(-10,+11,5)#rotations in augmented data varies form -10 to 10 in an interval of 5
mean_array=np.arange(-3,4,3)#mean array ranges from -3 to 3 in an interval of 3
std_array=np.arange(80,126,15)#std array ranges from 80 to 125 in an interval of 15

#all locations where dataset is present
locations=[]
locations.append("dataset/no_stairs")
# locations.append("dataset/stairs/up")
# locations.append("dataset/stairs/down")

print("gathering image list...\n")
#collect all the file names from each location/directory from the list of location given as an argument
file_list=get_dataset(locations)

print("gathering image locations...\n")
#catenate the string file name with its path and deleting the older augmented dataset directories if clear_augment_dataset is set to true
file_location=give_path_to_images(file_list,locations,new_dataset_preposition,clear_augment_dataset)

augment_time=time.time()
print("\naugmenting data....\n")
augment_data(file_location,new_dataset_preposition,degree_range,noises,width,height)#all the augmentation is done in this function
print("\n\n\ntime to augment data=",time.time()-augment_time)
print("total time taken=",time.time()-total_time)

