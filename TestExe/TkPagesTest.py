import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import math as math
# numba is a library that must be install by running "pip install numba" It takes a function and re-writes in machine code to run extremely fast. It works best if numpy arrays are used.
from numba import jit, njit, vectorize
from dv import AedatFile
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
import threading

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

import re
#re allows for numerical resorting to ensure all files are read in order
#cv2 reads files in alphabetical order(not numerical) so 10 is read before 9

import os


# Skeleton built off from:
# https://stackoverflow.com/questions/14817210/using-buttons-in-tkinter-to-navigate-to-different-pages-of-the-application


# Restarts the program
def restartProgram():
    root.destroy()
    os.startfile("TkPagesTest.py")
    os.startfile("TkPagesTest.exe")

# Text color testing
class color:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

# Makes variables avaliable on all classes
class vars():
    def __init__(self, *args, **kwargs):

        self.time_range = int

        self.positive = int

        self.max_distance = int

        self.increment = int

        self.min = int

        self.max = int



        self.sample_size = int

        self.min_distance = int

        self.min_hits = int

        self.tolerance = int

        self.max_tracking_iterations = int



        self.fileDestination = ''

        self.directorySel = ''
        self.fileNameSet = ''

# Default values of variables
vars.time_range = 7
vars.positive = 2
vars.max_distance = 10
vars.increment = 10000
vars.min = 0
vars.max = 40000

vars.sample_size = 40
vars.min_distance = 10
vars.min_hits = 50
vars.tolerance = 5
vars.max_tracking_iterations = 50

