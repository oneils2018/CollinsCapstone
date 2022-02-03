import cv2
#cv2 (opencv-python) allows users to read files from a directory and create a video file from said images
#default framerate appears to be 15 frames per second, can probably be modified
#gives image dims

import glob
#glob (glob2) allows users to read every file of a certain file type in a directory. In this case:
#glob will read all files ending in a .png to be stored into img array
#sorted ensures that files are read in the proper order
#key is algorithm used to determine how to sort files in directory
#current algorithm will sort based on numerical values starting at 0

import numpy as np
import re
#re allows for numerical resorting to ensure all files are read in order
#cv2 reads files in alphabetical order(not numerical) so 10 is read before 9

import os
#NOTE: CODE UNORIGINAL, numericalSort function obtained from
# https://stackoverflow.com/questions/12093940/reading-files-in-a-particular-order-in-python
#User: Martijn Pieters on Aug 23, 2012
numbers = re.compile(r'(\d+)')
def numericalSort(value):
    parts = numbers.split(value)
    parts[1::2] = map(int, parts[1::2])
    return parts

#image reading code obtained from
#https://theailearner.com/2018/10/15/creating-video-from-images-using-opencv-python/
#User: kang&atul on 15 Oct 2018
img_array = []              #numpy array to store image information
for filename in sorted(glob.glob(r'C:\Users\Stephen\Desktop\Collins_Capstone\*.png'), key=numericalSort):
    img = cv2.imread(filename)
    print("Reading image: ", filename)
    height, width, layers = img.shape
    size = (width, height)
    img_array.append(img)


output = cv2.VideoWriter('DV_saved-2021_08_24_11_13_45.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 15, size)

for i in range(len(img_array)):
    output.write(img_array[i])
output.release()

#the following code removes all png files from the directory to prevent old images being added to videos
for filename in glob.glob(r'C:\Users\Stephen\Desktop\Collins_Capstone\*.png'):
    os.remove(filename)

