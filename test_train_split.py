import glob
#glob used for iterating through filepath to find a specified file type, in this case .png files
import os
#os used to create directories and move/replace files

import random
#used to select random file in working directory (prevent overfitting in model)

#Developed by Stephen O'Neil 2/21/2022
#Original Code

#file_path (string) is the working directory where the pngs can be found and where object training test split folders will be created
#object_name (string) is the name of the object being split for classification reasons (Cube, Plane, Cone, etc)
#train_split (float) used to specify percentage of files to be placed into each train/test folder (expecting floats like 0.6, 0.8, 0.9)
    #could be modified to accept other values

def test_train_split(file_path, object_name, train_split):

    n = 0   #variable for number of files to be split

    parent_path = os.path.join(file_path, object_name)  #parent directory (named after object i.e. cube, cone, quadcopter, etc)
    train_path  = os.path.join(parent_path, r"train")   #train path to folder inside parent_path, labeled as train
    test_path = os.path.join(parent_path, r"test")      #same as train_path but labeled as test


    # attempts to create 3 new directories, one labeled after object and two inside the first labeled as train, test
    #prints message if folders already exist
    try:    #parent folder
        os.mkdir(parent_path)
    except OSError:
        print(parent_path + " already exists in working directory")

    try:    #train folder
        os.mkdir(train_path)
    except OSError:
        print(train_path + " already exists in working directory")

    try:    #test folder
        os.mkdir(test_path)
    except OSError:
        print(test_path + " already exists in working directory")


    for filename in glob.glob(file_path + r"\*.png"):   #finds .png files in file_path
        n += 1  # gets num of png files to split

    print("Found " + str(n) + " png files in directory " + file_path)


    i = 0                           #used for naming files/counting index for train/test split
    index = int(n * train_split)    #whatever percentage of total number of files to be put into train

    #while loop will iterate i number of times (i value based off of split percentage)
    while i < index:
        file_names = glob.glob(file_path + r"\*.png")    #creates a python list of all .png files located in file_path
        file = random.choice(file_names)                 #selects a random png file from file_names list
        print(os.path.basename(file))
        os.replace(file, train_path + "\\" + os.path.basename(file))    #move randomly selected file
                                            #os.path.basename() gets actual file name, i.e. '0.png'

        i += 1

    #following loop will take all remaining png files not selected and place them into the test folder
    for filename in glob.glob(file_path + r"\*.png"):
        #moves remaining pngs in file into test split folder
        os.replace(filename, test_path + "\\" + os.path.basename(filename))
        i += 1


#sample test
test_train_split(r"C:\Users\Stephen\PycharmProjects\Collins_Capstone", r"cube", 0.8)



