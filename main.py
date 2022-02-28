import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import math as math
# numba is a library that must be install by running "pip install numba" It takes a function and re-writes in machine code to run extremely fast. It works best if numpy arrays are used.
from scipy import stats
from dv import AedatFile
import os
from functions import *


#Start_Time is set to 0 here, used to track execution time.
start_time = time.time()

## Note: Filter 1 takes the data from the Aedat file and filters it based on distances from a specific point and its distance from its
## neighbors, calculated using the X and Y values, as well as time in the form of a Z axis.
## Filter 2 takes the output from Filter 1 and filters it just using the distances from a hit point and its nearest neighbors, not taking
## into account the time variable.
## The thing that effects computation time the most is the time_range (Higher = more time) and the total number of points on the graph
## before passing it to filter 2.


min = 0
max = 5000
test = 0

# Load data from Aedat file.
#with AedatFile(r"C:\Users\jerem\Downloads\dvSave-2021_08_24_10_44_21.aedat4") as f:
with AedatFile(r"F:\Capstone\CollinsCapstone\dvSave-2022_02_21_14_13_04_cube_and_cone.aedat4") as f:
    events = np.hstack([packet for packet in f['events'].numpy()])
    timestamps, x, y, polarities = events['timestamp'], events['x'], events['y'], events['polarity']

    
    # Below here is a while loop that loops through the video data in increments.
    index3 = 0
    while index3 < 750:
        # Call the first filter and return the data to x_hits and y_hits.
        x_hits, y_hits = jitted_filter1(events, min, max)

        # Call filter10 and return the data to x_hits0 and y_hits0.
        x_hits0, y_hits0 = jitted_filter10(events, min, max)

        # Prints filter data to console.
        print("Total points on plot after first (+1) filter: ", len(x_hits))
        print("Total points on plot after first (-1) filter: ", len(x_hits0))

        # This while loop runs the second filter multiple times to remove any excess noise.
        index = 0
        while index < 7:
            x_hits, y_hits = jitted_filter2(x_hits, y_hits)
            x_hits0, y_hits0 = jitted_filter2(x_hits0, y_hits0)
            index += 1

        # Prints time and filter information to console.
        total_time = round((time.time() - start_time), 2)
        print("Total points on plot after second (+1) filter: ", len(x_hits))
        print("Total points on plot after second (-1) filter: ", len(x_hits0))
        print("Execution time: %s seconds" % (total_time))
        print("On Image #", index3)


        #Calls the jitted dualpolarityplotter function and stores the values in xdouble_hits and ydouble_hits
        xdouble_hits,ydouble_hits = jitted_dualpolarityplotter(x_hits,y_hits,x_hits0,y_hits0)

        #Adds the found hits to the plot function.
        plt.scatter(x_hits, y_hits, s=1, c='red')
        plt.scatter(x_hits0, y_hits0, s=1, c='blue')
        plt.scatter(xdouble_hits, ydouble_hits, s=11, c='purple')

        # Combine pixels of 1 and -1 polarity.
        x_combined = np.concatenate((x_hits, x_hits0))
        y_combined = np.concatenate((y_hits, y_hits0))

        #calls the object tracking function to draw boxes around objects found within image, extract the zoomed in images found within boxes,
        #and if make_test_data is set to True saves said images, if not it will use them to classify objects detected, delete the zoomed images, then save
        #an image showing the models predictions.
        object_tracking(x_combined,y_combined,index3,x_hits,y_hits,x_hits0,y_hits0)
        
        #Define double polarity hit arrays
        xdouble_hits = np.empty(0)
        ydouble_hits = np.empty(0)

        #Checks if make_test_data is set to false. If so saved the generated classification image.
        if(make_test_data == False):
            plt.xlim(0, 350)
            plt.ylim(250, 0)
            plt.axis('off')
            plt.savefig(str(index3))
            plt.clf()

        # Increment time.
        min = min + increment
        max = max + increment
        index3 += 1
