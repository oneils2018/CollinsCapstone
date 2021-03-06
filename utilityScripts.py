# cv2 (opencv-python) allows users to read files from a directory and create a video file from said images
# default framerate appears to be 15 frames per second, can probably be modified
# gives image dims
import cv2

# glob (glob2) allows users to read every file of a certain file type in a directory. In this case:
# glob will read all files ending in a .png to be stored into img array
# sorted ensures that files are read in the proper order
# key is algorithm used to determine how to sort files in directory
# current algorithm will sort based on numerical values starting at 0
import glob

# re allows for numerical resorting to ensure all files are read in order
# cv2 reads files in alphabetical order(not numerical) so 10 is read before 9
import re

# used to select random file in working directory (prevent overfitting in model)
import random

# Allows the script to interact with the os
import os

# Useful scripts that can perform automated tasks. Not part of any algorithm directly.

# NOTE: CODE UNORIGINAL, numericalSort function obtained from
# https://stackoverflow.com/questions/12093940/reading-files-in-a-particular-order-in-python
# User: Martijn Pieters on Aug 23, 2012
# PNGs to MP4 as a function
def generateVideo(file_path, output_name, del_toggle):
    numbers = re.compile(r'(\d+)')

    def numericalSort(value):
        parts = numbers.split(value)
        parts[1::2] = map(int, parts[1::2])
        return parts

    # Image reading code obtained from
    # https://theailearner.com/2018/10/15/creating-video-from-images-using-opencv-python/
    # User: kang&atul on 15 Oct 2018
    img_array = []  # numpy array to store image information
    for filename in sorted(glob.glob(file_path + '\*.png'), key=numericalSort):
        img = cv2.imread(filename)
        print('Reading image: ', filename)
        height, width, layers = img.shape
        size = (width, height)
        img_array.append(img)

    output = cv2.VideoWriter(file_path + output_name + '.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 15, size)
    print("MP4 file saved: " + file_path + output_name + '.mp4')

    for i in range(len(img_array)):
        output.write(img_array[i])
    output.release()

    # The following code removes all png files from the directory to prevent old images being added to videos
    if del_toggle == 1:
        for filename in glob.glob(file_path + '/' + '*.png'):
            os.remove(filename)


# Developed by Stephen O'Neil 2/21/2022
# Original Code
# file_path (string) is the working directory where the pngs can be found and where object training test split folders will be created
# object_name (string) is the name of the object being split for classification reasons (Cube, Plane, Cone, etc)
# train_split (float) used to specify percentage of files to be placed into each train/test folder (expecting floats like 0.6, 0.8, 0.9)
# could be modified to accept other values
def test_train_split(file_path, object_name, train_split):
    n = 0  # variable for number of files to be split

    parent_path = os.path.join(file_path,
                               object_name)  # parent directory (named after object i.e. cube, cone, quadcopter, etc)
    train_path = os.path.join(parent_path, r"train")  # train path to folder inside parent_path, labeled as train
    test_path = os.path.join(parent_path, r"test")  # same as train_path but labeled as test

    # attempts to create 3 new directories, one labeled after object and two inside the first labeled as train, test
    # prints message if folders already exist
    try:  # parent folder
        os.mkdir(parent_path)
    except OSError:
        print(parent_path + " already exists in working directory")

    try:  # train folder
        os.mkdir(train_path)
    except OSError:
        print(train_path + " already exists in working directory")

    try:  # test folder
        os.mkdir(test_path)
    except OSError:
        print(test_path + " already exists in working directory")

    for filename in glob.glob(file_path + r"\*.png"):
        n += 1  # gets num of png files to split

    print("Found " + str(n) + " png files in directory " + file_path)

    i = 0  # used for naming files/counting index for train/test split
    index = int(n * train_split)  # whatever percentage of total number of files to be put into train

    # while loop will iterate i number of times (i value based off of split percentage)
    while i < index:
        file_names = glob.glob(file_path + r"\*.png")  # creates a python list of all .png files located in file_path
        file = random.choice(file_names)  # selects a random png file from file_names list
        print(os.path.basename(file))
        os.replace(file, train_path + "\\" + os.path.basename(file))  # move randomly selected file
        # os.path.basename() gets actual file name, i.e. '0.png'

        i += 1

    # following loop will take all remaining png files not selected and place them into the test folder
    for filename in glob.glob(file_path + r"\*.png"):
        # moves remaining pngs in file into test split folder
        os.replace(filename, test_path + "\\" + os.path.basename(filename))
        i += 1
