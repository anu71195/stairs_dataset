# Staircase Dataset

Dataset is provided in the directory "dataset" which contains two subdirectories stairs and no_stairs and further stairs contains two more subdirectories namely "up" and "down" for up and down staircases respectively

## Files

### check_gpsinfo.py

* *locations*:-Empty it (if needed) and add the path/location of all the directory which you want to check the whether it has gps info or metadata 

* *delete_files_without_metadata*:-If set the files which are without gpsinfo or without metadata will be deleted

* **check**:-It checks whether the image has metadata or gps info. It takes two parameters one is *delete_files_without_metadata* and other is derives from the variables *locations*

### data_augmentation.py

* *new_dataset_preposition*:-By default it is set to "augmented_" that means augmented dataset created will have name as "augmented_dataset" changing that will change the preposition before dataset

* *noises*:-list of noises which will be generated. Remove the noises from the list which are unwanted

* *clear_augment_dataset*:-Setting this true will delete all the previously generated augmented dataset (if created)

* *degree_range*:-rotated images and original images will have angles before them with values in this list. (a,b+1,c) is the format it follow meaning between a and b in the interval of c(see the comment in the code).

* *locations*:-Empty it (if needed) and add the path/location of all the directory which you want to check the whether it has gps info or metadata 

* *width*:-gives the width to the newly image created. If width or height any of them are None them original size will be used. Also note smaller size gives faster augmentation.

* *height*:-gives the height to the newly image created. If width or height any of them are None them original size will be used. Also note smaller size gives faster augmentation.

* **augment_data**:- It will do all the augmentation of data. all the params are mentioned above. It has by default "metadata.pkl" as name for the metadata file which wil be created. It can be changed manually.

* **save_image_same_resolution**:-saves the image in the **augment_data** function as the same resolution as given the input

* **save_image_fit_resolution**:saves the image in the **augment_data** function minimized (as visualized by cv2 in imshow). However note that this function is slower than the **save_image_same_resolution**. It can be changed manually by replacing function name in **augment_data**.

## Var Directory

It contains the part of the code from the data_augmentation.py which are implemented independently for visual and knowledge purpose


## Author

**Anurag Ramteke** 