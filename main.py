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

### IMPORTANT INFORMATION ON HOW TO READ THESE SCRIPTS ###

# The code within this program is organized as such:
# The main.py is the python script that runs the code. It is responsible for loading the davis camera recordins, and then using funcions defined in other files to filter the data
# and save the resulting images within the folder it is run in.

# Most functions you will see below have jitted_ in front of them. This is a function that has been passed to the numba library to convert them to machine code that makes them run much faster.
# If you are trying to follow the function calling path, go to the file name after the jitted_ within the folder that the main.py is located.

# Right now, the main.py includes a functions.py file, which contains a python script that includes all the other functions within the program.

# The order in which functions are called within this file work as such:
# 1. Loads the aedat4 file -> only if it has not already be loaded in a previous loop.

# 2. pass the data to the filter1 function and the filter10 function. Each output is stored seperatly.

# 3. Results of both filters are independently sent to filter2. Filter2 is run multiple times, as each runtrhough, a number of points are removed.

# 4. After going through filter2, both results are passed to a function called dual_pollarity_filter. This function takes points that are found in both the 0 and 1 polarities at the same x and y
# coordinates, and plots them in purple. Without this, all 0 polarity points at the same x and y coords will be completely overshadowed by the 1 polarity hits with the same coordinates. These points are stored in a third array,
# and the 2 different 1 and 0 hit polarity arrays remain unchanged.

# 5. The 0 and 1 polarity arrays are combined into a new array that is passed to the object_tracking function. This function draws boxes around the filtered objects detected.
# Note that within the object_tracking function is a call to another function called image_classifier. This function is called depending on a user defined variable make_test_data.
# It classifies objects based on a trained tensorflow model.
# If make_test_data is set to True, it will output the zoomed in images of objects found within the boxes. If False, it outputs the whole image with tracked objects having a predicted label above them.

# 6. Results are saved to the local directory of the main.py file. The program will loops through this process over and over until it reaches the end of the aedat4 file.

## NOTE: Descriptions on what each function actually do can be found within their respective file.

def filterTrackCode(timeRVar,
                    positiveVar,
                    maxDVar,
                    incrementVar,
                    minVar,
                    maxVar,
                    sampleSVar,
                    minDVar,
                    minHVar,
                    toleranceVar,
                    maxTIVar,
                    fileSelectVar,
                    directorySelVar,
                    model,
                    make_test_data,
                    ):

    time_range = int(timeRVar)
    positive = int(positiveVar)
    max_distance = int(maxDVar)
    increment = int(incrementVar)
    min = int(minVar)
    max = int(maxVar)
    sample_size = int(sampleSVar)
    min_distance = int(minDVar)
    min_hits = int(minHVar)
    tolerance = int(toleranceVar)
    max_tracking_iterations = int(maxTIVar)

    #Start_Time is set to 0 here, used to track execution time.
    start_time = time.time()

    ## Note: Filter 1 takes the data from the Aedat file and filters it based on distances from a specific point and its distance from its
    ## neighbors, calculated using the X and Y values, as well as time in the form of a Z axis.
    ## Filter 2 takes the output from Filter 1 and filters it just using the distances from a hit point and its nearest neighbors, not taking
    ## into account the time variable.
    ## The thing that effects computation time the most is the time_range (Higher = more time) and the total number of points on the graph
    ## before passing it to filter 2.


    # Load data from Aedat file.
    with AedatFile(fileSelectVar) as f:
        events = np.hstack([packet for packet in f['events'].numpy()])
        timestamps, x, y, polarities = events['timestamp'], events['x'], events['y'], events['polarity']


        # Below here is a while loop that loops through the video data in increments.
        index3 = 0
        while index3 < 750:
            # Call the first filter and return the data to x_hits and y_hits.
            x_hits, y_hits = jitted_filter1(events, min, max, time_range, max_distance, positive)

            # Call filter10 and return the data to x_hits0 and y_hits0.
            x_hits0, y_hits0 = jitted_filter10(events, min, max, time_range, max_distance, positive)

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
            xdouble_hits,ydouble_hits = jitted_dualpolarityplotter(x_hits, y_hits, x_hits0, y_hits0)

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
            object_tracking(x_combined, y_combined, index3, x_hits, y_hits, x_hits0, y_hits0, sample_size, min_distance, min_hits, tolerance, max_tracking_iterations, directorySelVar, model, make_test_data)

            #Define double polarity hit arrays
            xdouble_hits = np.empty(0)
            ydouble_hits = np.empty(0)

            #Checks if make_test_data is set to false. If so saved the generated classification image.
            if(make_test_data == 0):
                title = 'Time Increment: ' + str(min) + ' to ' + str(max)
                plt.title(title)
                plt.xlim(0, 350)
                plt.ylim(250, 0)
                plt.axis('off')
                plt.savefig(directorySelVar + str(index3))
                print(directorySelVar + str(index3) + '.png')

            plt.clf()

            # Increment time.
            min = min + increment
            max = max + increment
            index3 += 1
