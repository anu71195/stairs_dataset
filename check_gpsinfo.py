import os
from os import walk
from PIL import Image, ExifTags
import numpy as np

def get_direction_number(direction):
	if(direction=='E'):
		return 0;
	elif(direction=='W'):
		return 1;
	elif(direction=='N'):
		return 2;
	elif(direction=='S'):
		return 3;

def get_file_list(location):
	f = []
	for (dirpath, dirnames, filenames) in walk(location):
	    f.extend(filenames)
	    break
	return f;

def extract_metadata(filename):
	print(filename)
	#opening the image with the name given by the variable filename
	img = Image.open(filename)

	#reading the metadata
	exif = { ExifTags.TAGS[k]: v for k, v in img._getexif().items() if k in ExifTags.TAGS }

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

def get_gps_features(gpsinfo):
	features=np.array([]);
	features=np.append(features,gpsinfo['GPSAltitude'][0]/gpsinfo['GPSAltitude'][1])
	features[-1]=features[-1]/1000;
	latitude=((gpsinfo['GPSLatitude'][0][0]/gpsinfo['GPSLatitude'][0][1])+(gpsinfo['GPSLatitude'][1][0]/(gpsinfo['GPSLatitude'][1][1]*60))+(gpsinfo['GPSLatitude'][2][0]/(gpsinfo['GPSLatitude'][2][1]*3600)))
	features=np.append(features,latitude)
	features[-1]=features[-1]/90;
	longitude=((gpsinfo['GPSLongitude'][0][0]/gpsinfo['GPSLongitude'][0][1])+(gpsinfo['GPSLongitude'][1][0]/(gpsinfo['GPSLongitude'][1][1]*60))+(gpsinfo['GPSLongitude'][2][0]/(gpsinfo['GPSLongitude'][2][1]*3600)))
	features=np.append(features,longitude)
	features[-1]=features[-1]/180;
	features=np.append(features,gpsinfo['GPSImgDirection'][0]/gpsinfo['GPSImgDirection'][1])
	features[-1]=features[-1]/360;
	features=np.append(features,get_direction_number(gpsinfo['GPSLatitudeRef']))
	features[-1]=features[-1]/4;
	features=np.append(features,get_direction_number(gpsinfo['GPSLongitudeRef']))
	features[-1]=features[-1]/4;
	return features



def check(file_list,location):
	wrong_files=[]
	for name in file_list:
		file_name=location+'/'+name;
		gpsinfo=extract_metadata(file_name)
		try:
			gps_features=get_gps_features(gpsinfo);
		except:
			wrong_files.append(file_name)
			os.remove(file_name)
			print("-------------------")

	return wrong_files


directory="no_stairs";
stairs_train_location=directory+"/training/stairs"
no_stairs_train_location=directory+"/training/no_stairs"
stairs_test_location=directory+"/testing/stairs"
no_stairs_test_location=directory+"/testing/no_stairs"

file_list=get_file_list(directory)
wrong_files=(check(file_list,directory))

print(wrong_files)
print(len(wrong_files))

# file_list=get_file_list(no_stairs_train_location)
# check(file_list,no_stairs_train_location)

# file_list=get_file_list(stairs_test_location)
# check(file_list,stairs_test_location)

# file_list=get_file_list(no_stairs_test_location)
# check(file_list,no_stairs_test_location)