vars.fileDestination = '/'
vars.directorySel = '/'
vars.fileNameSet = 'Default'



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

        # Reset filter variables to default values
        def resetToDefaultValues():
            vars.time_range = 7
            vars.positive = 2
            vars.max_distance = 10
            vars.increment = 10000
            vars.min = 0
            vars.max = 40000
            print('Filter reseted to defaut')
            entryTimeR.delete(0, 'end')
            entryTimeR.insert(0, vars.time_range)
            entryPositive.delete(0, 'end')
            entryPositive.insert(0, vars.positive)
            entryMaxD.delete(0, 'end')
            entryMaxD.insert(0, vars.max_distance)
            entryIncr.delete(0, 'end')
            entryIncr.insert(0, vars.increment)
            entryMin.delete(0, 'end')
            entryMin.insert(0, vars.min)
            entryMax.delete(0, 'end')
            entryMax.insert(0, vars.max)



        label1 = tk.Label(self, text='Time range')
        label2 = tk.Label(self, text='Positive hits')
        label3 = tk.Label(self, text='Max distance')
        label4 = tk.Label(self, text='Increment')
        label5 = tk.Label(self, text='Min')
        label6 = tk.Label(self, text='Max')

        label1.grid(column=0, row=0, columnspan=1, padx=5, pady=5)
        label2.grid(column=0, row=1, columnspan=1, padx=5, pady=5)
        label3.grid(column=0, row=2, columnspan=1, padx=5, pady=5)
        label4.grid(column=0, row=3, columnspan=1, padx=5, pady=5)
        label5.grid(column=0, row=4, columnspan=1, padx=5, pady=5)
        label6.grid(column=0, row=5, columnspan=1, padx=5, pady=5)

        entryTimeR = tk.Entry(self)
        entryPositive = tk.Entry(self)
        entryMaxD = tk.Entry(self)
        entryIncr = tk.Entry(self)
        entryMin = tk.Entry(self)
        entryMax = tk.Entry(self)

        entryTimeR.insert(0, vars.time_range)
        entryPositive.insert(0, vars.positive)
        entryMaxD.insert(0, vars.max_distance)
        entryIncr.insert(0, vars.increment)
        entryMin.insert(0, vars.min)
        entryMax.insert(0, vars.max)

        vars.time_range = entryTimeR.get()
        vars.positive = entryPositive.get()
        vars.max_distance = entryMaxD.get()
        vars.increment = entryIncr.get()
        vars.min = entryMin.get()
        vars.max = entryMax.get()

        entryTimeR.grid(column=1, row=0, columnspan=1, padx=5, pady=5)
        entryPositive.grid(column=1, row=1, columnspan=1, padx=5, pady=5)
        entryMaxD.grid(column=1, row=2, columnspan=1, padx=5, pady=5)
        entryIncr.grid(column=1, row=3, columnspan=1, padx=5, pady=5)
        entryMin.grid(column=1, row=4, columnspan=1, padx=5, pady=5)
        entryMax.grid(column=1, row=5, columnspan=1, padx=5, pady=5)

        tk.Button(self, text="Save", command=lambda: printValue(1)).grid(column=2, row=0, columnspan=1, padx=5, pady=5)
        tk.Button(self, text="Save", command=lambda: printValue(2)).grid(column=2, row=1, columnspan=1, padx=5, pady=5)
        tk.Button(self, text="Save", command=lambda: printValue(3)).grid(column=2, row=2, columnspan=1, padx=5, pady=5)
        tk.Button(self, text="Save", command=lambda: printValue(4)).grid(column=2, row=3, columnspan=1, padx=5, pady=5)
        tk.Button(self, text="Save", command=lambda: printValue(5)).grid(column=2, row=4, columnspan=1, padx=5, pady=5)
        tk.Button(self, text="Save", command=lambda: printValue(6)).grid(column=2, row=5, columnspan=1, padx=5, pady=5)

        tk.Button(self, text="Reset filter to default values", command=lambda: resetToDefaultValues()).grid(column=3,
                                                                                                             row=7,
                                                                                                             columnspan=1,
                                                                                                             padx=5,
                                                                                                             pady=5)

        def regMsg(rowNum):
            label01 = tk.Label(self, text='Saved!')
            label01.grid(column=3, row=rowNum - 1, pady=5)
            self.after(500, lambda: label01.grid_remove())

        def printValue(varNum):
            if varNum == 1:
                vars.time_range = entryTimeR.get()
                regMsg(varNum)
                print(vars.time_range)
            if varNum == 2:
                vars.positive = entryPositive.get()
                regMsg(varNum)
                print(vars.positive)
            if varNum == 3:
                vars.max_distance = entryMaxD.get()
                regMsg(varNum)
                print(vars.max_distance)
            if varNum == 4:
                vars.increment = entryIncr.get()
                regMsg(varNum)
                print(vars.increment)
            if varNum == 5:
                vars.min = entryMin.get()
                regMsg(varNum)
                print(vars.min)
            if varNum == 6:
                vars.max = entryMax.get()
                regMsg(varNum)
                print(vars.max)

