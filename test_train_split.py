import glob
#glob used for iterating through filepath to find a specified file type, in this case .png files
import os
#os used to create directories and move/replace files

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
    try:
        #attempts to create 3 new directories, one labeled after object and two inside the first labeled as train, test
        os.mkdir(parent_path)
        os.mkdir(train_path)
        os.mkdir(test_path)

    except OSError as error:
        #prints error if filenames already exists (can be ignored, program will continue normally)
        print(error)

    for filename in glob.glob(file_path + r"\*.png"):
        n += 1  # gets num of png files to split

    print("Found " + str(n) + " png files in directory " + file_path)


    i = 0                           #used for naming files/counting index for train/test split
    index = int(n * train_split)    #whatever percentage of total number of files to be put into train

    for filename in glob.glob(file_path + r"\*.png"):
        #iterates through working directory and moves i number of png files into training split
        if i < index:
            os.replace(filename, train_path + "\\" + str(i) + ".png")

            i += 1
        else:
            break   #moves onto test split
    for filename in glob.glob(file_path + r"\*.png"):
        #moves remaining pngs in file into test split folder
        os.replace(filename, test_path + "\\" + str(i) + ".png")
        i += 1


test_train_split(r"C:\Users\Stephen\PycharmProjects\Collins_Capstone", r"cube", 0.8)



