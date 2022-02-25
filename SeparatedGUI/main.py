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

# Import seperate files
import filterTracking as FiTr
import utilityScripts as UtSc

# Allows the script to interact with the os
import os


# Tkinter skeleton built off from:
# https://stackoverflow.com/questions/14817210/using-buttons-in-tkinter-to-navigate-to-different-pages-of-the-application

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
                 train_split
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
               'Object_Name',       # test/train parent directory
               0.8,                 # test/train percentage
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
        v1.train_split              # 16
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
         ]

# Array of string names of the variables
varName = entry.copy()

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
            print(f'{varName[num]} = {vars[num]}')

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
            print(f'{varName[num]} = {vars[num]}')

# Run scripts screen
class Page3(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        ### GUI widgets placement, text, and commands. ###

        # Initializing the variables for the option to turn off the tracker or legend
        option1 = tk.IntVar() # Tracker
        option2 = tk.IntVar() # Legend

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

        # Options to turn off tracking or the legend
        checkBox1 = tk.Checkbutton(self, text='Turn off the tracker', variable=option1, onvalue=1, offvalue=0)
        checkBox2 = tk.Checkbutton(self, text='Turn off the legend', variable=option2, onvalue=1, offvalue=0)

        # Buttons to start and stop the algorithem.
        # They turn on when the user selects a file.
        # The stop restarts the program to stop the thread
        startButton1 = tk.Button(self, text='Start', command=lambda: [t1.start(), pb1.start()], state='disabled')
        stopButton1 = tk.Button(self, text='Stop', command=restartProgram, state='disabled')

        # A visual progressbar widget
        pb1 = tk.ttk.Progressbar(self, orient='horizontal', mode='indeterminate', length=100)

        # Grid location of entry fields, labels, and buttons
        label03.grid(column=0, row=0, columnspan=4, padx=10, pady=10)

        fileCurrent1.grid(column=1, row=1, columnspan=100, padx=10, pady=10)
        directoryCurrent1.grid(column=1, row=3, columnspan=100, padx=10, pady=10)

        searchButton1.grid(column=0, row=1, columnspan=1, padx=10, pady=10, sticky='ew')
        searchButton2.grid(column=0, row=3, columnspan=1, padx=10, pady=10, sticky='ew')

        checkBox1.grid(column=0, row=5, columnspan=1, padx=10, pady=10)
        checkBox2.grid(column=0, row=6, columnspan=1, padx=10, pady=10)

        startButton1.grid(column=0, row=7, columnspan=1, padx=10, pady=10)
        stopButton1.grid(column=1, row=7, columnspan=1, padx=10, pady=10)

        pb1.grid(column=2, row=7, columnspan=2, padx=10, pady=10)

        # Defining the thread for the filter and tracking algorithm
        def thread1():
            # Creates file directory if it does not exist
            if not os.path.isdir(vars[13]):
                os.makedirs(vars[13])

            # Input variables for the filter and tracking algorithm
            FiTr.filterTrackCode(vars[1],
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
                            vars[13],
                            option1.get(),
                            option2.get(),
                            )

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

# Run PNGs to MP4 screen
class Page4(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        ### GUI widgets placement, text, and commands. Similar to the ones in Page3 but modified for the PNGs to MP4 script. ###

        option3 = tk.IntVar()  # Delete PNGs

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

        fileSaveButton = tk.Button(self, text='Save file name', command=lambda: printValue(14))

        searchButton3 = tk.Button(self, text='Search directory to convert', command=lambda: browseDirectory2())

        checkBox3 = tk.Checkbutton(self, text='Delete PNGs after making the video PERMANENTLY. (CAREFUL!)', variable=option3, onvalue=1, offvalue=0, fg='red')

        startButton2 = tk.Button(self, text='Start', command=lambda: [t2.start(), pb2.start()])
        stopButton2 = tk.Button(self, text='Stop', command=restartProgram)

        pb2 = tk.ttk.Progressbar(self, orient='horizontal', mode='indeterminate', length=100)

        label04.grid(column=0, row=5, columnspan=3, padx=10, pady=10)

        directoryCurrent2.grid(column=1, row=6, columnspan=100, padx=10, pady=10)

        fileSaveName1.grid(column=0, row=7, columnspan=1, padx=10, pady=10)

        entryFileSaveName.grid(column=1, row=7, columnspan=1, padx=5, pady=5)

        fileSaveButton.grid(column=2, row=7, columnspan=1, padx=10, pady=10)

        searchButton3.grid(column=0, row=6, columnspan=1, padx=10, pady=10, sticky='ew')

        checkBox3.grid(column=0, row=8, columnspan=3, padx=10, pady=10)

        startButton2.grid(column=0, row=9, columnspan=1, padx=10, pady=10)
        stopButton2.grid(column=1, row=9, columnspan=1, padx=10, pady=10)

        pb2.grid(column=2, row=9, columnspan=1, padx=10, pady=10)

        def thread2():
            if not os.path.isdir(vars[13]):
                os.makedirs(vars[13])

            UtSc.generateVideo(vars[13],
                          vars[14],
                          option3.get(),
            )
            pb2.stop()

        t2 = threading.Thread(target=thread2)

        t2.daemon = True

        def browseDirectory2():
            vars[13] = tk.filedialog.askdirectory() + '/'
            directoryCurrent2.config(text='Directory Selected: ' + vars[13], anchor="w")

            if not os.path.isdir(vars[13]):
                os.makedirs(vars[13])

        # Save entry and display saved message
        def printValue(num):
            vars[num] = entryFileSaveName.get()
            label01 = tk.Label(self, text='Saved!', fg='green', bg='white')
            label01.grid(column=3, row=num - 7, pady=5)
            self.after(500, lambda: label01.grid_remove())
            print(f'{varName[num]} = {vars[num]}')

# Run test/train split screen
class Page5(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        ### GUI widgets placement, text, and commands. Similar to the ones in Page4 but modified for the split data script. ###

        label05 = tk.Label(self, fg='#FF0000', text='Split resulting PNGs to testing and training sets:\n  '
                                                    '(Need to select a directory with PNGs)\n '
                                                    '(Output directory is in the same folder as PNGs)'
                           )

        # Declares the directory label and updates the diplayed label when it changes
        directoryCurrent3 = tk.Label(self, text='Directory to Split: ' + vars[13], anchor="w")
        def update():
            directoryCurrent3.config(text='Directory to Split: ' + vars[13], anchor="w")
            self.after(1000, update)
        update()

        dirSaveNameLabel = tk.Label(self, text='Split result directory name:')
        splitPercentLabel = tk.Label(self, text='Split percent to be for training:')

        # Declares directory object name entry filed and put in the default string
        entry[15] = tk.Entry(self)
        entry[15].insert(0, vars[15])
        vars[15] = entry[15].get()

        # Declares percent to split entry filed and put in the default value
        entry[16] = tk.Entry(self)
        entry[16].insert(0, vars[16])
        vars[16] = entry[16].get()

        dirSaveButton = tk.Button(self, text='Save directory name', command=lambda: printValue(15))
        splitSaveButton = tk.Button(self, text='Save percent', command=lambda: printValue(16))

        searchButton3 = tk.Button(self, text='Search Directory to Split', command=lambda: browseDirectory3())

        startButton2 = tk.Button(self, text='Start', command=lambda: [t3.start(), pb3.start()])
        stopButton2 = tk.Button(self, text='Stop', command=restartProgram)

        pb3 = tk.ttk.Progressbar(self, orient='horizontal', mode='indeterminate', length=100)

        label05.grid(column=0, row=5, columnspan=3, padx=10, pady=10)

        directoryCurrent3.grid(column=1, row=6, columnspan=100, padx=10, pady=10)

        dirSaveNameLabel.grid(column=0, row=7, columnspan=1, padx=10, pady=10)
        splitPercentLabel.grid(column=0, row=8, columnspan=1, padx=10, pady=10)

        entry[15].grid(column=1, row=7, columnspan=1, padx=5, pady=5)
        entry[16].grid(column=1, row=8, columnspan=1, padx=5, pady=5)

        dirSaveButton.grid(column=2, row=7, columnspan=1, padx=10, pady=10)
        splitSaveButton.grid(column=2, row=8, columnspan=1, padx=10, pady=10)

        searchButton3.grid(column=0, row=6, columnspan=1, padx=10, pady=10, sticky='ew')

        startButton2.grid(column=0, row=9, columnspan=1, padx=10, pady=10)
        stopButton2.grid(column=1, row=9, columnspan=1, padx=10, pady=10)

        pb3.grid(column=2, row=9, columnspan=1, padx=10, pady=10)

        def thread3():
            if not os.path.isdir(vars[13]):
                os.makedirs(vars[13])

            UtSc.test_train_split(vars[13],
                             vars[15],
                             float(vars[16]),
            )
            pb3.stop()
            print(vars[13])

        t3 = threading.Thread(target=thread3)

        t3.daemon = True

        def browseDirectory3():
            vars[13] = tk.filedialog.askdirectory() + '/'
            directoryCurrent3.config(text='Directory Selected: ' + vars[13], anchor="w")

            if not os.path.isdir(vars[13]):
                os.makedirs(vars[13])

        # Save entry and display saved message
        def printValue(num):
            vars[num] = entry[num].get()
            label01 = tk.Label(self, text='Saved!', fg='green', bg='white')
            label01.grid(column=3, row=num - 8, pady=5)
            self.after(500, lambda: label01.grid_remove())
            print(f'{varName[num]} = {vars[num]}')

# Help screen
class Page6(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)



# The main tkinter frame to function as a top menu row of buttons
class MainView(tk.Frame):
    def __init__(self, *args, **kwargs):
        tk.Frame.__init__(self, *args, **kwargs)
        p1 = Page1(self)
        p2 = Page2(self)
        p3 = Page3(self)
        p4 = Page4(self)
        p5 = Page5(self)
        p6 = Page6(self)


        buttonframe = tk.Frame(self)
        container = tk.Frame(self)
        buttonframe.pack(side='top', fill='x', expand=False)
        container.pack(side='top', fill='both', expand=True)

        p1.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p2.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p3.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p4.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        p5.place(in_=container, x=0, y=0, relwidth=1, relheight=1)
        #p6.place(in_=container, x=0, y=0, relwidth=1, relheight=1)


        # Buttons to show the different pages
        b1 = tk.Button(buttonframe, text='Filter', command=p1.show)
        b2 = tk.Button(buttonframe, text='Tracking', command=p2.show)
        b3 = tk.Button(buttonframe, text='Run Algorithms', command=p3.show)
        b4 = tk.Button(buttonframe, text='Convert to MP4', command=p4.show)
        b5 = tk.Button(buttonframe, text='Split Data', command=p5.show)
        #b6 = tk.Button(buttonframe, text='Help', command=p6.show)

        # Placing buttons on the top left of the window
        b1.pack(side='left')
        b2.pack(side='left')
        b3.pack(side='left')
        b4.pack(side='left')
        b5.pack(side='left')
        #b6.pack(side='right')


        # Start the GUI on Page1
        p1.show()

# Main loop for tkinter to function
if __name__ == '__main__':
    root = tk.Tk()
    main = MainView(root)
    main.pack(side='top', fill='both', expand=True)
    root.geometry('600x350')
    root.grid()
    root.mainloop()
