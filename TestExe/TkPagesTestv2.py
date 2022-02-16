# Imported to track the time elapsed when executing code
import time

# Mainly used for arrays in algorithms
import numpy as np

# Used to plot the filtered points graphs
import matplotlib.pyplot as plt

# Used to create the graph legend
import matplotlib.patches as mpatches

# Used for quick maths in the algorithms
import math as math

# numba is a library that must be install by running 'pip install numba'.
# It takes a function and re-writes in machine code to run extremely fast.
# It works best if numpy arrays are used.
from numba import jit, njit, vectorize

# Used to read and import aedat4 files
from dv import AedatFile

# Python GUI module
import tkinter as tk

# tkinter extra widgets like the progress bar
from tkinter import ttk

# Allows the creation of hover over tooltips with tkinter
from tktooltip import ToolTip

# Allows using multiple threads for specific lines of code.
# Useful to stop tkinter from freezing from running loops
import threading

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

# Allows the script to interact with the os
import os

# Tkinter skeleton built off from:
# https://stackoverflow.com/questions/14817210/using-buttons-in-tkinter-to-navigate-to-different-pages-of-the-application

# Makes variables avaliable on all classes making them act as global variables
class variables():
    def __init__(self, *args, **kwargs):

        ############################
        ##### FILTER Variables #####
        ############################

        # The time_range is how far back in time and in the future of the current index does the program check for hits.
        # This has the largest hit on performance (Exponentially)
        self.time_range = int

        # Positive is the minimum number of neighbor hits that must be attained for the hit to be added to the plot.
        self.positive = int

        # The max_distance is the maximum distance in a 3d space
        # Where z is time that a hit must be under to be added to the plot.
        self.max_distance = int

        # The increment is the duration of time stamps the program will process at a time then plot to a graph.
        self.increment = int

        # The event number after the increment from which the filter starts
        self.min = int

        # The number of events filtered into a single frame
        self.max = int

        ##############################
        ##### TRACKING Variables #####
        ##############################

        # Determines how large a sample size we should take for averaging pixels to find the center of an object
        self.sample_size = int

        # Threshold for number of misses in a row before we "give up" and use the last hit as a bound
        self.min_distance = int

        # Minimum number of hits within a sample required to identify it as an object and draw a box
        self.min_hits = int

        # How much bigger should the box be then the object
        self.tolerance = int

        # How many times should we iterate the tracking function before we give up
        self.max_tracking_iterations = int

        #########################
        ##### GUI Variables #####
        #########################

        # GUI selected file path for filtering and tracking
        self.fileSelect = ''

        # GUI selected directory to convert into mp4
        self.directorySel = ''

        # GUI save filename for video
        self.fileNameSet = ''


# Obtains the current directory of this file and attach a new folder for script results
directoryPath = os.path.join(os.path.dirname(__file__), 'Results\\')

# Global default values of variables
defaultVals = ['zero',              # ('zero' or 0 is always used to bump array by one)
               7,                   # time range (filter)
               2,                   # positive (filter)
               10,                  # max distance (filter)
               10000,               # increment (filter)
               0,                   # min (filter)
               40000,               # max(filter)
               40,                  # sample size (tracking)
               10,                  # min distance (tracking)
               50,                  # min hits (tracking)
               5,                   # tolarance (tracking)
               50,                  # max tracking distance (tracking)
               '',                  # file select (GUI)
               directoryPath,       # directory select (GUI)
               'Default'            # file name set (GUI)
               ]

# Initially set all variables to their default values
variables.time_range = defaultVals[1]
variables.positive = defaultVals[2]
variables.max_distance = defaultVals[3]
variables.increment = defaultVals[4]
variables.min = defaultVals[5]
variables.max = defaultVals[6]
variables.sample_size = defaultVals[7]
variables.min_distance = defaultVals[8]
variables.min_hits = defaultVals[9]
variables.tolerance = defaultVals[10]
variables.max_tracking_iterations = defaultVals[11]
variables.fileSelect = defaultVals[12]
variables.directorySel = defaultVals[13]
variables.fileNameSet = defaultVals[14]

# Places all global variables into an array
vars = ['zero',                             # 0
        variables.time_range,               # 1
        variables.positive,                 # 2
        variables.max_distance,             # 3
        variables.increment,                # 4
        variables.min,                      # 5
        variables.max,                      # 6
        variables.sample_size,              # 7
        variables.min_distance,             # 8
        variables.min_hits,                 # 9
        variables.tolerance,                # 10
        variables.max_tracking_iterations,  # 11
        variables.fileSelect,               # 12
        variables.directorySel,             # 13
        variables.fileNameSet,              # 14
        ]

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
            ]

# Array of entry boxes and their intended uses per variable
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
         ]

# Array of string names of the variables
varName = ['zero',                      # 0
           'Time Range',                # 1
           'Positive Hits',             # 2
           'Max Distance',              # 3
           'Increment',                 # 4
           'Min',                       # 5
           'Max',                       # 6
           'Sample Size',               # 7
           'Min Distance',              # 8
           'Min Hits',                  # 9
           'Tolerance',                 # 10
           'Max Tracking Iterations',   # 11
           'File Destination',          # 12
           'Directory Select',          # 13
           'File Name Set',             # 14
           ]