# Tracking variables screen
class Page2(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        def resetToDefaultValues():
            vars.sample_size = 40
            vars.min_distance = 10
            vars.min_hits = 50
            vars.tolerance = 5
            vars.max_tracking_iterations = 50
            print('Tracking reseted to defaut')
            entrySampleS.delete(0, 'end')
            entrySampleS.insert(0, vars.sample_size)
            entryMinD.delete(0, 'end')
            entryMinD.insert(0, vars.min_distance)
            entryMinH.delete(0, 'end')
            entryMinH.insert(0, vars.min_hits)
            entryTolerance.delete(0, 'end')
            entryTolerance.insert(0, vars.tolerance)
            entryMaxTI.delete(0, 'end')
            entryMaxTI.insert(0, vars.max_tracking_iterations)

        label1 = tk.Label(self, text='Sample size')
        label2 = tk.Label(self, text='Min distance')
        label3 = tk.Label(self, text='Min hits')
        label4 = tk.Label(self, text='Tolarance')
        label5 = tk.Label(self, text='Max tracking iterations')

        label1.grid(column=0, row=0, columnspan=1, padx=5, pady=5)
        label2.grid(column=0, row=1, columnspan=1, padx=5, pady=5)
        label3.grid(column=0, row=2, columnspan=1, padx=5, pady=5)
        label4.grid(column=0, row=3, columnspan=1, padx=5, pady=5)
        label5.grid(column=0, row=4, columnspan=1, padx=5, pady=5)

        entrySampleS = tk.Entry(self)
        entryMinD = tk.Entry(self)
        entryMinH = tk.Entry(self)
        entryTolerance = tk.Entry(self)
        entryMaxTI= tk.Entry(self)

        entrySampleS.insert(0, vars.sample_size)
        entryMinD.insert(0, vars.min_distance)
        entryMinH.insert(0, vars.min_hits)
        entryTolerance.insert(0, vars.tolerance)
        entryMaxTI.insert(0, vars.max_tracking_iterations)

        vars.sample_size = entrySampleS.get()
        vars.min_distance = entryMinD.get()
        vars.min_hits = entryMinH.get()
        vars.tolerance = entryTolerance.get()
        vars.max_tracking_iterations = entryMaxTI.get()

        entrySampleS.grid(column=1, row=0, columnspan=1, padx=5, pady=5)
        entryMinD.grid(column=1, row=1, columnspan=1, padx=5, pady=5)
        entryMinH.grid(column=1, row=2, columnspan=1, padx=5, pady=5)
        entryTolerance.grid(column=1, row=3, columnspan=1, padx=5, pady=5)
        entryMaxTI.grid(column=1, row=4, columnspan=1, padx=5, pady=5)

        tk.Button(self, text="Save", command=lambda: printValue(1)).grid(column=2, row=0, columnspan=1, padx=5, pady=5)
        tk.Button(self, text="Save", command=lambda: printValue(2)).grid(column=2, row=1, columnspan=1, padx=5, pady=5)
        tk.Button(self, text="Save", command=lambda: printValue(3)).grid(column=2, row=2, columnspan=1, padx=5, pady=5)
        tk.Button(self, text="Save", command=lambda: printValue(4)).grid(column=2, row=3, columnspan=1, padx=5, pady=5)
        tk.Button(self, text="Save", command=lambda: printValue(5)).grid(column=2, row=4, columnspan=1, padx=5, pady=5)

        tk.Button(self, text="Reset tracking to default values", command=lambda: resetToDefaultValues()).grid(column=3,
                                                                                                             row=7,
                                                                                                             columnspan=1,
                                                                                                             padx=5,
                                                                                                             pady=5)

        def regMsg(rowNum):
            label01 = tk.Label(self, text='Saved!')
            label01.grid(column=3, row=rowNum - 1, pady=5)
            self.after(500, lambda: label01.grid_remove())

        def printValue(varNum):
            if varNum == 1:
                vars.sample_size = entrySampleS.get()
                regMsg(varNum)
                print(vars.sample_size)
            if varNum == 2:
                vars.min_distance = entryMinD.get()
                regMsg(varNum)
                print(vars.min_distance)
            if varNum == 3:
                vars.min_hits = entryMinH.get()
                regMsg(varNum)
                print(vars.min_hits)
            if varNum == 4:
                vars.tolerance = entryTolerance.get()
                regMsg(varNum)
                print(vars.tolerance)
            if varNum == 5:
                vars.max_tracking_iterations = entryMaxTI.get()
                regMsg(varNum)
                print(vars.max_tracking_iterations)

# Run scripts screen
class Page3(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        def browseFiles1():
            fileName = filedialog.askopenfilename(initialdir = "/", title = "Select a File", filetypes = (("aedat4 files", "*.aedat4*"), ("all files", "*.*")))
            vars.fileDestination = fileName

            if fileName !='':
                fileCurrent.config(text="File Selected: " + fileName)
                startButton1.config(state="normal")
                stopButton1.config(state="normal")

        fileCurrent = tk.Label(self, text="Select a File: ")
        fileCurrent.grid(column=3, row=1, columnspan=10, padx=10, pady=20)

        tk.Button(self, text="Search File", command=lambda: browseFiles1()).grid(column=0, row=1, columnspan=1, padx=10, pady=20, sticky="ew")

        def browseDirectory1():
            directoryName = filedialog.askdirectory()
            vars.directorySel = directoryName
            directoryCurrent.config(text="File Selected: " + directoryName)
            
            if directoryName != '':
                startButton2.config(state="normal")
                stopButton2.config(state="normal")

        directoryCurrent = tk.Label(self, text="Select a Directory: ")
        directoryCurrent.grid(column=3, row=6, columnspan=10, padx=10, pady=20)

        tk.Button(self, text="Search Directory", command=lambda: browseDirectory1()).grid(column=0, row=6, columnspan=1, padx=10, pady=20, sticky="ew")

        def regMsg(rowNum):
            label01 = tk.Label(self, text='Saved!')
            label01.grid(column=3, row=rowNum, pady=5)
            self.after(500, lambda: label01.grid_remove())

        def printValue(varNum):
            if varNum == 7:
                vars.fileNameSet = entryFileSaveName.get()
                regMsg(varNum)
                print(vars.fileNameSet)

        tk.Label(self, text='Save video as:').grid(column=0, row=7, columnspan=1, padx=10, pady=10)
        entryFileSaveName = tk.Entry(self)
        entryFileSaveName.insert(0, vars.fileNameSet)
        vars.fileNameSet = entryFileSaveName.get()
        entryFileSaveName.grid(column=1, row=7, columnspan=1, padx=5, pady=5)
        tk.Button(self, text="Save file name", command=lambda: printValue(7)).grid(column=2, row=7, columnspan=1, padx=5, pady=5)

        def thread1():
            filterTrackCode(vars.time_range,
                     vars.positive,
                     vars.max_distance,
                     vars.increment,
                     vars.min,
                     vars.max,
                     vars.sample_size,
                     vars.min_distance,
                     vars.min_hits,
                     vars.tolerance,
                     vars.max_tracking_iterations,
                     vars.fileDestination)
            pb1.stop()

        def thread2():
            generateVideo(
                vars.directorySel,
                vars.fileNameSet,
                False
            )
            pb2.stop()

        t1 = threading.Thread(target=thread1)
        t2 = threading.Thread(target=thread2)

        t1.daemon = True
        t2.daemon = True

        tk.Label(self, fg='#FF0000', text='Filter and tracking program:\n '
                            '(Need to select .aedat4 file before starting filter/track!)\n '
                            '(Output is in the same directory as this script!)'
                 ).grid(column=1, row=0, columnspan=1, padx=10, pady=10)
        tk.Label(self, fg='#FF0000', text='Resulting PNGs to MP4 program:\n  '
                            '(Need to select a directory with PNGs)\n '
                            '(Output is in the same directory as this script!)'
                 ).grid(column=1, row=5, columnspan=1, padx=10, pady=10)


        startButton1 = tk.Button(self, text="Start", command=lambda: [t1.start(), pb1.start()], state="disabled")
        stopButton1 = tk.Button(self, text="Stop", command=restartProgram, state="disabled")
        startButton2 = tk.Button(self, text="Start", command=lambda: [t2.start(), pb2.start()], state="disabled")
        stopButton2 = tk.Button(self, text="Stop", command=restartProgram, state="disabled")

        startButton1.grid(column=0, row=3, columnspan=1, padx=10, pady=20)
        stopButton1.grid(column=1, row=3, columnspan=1, padx=10, pady=20)
        startButton2.grid(column=0, row=8, columnspan=1, padx=10, pady=20)
        stopButton2.grid(column=1, row=8, columnspan=1, padx=10, pady=20)

        pb1 = ttk.Progressbar(self, orient='horizontal', mode='indeterminate', length=100)
        pb2 = ttk.Progressbar(self, orient='horizontal', mode='indeterminate', length=100)

        pb1.grid(column=3, row=3, columnspan=2, padx=10, pady=20)
        pb2.grid(column=3, row=8, columnspan=2, padx=10, pady=20)




class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        p1 = Page1(self)
        p2 = Page2(self)
        p3 = Page3(self)

        buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        buttonframe.pack(side="top", fill="x", expand=False)
        container.pack(side="top", fill="both", expand=True)

        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)

        b1 = tk.Button(buttonframe, text="Filter", command=p1.show)
        b2 = tk.Button(buttonframe, text="Tracking", command=p2.show)
        b3 = tk.Button(buttonframe, text="Run Programs", command=p3.show)

        b1.pack(side="left")
        b2.pack(side="left")
        b3.pack(side="left")

        p1.show()


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
             fileDesVar):

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
    # with AedatFile(r"C:\Users\jerem\Downloads\dvSave-2021_08_24_10_44_21.aedat4") as f:
    with AedatFile(fileDesVar) as f:
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
        # min_distance is the minimum distance that the algorithm reaches before it "gives up" trying to find more pixels and just sets the last pixel hit as the bound
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

            print("Total points on plot after first (+1) filter: ", len(x_hits))
            print("Total points on plot after first (-1) filter: ", len(x_hits0))

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
            print("Total points on plot after second (+1) filter: ", len(x_hits))
            print("Total points on plot after second (-1) filter: ", len(x_hits0))
            print("Execution time: %s seconds" % (total_time))
            print("On Image #", index3)

            # Plots data
            bisque_patch = mpatches.Patch(color='pink', label='First (+1) Filter output')
            red_patch = mpatches.Patch(color='red', label='Second (+1) Filter output')
            skyblue_patch = mpatches.Patch(color='skyblue', label='First (-1) Filter output')
            blue_patch = mpatches.Patch(color='blue', label='Second (-1) Filter output')
            title = "Time Increment: " + str(min) + " to " + str(max)
            plt.title(title)
            plt.legend(handles=[red_patch, bisque_patch, blue_patch, skyblue_patch], bbox_to_anchor=(1,1), loc=2)
            plt.xlim(0, 350)
            plt.ylim(0, 250)
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
                                              ec="green")  # Draw rectangle around the object
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
            plt.savefig(str(index3), bbox_inches='tight')
            plt.clf()

            # Increment time.
            min = min + increment
            max = max + increment
            index3 += 1
            print(index3max)

