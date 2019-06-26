from os import walk
from PIL import Image, ExifTags

def get_dataset(locations):
	file_list=[]
	for i in locations:
		file_list.append(get_file_list(i))
	return file_list

def get_file_list(location):
	f = []
	for (dirpath, dirnames, filenames) in walk(location):
	    f.extend(filenames)
	    break
	return f;

def give_path_to_images(file_list,locations):
	for i in range(len(file_list)):
		for j in range(len(file_list[i])):
			file_list[i][j]=locations[i]+"/"+file_list[i][j]
	return file_list


#extracts the gpsinfo from the image by the filename given as the input
def extract_metadata(filename):
	# print(filename)
	#opening the image with the name given by the variable filename
	img = Image.open(filename)

	#reading the metadata
	exif = { ExifTags.TAGS[k]: v for k, v in img._getexif().items() if k in ExifTags.TAGS }
	# print(exif)
	return exif;
	#creating initial empty dictionary
	gpsinfo={}

	#looping over every information given about the gps form the metadata
	for key in exif['GPSInfo'].keys():

		#getting the key from the metadata
		decode = ExifTags.GPSTAGS.get(key,key)

		#storing the data with the key in gpsinfo
		gpsinfo[decode]=exif['GPSInfo'][key]

	#returning the gpsinfo
	return gpsinfo

def get_metadata(file_location):
	metadata={}
	total_files=0;
	counter=0;
	for i in file_location:
		total_files+=len(i)
	for i in file_location:
		for j in i:
			counter+=1;
			if counter%50==0 or counter==total_files:	
				print("                                                                                                ",end="\r")
				print((counter/total_files)*100,"%",end="\r");
			metadata[j]=extract_metadata(j)
	print()
	return metadata


locations=[]
locations.append("dataset/stairs/up")
locations.append("dataset/no_stairs")
locations.append("dataset/stairs/down")

print("gathering image list...\n")
file_list=get_dataset(locations)

print("gathering image locations...\n")
file_location=give_path_to_images(file_list,locations)

metadata=get_metadata(file_location)
# print(metadata)