# Array for save buttons
saveButton = list(range(1,100))

# Restarts the program
def restartProgram():
    root.destroy()
    os.startfile('tkPagesTestv2.py')
    os.startfile('tkPagesTestv2.exe')

# Create frame around tkinter pages
class Page(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)

    def show(self):
        self.lift()


# Filter variables screen
class Page1(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        # Declaring entry fields and insert their default value into the entry fields
        i = 1
        while i <= 6:
            entry[i] = tk.Entry(self)
            entry[i].insert(0, vars[i])
            # print(vars[i])
            i += 1

        ### GUI widgets placement, text, and commands ###

        # Title of the page
        label01 = tk.Label(self, text='Filter Variables:')

        # Labels for each entry field
        label1 = tk.Label(self, text='Time range')
        label2 = tk.Label(self, text='Positive hits')
        label3 = tk.Label(self, text='Max distance')
        label4 = tk.Label(self, text='Increment')
        label5 = tk.Label(self, text='Min')
        label6 = tk.Label(self, text='Max')

        # Declaring save buttons for each entry field
        Button1 = tk.Button(self, text='Save', command=lambda: printValue(1))
        Button2 = tk.Button(self, text='Save', command=lambda: printValue(2))
        Button3 = tk.Button(self, text='Save', command=lambda: printValue(3))
        Button4 = tk.Button(self, text='Save', command=lambda: printValue(4))
        Button5 = tk.Button(self, text='Save', command=lambda: printValue(5))
        Button6 = tk.Button(self, text='Save', command=lambda: printValue(6))

        # Button to reset the filter variables to their default
        Button100 = tk.Button(self, text='Reset filter to default values', command=lambda: resetToDefaultValues(1))

        # Grid location of entry fields, labels, and buttons
        entry[1].grid(column=1, row=1, columnspan=1, padx=5, pady=5)
        entry[2].grid(column=1, row=2, columnspan=1, padx=5, pady=5)
        entry[3].grid(column=1, row=3, columnspan=1, padx=5, pady=5)
        entry[4].grid(column=1, row=4, columnspan=1, padx=5, pady=5)
        entry[5].grid(column=1, row=5, columnspan=1, padx=5, pady=5)
        entry[6].grid(column=1, row=6, columnspan=1, padx=5, pady=5)

        label01.grid(column=0, row=0, columnspan=2, padx=5, pady=5)

        label1.grid(column=0, row=1, columnspan=1, padx=5, pady=5)
        label2.grid(column=0, row=2, columnspan=1, padx=5, pady=5)
        label3.grid(column=0, row=3, columnspan=1, padx=5, pady=5)
        label4.grid(column=0, row=4, columnspan=1, padx=5, pady=5)
        label5.grid(column=0, row=5, columnspan=1, padx=5, pady=5)
        label6.grid(column=0, row=6, columnspan=1, padx=5, pady=5)

        Button1.grid(column=2, row=1, columnspan=1, padx=5, pady=5)
        Button2.grid(column=2, row=2, columnspan=1, padx=5, pady=5)
        Button3.grid(column=2, row=3, columnspan=1, padx=5, pady=5)
        Button4.grid(column=2, row=4, columnspan=1, padx=5, pady=5)
        Button5.grid(column=2, row=5, columnspan=1, padx=5, pady=5)
        Button6.grid(column=2, row=6, columnspan=1, padx=5, pady=5)

        Button100.grid(column=3, row=7, columnspan=1, padx=5, pady=5)

        # Hovering tool tips for each label
        ToolTip(label1, msg=toolTips[1], follow=True)
        ToolTip(label2, msg=toolTips[2], follow=True)
        ToolTip(label3, msg=toolTips[3], follow=True)
        ToolTip(label4, msg=toolTips[4], follow=True)
        ToolTip(label5, msg=toolTips[5], follow=True)
        ToolTip(label6, msg=toolTips[6], follow=True)

        # Reset variables to default values and displays a notification
        def resetToDefaultValues(algo):
            if algo == 1:
                i = 1
                j = 6
                print('Filter reseted to defaut')
            if algo == 2:
                i = 7
                j = 11
                print('Tracker reseted to defaut')
            while i <= j:
                vars[i] = defaultVals[i]
                entry[i].delete(0, 'end')
                entry[i].insert(0, vars[i])
                i += 1
            label0 = tk.Label(self, text='Reset to default!', fg='orange', bg='white')
            label0.grid(column=3, row=0, pady=5)
            self.after(500, lambda: label0.grid_remove())

        # Saves entry to variable and displays a notification
        def printValue(num):
            vars[num] = entry[num].get()
            label0 = tk.Label(self, text=str(varName[num]) + ' Saved!', fg='green', bg='white')
            label0.grid(column=3, row=num, pady=5)
            self.after(500, lambda: label0.grid_remove())
            print(vars[num])


# Tracking variables screen
class Page2(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        ### GUI widgets placement, text, and commands. Similar to the ones in Page1 but modified for tracking variables. ###

        i = 7
        while i <= 11:
            entry[i] = tk.Entry(self)
            entry[i].insert(0, vars[i])
            i += 1

        label02 = tk.Label(self, text='Tracker Variables:')

        label7 = tk.Label(self, text='Sample size')
        label8 = tk.Label(self, text='Min distance')
        label9 = tk.Label(self, text='Min hits')
        label10 = tk.Label(self, text='Tolarance')
        label11 = tk.Label(self, text='Max tracking iterations')

        Button7 = tk.Button(self, text='Save', command=lambda: printValue(7))
        Button8 = tk.Button(self, text='Save', command=lambda: printValue(8))
        Button9 = tk.Button(self, text='Save', command=lambda: printValue(9))
        Button10 = tk.Button(self, text='Save', command=lambda: printValue(10))
        Button11 = tk.Button(self, text='Save', command=lambda: printValue(11))

        Button101 = tk.Button(self, text='Reset tracking to default values', command=lambda: resetToDefaultValues(2))

        entry[7].grid(column=1, row=9, columnspan=1, padx=5, pady=5)
        entry[8].grid(column=1, row=10, columnspan=1, padx=5, pady=5)
        entry[9].grid(column=1, row=11, columnspan=1, padx=5, pady=5)
        entry[10].grid(column=1, row=12, columnspan=1, padx=5, pady=5)
        entry[11].grid(column=1, row=13, columnspan=1, padx=5, pady=5)

        label02.grid(column=0, row=8, columnspan=2, padx=5, pady=5)

        label7.grid(column=0, row=9, columnspan=1, padx=5, pady=5)
        label8.grid(column=0, row=10, columnspan=1, padx=5, pady=5)
        label9.grid(column=0, row=11, columnspan=1, padx=5, pady=5)
        label10.grid(column=0, row=12, columnspan=1, padx=5, pady=5)
        label11.grid(column=0, row=13, columnspan=1, padx=5, pady=5)

        Button7.grid(column=2, row=9, columnspan=1, padx=5, pady=5)
        Button8.grid(column=2, row=10, columnspan=1, padx=5, pady=5)
        Button9.grid(column=2, row=11, columnspan=1, padx=5, pady=5)
        Button10.grid(column=2, row=12, columnspan=1, padx=5, pady=5)
        Button11.grid(column=2, row=13, columnspan=1, padx=5, pady=5)

        Button101.grid(column=3, row=14, columnspan=1, padx=5, pady=5)

        ToolTip(label7, msg=toolTips[7], follow=True)
        ToolTip(label8, msg=toolTips[8], follow=True)
        ToolTip(label9, msg=toolTips[9], follow=True)
        ToolTip(label10, msg=toolTips[10], follow=True)
        ToolTip(label11, msg=toolTips[11], follow=True)

        def resetToDefaultValues(algo):
            if algo == 1:
                i = 1
                j = 6
                print('Filter reseted to defaut')
            if algo == 2:
                i = 7
                j = 11
                print('Tracker reseted to defaut')
            while i <= j:
                vars[i] = defaultVals[i]
                entry[i].delete(0, 'end')
                entry[i].insert(0, vars[i])
                i += 1
            label0 = tk.Label(self, text='Reset to default!', fg='orange', bg='white')
            label0.grid(column=3, row=8, pady=5)
            self.after(500, lambda: label0.grid_remove())

        def printValue(num):
            vars[num] = entry[num].get()
            label0 = tk.Label(self, text=str(varName[num]) + ' Saved!', fg='green', bg='white')
            label0.grid(column=3, row=num + 2, pady=5)
            self.after(500, lambda: label0.grid_remove())
            print(vars[num])

# Run scripts screen
class Page3(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        ### GUI widgets placement, text, and commands. ###

        # Title of the page
        label03 = tk.Label(self, fg='#FF0000', text='Filter and tracking program:\n '
                                          '(Need to select .aedat4 file before starting filter/track!)\n '
                                          ''
                 )

        # Labels for the search buttons
        fileCurrent1 = tk.Label(self, text='Select a File: ', anchor="w")
        directoryCurrent1 = tk.Label(self, text='Results Directory: ' + vars[13], anchor="w")

        # Buttons to search files to be used and directory where the results are placed
        searchButton1 = tk.Button(self, text='Search File', command=lambda: browseFiles1())
        searchButton2 = tk.Button(self, text='Search Results Directory', command=lambda: browseDirectory1())

        # Buttons to start and stop the algorithem.
        # They turn on when the user selects a file.
        # The stop restarts the program to stop the thread
        startButton1 = tk.Button(self, text='Start', command=lambda: [t1.start(), pb1.start()], state='disabled')
        stopButton1 = tk.Button(self, text='Stop', command=restartProgram, state='disabled')

        # A visual progressbar widget
        pb1 = tk.ttk.Progressbar(self, orient='horizontal', mode='indeterminate', length=100)

        # Grid location of entry fields, labels, and buttons
        label03.grid(column=0, row=0, columnspan=4, padx=10, pady=10)

        fileCurrent1.grid(column=1, row=1, columnspan=100, padx=10, pady=20)
        directoryCurrent1.grid(column=1, row=3, columnspan=100, padx=10, pady=20)

        searchButton1.grid(column=0, row=1, columnspan=1, padx=10, pady=20, sticky='ew')
        searchButton2.grid(column=0, row=3, columnspan=1, padx=10, pady=10, sticky='ew')

        startButton1.grid(column=0, row=4, columnspan=1, padx=10, pady=20)
        stopButton1.grid(column=1, row=4, columnspan=1, padx=10, pady=20)

        pb1.grid(column=2, row=4, columnspan=2, padx=10, pady=20)

        # Defining the thread for the filter and tracking algorithm
        def thread1():
            # Creates file directory if it does not exist
            if not os.path.isdir(vars[13]):
                os.makedirs(vars[13])

            # Input variables for the filter and tracking algorithm
            filterTrackCode(vars[1],
                            vars[2],
                            vars[3],
                            vars[4],
                            vars[5],
                            vars[6],
                            vars[7],
                            vars[8],
                            vars[9],
                            vars[10],
                            vars[11],
                            vars[12],
                            vars[13])

            # Stops progress bar animation
            pb1.stop()

        # Declares the thread for thr filter and tracking algorithm
        t1 = threading.Thread(target=thread1)

        # Makes the thread into a daemon so it would stop when the application (GUI) is closed
        t1.daemon = True

        # Funtion to browes files to use.
        def browseFiles1():
            # Search for a file popup
            vars[12] = tk.filedialog.askopenfilename(initialdir='/',
                                                     title='Select a File',
                                                     filetypes=(('aedat4 files', '*.aedat4*'), ('all files', '*.*')))

            # If a file is chosen, enable the buttons
            if vars[12] != '':
                fileCurrent1.config(text='File Selected: ' + vars[12], anchor="w")
                startButton1.config(state='normal')
                stopButton1.config(state='normal')

                # If redults directory does not exist, make one
                if not os.path.isdir(vars[13]):
                    os.makedirs(vars[13])

        # Funstion to browse for a results directory
        def browseDirectory1():
            vars[13] = tk.filedialog.askdirectory() + '/'
            directoryCurrent1.config(text='Directory Selected: ' + vars[13], anchor="w")


# Run scripts screen
class Page4(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        ### GUI widgets placement, text, and commands. Similar to the ones in Page3 but modified for the PNGs to MP4 script. ###

        label04 = tk.Label(self, fg='#FF0000', text='Resulting PNGs to MP4 program:\n  '
                                                    '(Need to select a directory with PNGs)\n '
                                                    '(Output MP4 is in the same directory as the PNGs!)'
                           )

        # Declares the directory label and updates the diplayed label when it changes
        directoryCurrent2 = tk.Label(self, text='Directory to Convert: ' + vars[13], anchor="w")
        def update():
            directoryCurrent2.config(text='Directory to Convert: ' + vars[13], anchor="w")
            self.after(1000, update)
        update()

        fileSaveName1 = tk.Label(self, text='Save video as:')

        # Declares file name entry filed and put in the default string
        entryFileSaveName = tk.Entry(self)
        entryFileSaveName.insert(0, vars[14])
        vars[14] = entryFileSaveName.get()

        fileSaveButton = tk.Button(self, text='Save file name', command=lambda: printValue(1))

        searchButton3 = tk.Button(self, text='Search Directory to Convert', command=lambda: browseDirectory2())

        startButton2 = tk.Button(self, text='Start', command=lambda: [t2.start(), pb2.start()])
        stopButton2 = tk.Button(self, text='Stop', command=restartProgram)

        pb2 = tk.ttk.Progressbar(self, orient='horizontal', mode='indeterminate', length=100)

        label04.grid(column=0, row=5, columnspan=4, padx=10, pady=10)

        directoryCurrent2.grid(column=1, row=6, columnspan=100, padx=10, pady=20)

        fileSaveName1.grid(column=0, row=7, columnspan=1, padx=10, pady=10)

        entryFileSaveName.grid(column=1, row=7, columnspan=1, padx=5, pady=5)

        fileSaveButton.grid(column=2, row=7, columnspan=1, padx=10, pady=10)

        searchButton3.grid(column=0, row=6, columnspan=1, padx=10, pady=10, sticky='ew')

        startButton2.grid(column=0, row=8, columnspan=1, padx=10, pady=20)
        stopButton2.grid(column=1, row=8, columnspan=1, padx=10, pady=20)

        pb2.grid(column=2, row=8, columnspan=1, padx=10, pady=20)

        def thread2():
            if not os.path.isdir(vars[13]):
                os.makedirs(vars[13])

            generateVideo(
                vars[13],
                vars[14],
                False
            )
            pb2.stop()

        t2 = threading.Thread(target=thread2)

        t2.daemon = True

        def browseDirectory2():
            vars[13] = tk.filedialog.askdirectory()
            directoryCurrent2.config(text='Directory Selected: ' + vars[13], anchor="w")

            if not os.path.isdir(vars[13]):
                os.makedirs(vars[13])

# The main tkinter frame to function as a top menue row of buttons
class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        p1 = Page1(self)
        p2 = Page2(self)
        p3 = Page3(self)
        p4 = Page4(self)

        buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        buttonframe.pack(side='top', fill='x', expand=False)
        container.pack(side='top', fill='both', expand=True)

        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p4.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        # Buttons to show the different pages
        b1 = tk.Button(buttonframe, text='Filter', command= p1.show)
        b2 = tk.Button(buttonframe, text='Tracking', command= p2.show)
        b3 = tk.Button(buttonframe, text='Run Filter and Tracking', command= p3.show)
        b4 = tk.Button(buttonframe, text='Convert to MP4', command= p4.show)

        b1.pack(side='left')
        b2.pack(side='left')
        b3.pack(side='left')
        b4.pack(side='left')

        # Start the GUI on Page1
        p1.show()

# Filtering and trasking algorithm as a function
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
                    directorySelVar):

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

    start_time = time.time()

    # Load data from Aedat file.
    # with AedatFile(r'C:\Users\jerem\Downloads\dvSave-2021_08_24_10_44_21.aedat4') as f:
    with AedatFile(fileSelectVar) as f:
        events = np.hstack([packet for packet in f['events'].numpy()])
        timestamps, x, y, polarities = events['timestamp'], events['x'], events['y'], events['polarity']

        ############
        # Filter 1 #
        ############

        def Filter1(events, min, max):
            index = min
            x_hits = np.empty(0)
            y_hits = np.empty(0)
            while index < max:
                # If a hit is found, write down its x and y, and its current timestamp stored as temp1_time to act as a z variable.
                if (events[index]['polarity'] == 1):
                    temp1_x = events[index]['x']
                    temp1_y = events[index]['y']
                    temp1_time = index
                    index2 = index - time_range
                    # Reset number of found hits
                    hits = 0
                    # Indexes through timestamps with a range from index-time_rance to index+time_range
                    while index2 <= index + time_range:
                        if (events[index2]['polarity'] == 1):
                            temp2_x = events[index2]['x']
                            temp2_y = events[index2]['y']
                            temp2_time = index2
                            # Uses a distance formula to calculate the distance between hits found in time range, accounting for distance through time.
                            distance = math.sqrt(
                                (temp2_x - temp1_x) ** 2 + (temp2_y - temp1_y) ** 2 + (temp1_time - temp2_time) ** 2)
                            # If distance calculated is less then or equal to max_distance, add one to hit variable.
                            if distance <= max_distance:
                                hits += 1
                        index2 += 1
                    # If number of hits is greater then or equal to the set positive value, add it to the plot.
                    if hits >= positive:
                        x_hits = np.append(x_hits, events[index]['x'])
                        y_hits = np.append(y_hits, events[index]['y'])
                index += 1
            return x_hits, y_hits

        # The jit function converts Filter1 into a jitted function, basically re-writting the code in a much faster to run machine code.
        jitted_filter1 = jit(nopython=True)(Filter1)

        ################
        ### FILTER 2 ###
        ################

        # Below this point is a function that takes the plot data and further filters it, removing points that do not have enough neighbors.
        def plot_filter(x_hits, y_hits):
            index = 0
            while index < len(x_hits):
                temp1_x = x_hits[index]
                temp1_y = y_hits[index]
                index2 = 0
                hits = 0
                while index2 < len(x_hits):
                    temp2_x = x_hits[index2]
                    temp2_y = y_hits[index2]
                    distance = math.sqrt((temp2_x - temp1_x) ** 2 + (temp2_y - temp1_y) ** 2)
                    if distance < 5:
                        hits += 1
                    index2 += 1
                if hits < 8:
                    x_hits = np.delete(x_hits, index)
                    y_hits = np.delete(y_hits, index)
                index += 1
            return x_hits, y_hits

        # Jitting filter2 to run faster as well.
        jitted_filter2 = jit(nopython=True)(plot_filter)

        ################
        ### TRACKING ###
        ################

        # Function below takes filtered data and outputs the object center and left, right, top, and bottom bounds
        # min_distance is the minimum distance that the algorithm reaches before it 'gives up' trying to find more pixels and just sets the last pixel hit as the bound
        # min_hits is the minimum number of hits required to actually create a box
        # tolerance is the number of pixels to go past the original bounds to create a box that is bigger then the object
        def tracking2(sample_size, min_distance, min_hits, tolerance, x_hits, y_hits):
            # Arrays for keeping track of hits outside the box
            x_outside = x_hits
            y_outside = y_hits

            # Arrays for keeping track of hits inside the box
            x_inside = np.empty(0)
            y_inside = np.empty(0)

            # Coordinates for center of object
            x_average = 0
            y_average = 0

            # If the sample square goes past the edge of the frame, set the bound of the sample to the edge
            if x_hits[0] + sample_size <= 345:
                sample_right = x_hits[0] + sample_size
            else:
                sample_right = 345
            if x_hits[0] - sample_size >= 1:
                sample_left = x_hits[0] - sample_size
            else:
                sample_left = 1
            if y_hits[0] + sample_size <= 249:
                sample_top = y_hits[0] + sample_size
            else:
                sample_top = 249
            if y_hits[0] - sample_size >= 1:
                sample_bottom = y_hits[0] - sample_size
            else:
                sample_bottom = 1

            # Holds pixels found within the sample square
            sample_hits_x = np.empty(0)
            sample_hits_y = np.empty(0)

            # Find all pixels within the sample square
            index = 0
            while index < len(x_hits):
                if x_hits[index] <= sample_right and x_hits[index] >= sample_left and y_hits[index] <= sample_top and \
                        y_hits[index] >= sample_bottom:
                    sample_hits_x = np.append(sample_hits_x, x_hits[index])
                    sample_hits_y = np.append(sample_hits_y, y_hits[index])
                index += 1

            # Calculate the average for pixels within the sample square to find the center of object
            index = 0
            while index < len(sample_hits_x):
                x_average += sample_hits_x[index]
                y_average += sample_hits_y[index]
                index += 1

            # If there are not enough points within the sample square, return 0 for everything except x_outside and y_outside
            if index < min_hits:
                x_average = 0
                y_average = 0
                x_right = 0
                y_right = 0
                x_left = 0
                y_left = 0
                x_top = 0
                y_top = 0
                x_bottom = 0
                y_bottom = 0

                # Store all pixels that are outside of the sample square in x_outside and y_outside and delete everything inside. The outside pixels will be used as inputs for the next tracking function
                index1 = 0
                while index1 < len(sample_hits_x):
                    index2 = 0
                    while index2 < len(x_outside):
                        if x_outside[index2] == sample_hits_x[index1] and y_outside[index2] == sample_hits_y[index1]:
                            x_outside = np.delete(x_outside, index2)
                            y_outside = np.delete(y_outside, index2)
                        index2 += 1
                    index1 += 1

                return x_average, y_average, x_right, y_right, x_left, y_left, x_top, y_top, x_bottom, y_bottom, x_outside, y_outside, x_inside, y_inside

            # If there's enough pixels, calculate the average
            else:
                x_average /= len(sample_hits_x)
                y_average /= len(sample_hits_y)

            # CODE BELOW FINDS THE RIGHT BOUND
            index1 = int(x_average)  # Start looking at pixels to the right of the center
            flag = True
            no_hit = 0  # Track number of pixels in a row without a hit
            hit_bool = False
            y_right = y_average  # Look at pixels directly to the right of the center

            # Iterate through pixels left to right starting at the center and ending either at the right bound or the edge of the frame
            while flag and index1 < 346:
                hit = False  # Reset hit flag
                # Iterate through all of x_hits to see if there's a hit
                index2 = 0
                while index2 < len(x_hits) and not hit:
                    # If there's a hit, update the x coordinate for the right bound and exit the loop
                    if x_hits[index2] == index1:
                        hit = True
                        x_right = index1
                    # If not, keep looping
                    else:
                        hit = False
                    index2 += 1
                # If there's a hit, reset the no_hit counter since it only counts number of misses in a row
                if hit:
                    no_hit = 0
                    hit_bool = True
                # If there was no hit, increment the misses in a row counter
                else:
                    no_hit += 1
                # If there hasn't been a hit for more then the given minimum distance, give up and exit the loop. x_right is left as the last x coordinate there was a hit
                if no_hit > min_distance:
                    flag = False
                index1 += 1  # We are traveling to the right

            # If the object is cutoff by the edge of the frame, set the right bound to the edge of the frame
            if index1 == 345:
                x_right = 345

            # If there was no hit at all, set the bound to 10 pixels to the right of the center
            if hit_bool == False and x_average + 10 <= 345:
                x_right = x_average + 10

            # CODE BELOW FINDS THE LEFT BOUND
            # See comments for right bound
            index1 = int(x_average)
            flag = True
            no_hit = 0
            hit_bool = False
            y_left = y_average

            while flag and index1 > 0:
                hit = False
                index2 = 0
                while index2 < len(x_hits) and not hit:
                    if x_hits[index2] == index1:
                        hit = True
                        x_left = index1
                    else:
                        hit = False
                    index2 += 1
                if hit:
                    no_hit = 0
                    hit_bool = True
                else:
                    no_hit += 1
                if no_hit > min_distance:
                    flag = False
                index1 -= 1

            if index1 == 1:
                x_left = 1

            if hit_bool == False and x_average - 10 >= 1:
                x_left = x_average - 10

            # CODE BELOW FINDS THE TOP BOUND
            # See comments for right bound
            index1 = int(y_average)
            flag = True
            no_hit = 0
            hit_bool = False
            x_top = x_average

            while flag and index1 > 0:
                hit = False
                index2 = 0
                while index2 < len(y_hits) and not hit:
                    if y_hits[index2] == index1:
                        hit = True
                        y_top = index1
                    else:
                        hit = False
                    index2 += 1
                if hit:
                    no_hit = 0
                    hit_bool = True
                else:
                    no_hit += 1
                if no_hit > min_distance:
                    flag = False
                index1 += 1

            if index1 == 249:
                y_top = 249

            if hit_bool == False and y_average + 10 <= 249:
                y_top = y_average + 10

            # CODE BELOW FINDS THE BOTTOM BOUND
            # See comments for right bound
            index1 = int(y_average)
            flag = True
            no_hit = 0
            hit_bool = False
            x_bottom = x_average

            while flag and index1 > 0:
                hit = False
                index2 = 0
                while index2 < len(y_hits) and not hit:
                    if y_hits[index2] == index1:
                        hit = True
                        y_bottom = index1
                    else:
                        hit = False
                    index2 += 1
                if hit:
                    no_hit = 0
                    hit_bool = True
                else:
                    no_hit += 1
                if no_hit > min_distance:
                    flag = False
                index1 -= 1

            if index1 == 1:
                y_bottom = 1

            if hit_bool == False and y_average - 10 >= 1:
                y_bottom = y_average - 10

            # Apply tolerance (user defined)
            if x_right + tolerance < 345:
                x_right = x_right + tolerance
            if x_left - tolerance > 1:
                x_left = x_left - tolerance
            if y_top + tolerance < 250:
                y_top = y_top + tolerance
            if y_bottom - tolerance > 1:
                y_bottom = y_bottom - tolerance

            # Separate pixels inside and outside of the box that we just found
            index = 0
            while index < len(x_hits):
                if x_hits[index] <= x_right and x_hits[index] >= x_left and y_hits[index] <= y_top and y_hits[
                    index] >= y_bottom:
                    index1 = 0
                    while index1 < len(x_outside):
                        if x_outside[index1] == x_hits[index] and y_outside[index1] == y_hits[index]:
                            x_outside = np.delete(x_outside, index1)
                            y_outside = np.delete(y_outside, index1)
                            x_inside = np.append(x_inside, x_hits[index])
                            y_inside = np.append(y_inside, y_hits[index])
                        index1 += 1
                index += 1

            # Return the coordinates for the center of the object and the right, left, top, and bottom bounds
            # Return the pixels that are inside and the pixels that are outside the box
            return x_average, y_average, x_right, y_right, x_left, y_left, x_top, y_top, x_bottom, y_bottom, x_outside, y_outside, x_inside, y_inside

        jitted_filter5 = jit(nopython=True)(tracking2)

        ############################
        # Filter10 For -1 Polarity #
        ############################

        def Filter10(events, min, max):
            index = min
            x_hits = np.empty(0)
            y_hits = np.empty(0)
            while index < max:
                # If a hit is found, write down its x and y, and its current timestamp stored as temp1_time to act as a z variable.
                if events[index]['polarity'] == 0:
                    temp1_x = events[index]['x']
                    temp1_y = events[index]['y']
                    temp1_time = index
                    index2 = index - time_range
                    # Reset number of found hits
                    hits = 0
                    # Indexes through timestamps with a range from index-time_rance to index+time_range
                    while index2 <= index + time_range:
                        if events[index2]['polarity'] == 0:
                            temp2_x = events[index2]['x']
                            temp2_y = events[index2]['y']
                            temp2_time = index2
                            # Uses a distance formula to calculate the distance between hits found in time range, accounting for distance through time.
                            distance = math.sqrt(
                                (temp2_x - temp1_x) ** 2 + (temp2_y - temp1_y) ** 2 + (temp1_time - temp2_time) ** 2)
                            # If distance calculated is less then or equal to max_distance, add one to hit variable.
                            if distance <= max_distance:
                                hits += 1
                        index2 += 1
                    # If number of hits is greater then or equal to the set positive value, add it to the plot.
                    if hits >= positive:
                        x_hits = np.append(x_hits, events[index]['x'])
                        y_hits = np.append(y_hits, events[index]['y'])
                index += 1
            return x_hits, y_hits

        # The jit function converts Filter10 into a jitted function, basically re-writting the code in a much faster to run machine code.
        jitted_filter10 = jit(nopython=True)(Filter10)

        # Below here is a while loop that loops through the video data in increments.
        index3 = 0
        index3max = len(timestamps) / increment - 5
        while index3 < index3max:
            # Call the first filter and return the data to x_hits and y_hits.
            x_hits, y_hits = jitted_filter1(events, min, max)

            # Call filter10 and return the data to x_hits0 and y_hits0.
            x_hits0, y_hits0 = jitted_filter10(events, min, max)

            # Plot the data from the first filter in pink.
            plt.scatter(x_hits, y_hits, s=0.5, c='pink')

            # Plot the data from the first (-1) filter in skyblue.
            plt.scatter(x_hits0, y_hits0, s=0.5, c='skyblue')

            x_hits = np.array(x_hits)
            y_hits = np.array(y_hits)

            x_hits0 = np.array(x_hits0)
            y_hits0 = np.array(y_hits0)

            print('Total points on plot after first (+1) filter: ', len(x_hits))
            print('Total points on plot after first (-1) filter: ', len(x_hits0))

            index = 0
            while index < 7:
                x_hits, y_hits = jitted_filter2(x_hits, y_hits)
                x_hits0, y_hits0 = jitted_filter2(x_hits0, y_hits0)
                index += 1

            # Combine pixels of 1 and -1 polarity
            x_combined = np.concatenate((x_hits, x_hits0))
            y_combined = np.concatenate((y_hits, y_hits0))

            # Prints time to console
            total_time = round((time.time() - start_time), 2)
            print('Total points on plot after second (+1) filter: ', len(x_hits))
            print('Total points on plot after second (-1) filter: ', len(x_hits0))
            print('Execution time: %s seconds' % (total_time))
            print('On Image #', index3)

            # Plots data
            bisque_patch = mpatches.Patch(color='pink', label='First (+1) Filter output')
            red_patch = mpatches.Patch(color='red', label='Second (+1) Filter output')
            skyblue_patch = mpatches.Patch(color='skyblue', label='First (-1) Filter output')
            blue_patch = mpatches.Patch(color='blue', label='Second (-1) Filter output')
            title = 'Time Increment: ' + str(min) + ' to ' + str(max)
            plt.title(title)
            plt.legend(handles=[red_patch, bisque_patch, blue_patch, skyblue_patch], bbox_to_anchor=(1, 1), loc=2)
            plt.xlim(0, 350)
            plt.ylim(250, 0)
            plt.scatter(x_hits, y_hits, s=0.5, c='pink')
            plt.scatter(x_hits0, y_hits0, s=0.5, c='skyblue')

            # temporary variables for holding the output of the last tracking function
            temp_x_hits = x_combined
            temp_y_hits = y_combined

            # Positive pixels inside all of the boxes drawn
            x_inside1_p = np.empty(0)
            y_inside1_p = np.empty(0)

            # Negative pixels inside all of the boxes drawn
            x_inside1_n = np.empty(0)
            y_inside1_n = np.empty(0)

            # Execute tracking function until we hit a certain number of loops or there are no pixels left to track
            index = 0
            while len(temp_x_hits) > 0 and index < max_tracking_iterations:
                x_object, y_object, x_right, y_right, x_left, y_left, x_top, y_top, x_bottom, y_bottom, x_outside, y_outside, x_inside, y_inside = jitted_filter5(
                    sample_size, min_distance, min_hits, tolerance, temp_x_hits, temp_y_hits)

                # Use updated list of pixels for the next function (will either have pixels deleted from the sample square not having enough pixels or from a box that was already drawn)
                temp_x_hits = x_outside
                temp_y_hits = y_outside

                # If there wasn't enough pixels, don't draw a box
                no_object = False
                if x_object == 0 and y_object == 0:
                    no_object = True

                if not no_object:
                    # Draw square as well as the center, top, bottom, left, and right
                    plt.scatter(x_object, y_object, s=10, c='g')
                    plt.scatter(x_right, y_right, s=10, c='g')
                    plt.scatter(x_left, y_left, s=10, c='g')
                    plt.scatter(x_top, y_top, s=10, c='g')
                    plt.scatter(x_bottom, y_bottom, s=10, c='g')
                    rectangle = plt.Rectangle((x_left, y_bottom), x_right - x_left, y_top - y_bottom, fc='none',
                                              ec='green')  # Draw rectangle around the object
                    plt.gca().add_patch(rectangle)

                    # Find positive pixels inside all of the boxes drawn
                    index1 = 0
                    while index1 < len(x_hits):
                        if x_hits[index1] <= x_right and x_hits[index1] >= x_left and y_hits[index1] <= y_top and \
                                y_hits[index1] >= y_bottom:
                            x_inside1_p = np.append(x_inside1_p, x_hits[index1])
                            y_inside1_p = np.append(y_inside1_p, y_hits[index1])
                        index1 += 1

                    # Find negative pixels inside all of the boxes drawn
                    index1 = 0
                    while index1 < len(x_hits0):
                        if x_hits0[index1] <= x_right and x_hits0[index1] >= x_left and y_hits0[index1] <= y_top and \
                                y_hits0[index1] >= y_bottom:
                            x_inside1_n = np.append(x_inside1_n, x_hits0[index1])
                            y_inside1_n = np.append(y_inside1_n, y_hits0[index1])
                        index1 += 1
                index += 1

            # Highlight pixels inside of boxes
            plt.scatter(x_inside1_p, y_inside1_p, s=0.5, c='r')
            plt.scatter(x_inside1_n, y_inside1_n, s=0.5, c='b')
            plt.savefig(directorySelVar + str(index3), bbox_inches='tight')
            print(directorySelVar + str(index3) + '.png')
            plt.clf()

            # Increment time.
            min = min + increment
            max = max + increment
            index3 += 1
            print(index3max)


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

    output = cv2.VideoWriter(file_path + '/' + output_name + '.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 15, size)
    print("MP4 file saved: " + file_path + '/' + output_name + '.mp4')

    for i in range(len(img_array)):
        output.write(img_array[i])
    output.release()

    # The following code removes all png files from the directory to prevent old images being added to videos
    if del_toggle == True:
        for filename in glob.glob(file_path + '*.png'):
            os.remove(filename)

# Main loop for tkinter to function
if __name__ == '__main__':
    root = tk.Tk()
    main = MainView(root)
    main.pack(side='top', fill='both', expand=True)
    root.geometry('600x350')
    root.grid()
    root.mainloop()
