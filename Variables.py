# Python GUI module
import tkinter as tk

# tkinter extra widgets like the progress bar
from tkinter import ttk

# Allows the creation of hover over tooltips with tkinter
# https://github.com/gnikit/tkinter-tooltip
# pip install tkinter-tooltip
from tktooltip import ToolTip

# Allows using multiple threads for specific lines of code.
# Useful to stop tkinter from freezing from running loops
import threading

# Allows the script to interact with the os
import os


# This file hold all of the alterable variables that are used in the different alsogithms. Editing the values here is similar to editing the values with the GUI.

# Makes variables available for all classes making them act as global variables
class variables():
    def __init__(self,
                 time_range,
                 positive,
                 max_distance,
                 increment,
                 min,
                 max,
                 sample_size,
                 min_distance,
                 min_hits,
                 tolerance,
                 max_tracking_iterations,
                 fileSelect,
                 directorySel,
                 fileNameSet,
                 object_name,
                 train_split,
                 model,
                 make_test_data,
                 ):

        ############################
        ##### FILTER Variables #####
        ############################

        # The time_range is how far back in time and in the future of the current index does the program check for hits.
        # This has the largest hit on performance (Exponentially)
        self.time_range = time_range

        # Positive is the minimum number of neighbor hits that must be attained for the hit to be added to the plot.
        self.positive = positive

        # The max_distance is the maximum distance in a 3d space
        # Where z is time that a hit must be under to be added to the plot.
        self.max_distance = max_distance

        # The increment is the duration of time stamps the program will process at a time then plot to a graph.
        self.increment = increment

        # The event number after the increment from which the filter starts
        self.min = min

        # The number of events filtered into a single frame
        self.max = max

        ##############################
        ##### TRACKING Variables #####
        ##############################

        # Determines how large a sample size we should take for averaging pixels to find the center of an object
        self.sample_size = sample_size

        # Threshold for number of misses in a row before we "give up" and use the last hit as a bound
        self.min_distance = min_distance

        # Minimum number of hits within a sample required to identify it as an object and draw a box
        self.min_hits = min_hits

        # How much bigger should the box be then the object
        self.tolerance = tolerance

        # How many times should we iterate the tracking function before we give up
        self.max_tracking_iterations = max_tracking_iterations

        #############################
        ##### GUI/Etc Variables #####
        #############################

        # Selected file path for filtering and tracking
        self.fileSelect = fileSelect

        # Selected directory to convert into mp4
        self.directorySel = directorySel

        # Filename for the video
        self.fileNameSet = fileNameSet

        # Parent directory name for the test/train split script for classification reasons (Cube, Plane, Cone, etc)
        self.object_name = object_name

        # Specify percentage of files to be placed into each test/train folder (expecting floats like 0.6, 0.8, 0.9)
        self.train_split = train_split

        # Selected model to use for object identification
        self.model = model

        # Used to make the main function generate test images to train a tensorflow model,
        # or to use a trained model to classify data and output the saved images.
        self.make_test_data = make_test_data


# Obtains the current directory of this file and attach a new folder for script results
directoryPath = os.path.join(os.path.dirname(__file__), 'Results\\')

# Unchanging global default values of variables
defaultVals = ['zero',              # 'zero' or 0 is always used to bump array by one
               7,                   # time range (filter)
               2,                   # positive (filter)
               10,                  # max distance (filter)
               10000,               # increment (filter)
               0,                   # min (filter)
               40000,               # max(filter)
               40,                  # sample size (tracking)
               10,                  # min distance (tracking)
               50,                  # min hits (tracking)
               5,                   # tolerance (tracking)
               50,                  # max tracking distance (tracking)
               '',                  # file select (GUI)
               directoryPath,       # directory select (GUI)
               'Default',           # file name set (GUI)
               'Object_Name',       # test/train parent directory (Etc)
               0.8,                 # test/train percentage (Etc)
               os.path.dirname(__file__) + '\\tensorflow_model.h5', # Tensorflow Model (Etc)
               0,                   # make test data (Etc)
               ]

# Initially set all variables to their default values
v1 = variables(defaultVals[1],
               defaultVals[2],
               defaultVals[3],
               defaultVals[4],
               defaultVals[5],
               defaultVals[6],
               defaultVals[7],
               defaultVals[8],
               defaultVals[9],
               defaultVals[10],
               defaultVals[11],
               defaultVals[12],
               defaultVals[13],
               defaultVals[14],
               defaultVals[15],
               defaultVals[16],
               defaultVals[17],
               defaultVals[18],
               )

# Places all global variables into an array for loops. Each variable can be used without using this array.
vars = ['zero',                     # 0
        v1.time_range,              # 1
        v1.positive,                # 2
        v1.max_distance,            # 3
        v1.increment,               # 4
        v1.min,                     # 5
        v1.max,                     # 6
        v1.sample_size,             # 7
        v1.min_distance,            # 8
        v1.min_hits,                # 9
        v1.tolerance,               # 10
        v1.max_tracking_iterations, # 11
        v1.fileSelect,              # 12
        v1.directorySel,            # 13
        v1.fileNameSet,             # 14
        v1.object_name,             # 15
        v1.train_split,             # 16
        v1.model,                   # 17
        v1.make_test_data           # 18
        ]

# Text for tooltip popups when hovering over an item
toolTips = ['zero',
            'The time_range is how far back in time and in the future of the current index does the program check for hits. This has the largest hit on performance (Exponentially).',
            'Positive is the minimum number of neighbor hits that must be attained for the hit to be added to the plot.',
            'The max_distance is the maximum distance in a 3d space. Where z is time that a hit must be under to be added to the plot.',
            'The increment is the duration of time stamps the program will process at a time then plot to a graph.',
            'The event number after the increment from which the filter starts.',
            'The number of events filtered into a single frame.',
            'Determines how large a sample size we should take for averaging pixels to find the center of an object.',
            'Threshold for number of misses in a row before we "give up" and use the last hit as a bound.',
            'Minimum number of hits within a sample required to identify it as an object and draw a box.',
            'How much bigger should the box be then the object.',
            'How many times should we iterate the tracking function before we give up.',
            '',
            '',
            '',
            'The name of the object being split for classification reasons (Cube, Plane, Cone, etc). Will be the name of the parent folder of the test/train split data.',
            'specify percentage of files to be placed into each train/test folder (expecting floats like 0.6, 0.8, 0.9)',
            ''
            ]

# Array of entry boxes and their intended use per variable
entry = ['zero',                    # 0
         'Time Range',              # 1
         'Positive Hits',           # 2
         'Max Distance',            # 3
         'Increment',               # 4
         'Min',                     # 5
         'Max',                     # 6
         'Sample Size',             # 7
         'Min Distance',            # 8
         'Min Hits',                # 9
         'Tolerance',               # 10
         'Max Tracking Iterations', # 11
         'File select',             # 12
         'Directory Select',        # 13
         'File Name Set',           # 14
         'Object Name',             # 15
         'Train Split',             # 16
         'Tensorflow model',        # 17
         'Make Test Data',          # 18
         ]

# Array of string names of the variables
varName = entry.copy()



#make_test_data = False
    
    