#NOTE: CODE UNORIGINAL, numericalSort function obtained from
# https://stackoverflow.com/questions/12093940/reading-files-in-a-particular-order-in-python
#User: Martijn Pieters on Aug 23, 2012
def generateVideo(file_path, output_name, del_toggle):
    numbers = re.compile(r'(\d+)')

    def numericalSort(value):
        parts = numbers.split(value)
        parts[1::2] = map(int, parts[1::2])
        return parts

    # image reading code obtained from
    # https://theailearner.com/2018/10/15/creating-video-from-images-using-opencv-python/
    # User: kang&atul on 15 Oct 2018
    img_array = []  # numpy array to store image information
    for filename in sorted(glob.glob(file_path + "\*.png"), key=numericalSort):
        img = cv2.imread(filename)
        print("Reading image: ", filename)
        height, width, layers = img.shape
        size = (width, height)
        img_array.append(img)

    output = cv2.VideoWriter(output_name + '.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 15, size)

    for i in range(len(img_array)):
        output.write(img_array[i])
    output.release()

    # the following code removes all png files from the directory to prevent old images being added to videos
    if del_toggle == True:
        for filename in glob.glob(file_path  + "*.png"):
            os.remove(filename)
    

if __name__ == "__main__":
    root = tk.Tk()
    main = MainView(root)
    main.pack(side="top", fill="both", expand=True)
    root.geometry("1100x500")
    root.grid()
    root.mainloop()
