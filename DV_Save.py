import cv2

"""

Description:

    cv2 is a module that import name for opencv-python. It’s a library that helps the users to read a file from the directory and will develop a video file from images

    Default Frame rate around 15 frames per second

    Provides the image with dimensions

"""

import glob

"""

Description:

glob is used to return all file paths that match a specific pattern.

The use of glob can help with searching a specific file pattern or search files where the filename matches a certain pattern by using a wildcard character.

glob will read all the files the end with .png and will store it in an img array

The sorted function that we use will help that the files are read in the appropriate order that we want.

A build in algorithm that is called will help with the return a view object that displays a list of all the keys in the dictionary in order of insertion. It used to determine how to sort the files in directory.

current algorithm will sort based on numerical values starting at 0

"""
import numpy as np

"""
Description:

Import numpy as np, shortening the phrase “numpy” to np to make the code easier to comprehend

Numpy Is a library for the python programming language, adding support for  large, multi-dimensional arrays and matrices, along with a large collection of high-level mathematical function to operate on arrays.

You can install numpy to your device by the following command:
Import numpy as np

"""

import re

"""

Description:
    This import re (regular expression) specifies a set of strings that matches it; the functions in this module will let you check if a 
    particular string matches a given regular expression.

    It helps with resorting in numerical order to make sure that the files are read in proper order.

    cv2 reads files in alphabetical order (not numerical) so 10 is read before 9.

"""
import os

"""“

Description:
    code obtained:
     https://stackoverflow.com/questions/12093940/reading-files-in-a-particular-order-in-python
     User: Martijn Pieters on Aug 23, 2012

"""

def generate_video(file_path, output_name, del_toggle):

    numbers = re.compile(r'(\d+)')

"""

Description:
    Pythons re.compile() is used to compile a regular expression pattern provided as a string into a regex pattern object. We can compile a regular expression into a regex object to look for occurrences of the same patter inside various target string without rewriting it.

"""

def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts


img_array = []              #numpy array to store image information
for filename in sorted(glob.glob(file_path), key=numericalSort):
    img = cv2.imread(filename)
    print("Reading image: ", filename)
    height, width, layers = img.shape
    size = (width, height)
    img_array.append(img)

output = cv2.VideoWriter(output_name + '.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 15, size)

for i in range(len(img_array)):
    output.write(img_array[i])
output.release()

"""
Description:

    In this code block the first thing we go is fetch all the image files names using glob
    Then we read all the images using cv2.imread().
   
    Afterwards, we store all the images into a list. 
   
    We then develop object videowriter using cv2.VideoWriter().
   
    Later on we  save the images to video file using cv3.videowriter().write() Lastly, we release the videowriter and destroy all windows

    image reading code obtained from
    https://theailearner.com/2018/10/15/creating-video-from-images-using-opencv-python/
    User: kang&atul on 15 Oct 2018

"""

if del_toggle == True:
    for filename in glob.glob(file_path):
        os.remove(filename)

"""

Description:

    The os.remove methods in python is used to remove or delete a file path

    The following code removes all png files from the directory to prevent old images being added to videos

"""

