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
from main import *

# Allows the script to interact with the os
import os

# Allows for subprocesses
import subprocess

# This file is to start the GUI interface that connects the rest of the scripts in the same folder.

# Tkinter skeleton built off from:
# https://stackoverflow.com/questions/14817210/using-buttons-in-tkinter-to-navigate-to-different-pages-of-the-application

# Restarts the program
def restartProgram():
    root.destroy()
    os.startfile('GUI.py')
    os.startfile('GUI.exe')

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

        option = tk.IntVar()  # Create Test Data

        # Title of the 1st section
        label03 = tk.Label(self, fg='#FF0000', text='Filter, track, and classify algorithm:\n '
                                          '(Need to select .aedat4 file before starting algorithm!)\n '
                                          ''
                 )

        # Labels for the search buttons
        fileCurrent1 = tk.Label(self, text='Select a File: ', anchor="w")
        directoryCurrent1 = tk.Label(self, text='Results Directory: ' + vars[13], anchor="w")
        modelCurrent1 = tk.Label(self, text='Select a Model: ' + vars[17], anchor="w")

        # Buttons to search files to be used and directory where the results are placed
        searchButton1 = tk.Button(self, text='Search File', command=lambda: browseFiles1())
        searchButton2 = tk.Button(self, text='Search Results Directory', command=lambda: browseDirectory1())
        searchButton3 = tk.Button(self, text='Search Classification Model', command=lambda: browseFiles2())

        checkBox = tk.Checkbutton(self, text='Turn on test data creation', variable=option, onvalue=1, offvalue=0)

        # Buttons to start and stop the algorithm.
        # They turn on when the user selects a file.
        # The stop restarts the program to stop the thread
        startButton1 = tk.Button(self, text='Start', command=lambda: [t1.start(), pb1.start()], state='disabled')
        stopButton1 = tk.Button(self, text='Stop', command=restartProgram, state='disabled')

        # A visual progressbar widget for the Filter and tracking algorithm
        pb1 = tk.ttk.Progressbar(self, orient='horizontal', mode='indeterminate', length=100)

        # Title of the 2nd section
        labelProt = tk.Label(self, fg='#FF0000', text='--------------------------------------------------------------------------------------------------------------\n'
                                                    'Object Trajectory Prototype:\n '
                                                    '(This is the pose tracking prototype program that was only tested with the exact variables and file used)\n '
                                                    '(The script is titled "Object_Trajectory_Algorithm")\n'
                                                    '(Output is found in the Prototype folder in the Results directory)'
                           )

        # Buttons to start and stop the algorithem.
        # The stop restarts the program to stop the thread
        startButtonProt = tk.Button(self, text='Start', command=lambda: [tProt.start(), pbProt.start()])
        stopButtonProt = tk.Button(self, text='Stop', command=restartProgram)

        # A visual progressbar widget for the object trajectory prototype
        pbProt = tk.ttk.Progressbar(self, orient='horizontal', mode='indeterminate', length=100)

        # Grid location of entry fields, labels, and buttons
        label03.grid(column=0, row=0, columnspan=4, padx=10, pady=10)
        labelProt.grid(column=0, row=8, columnspan=4, padx=10, pady=10)

        fileCurrent1.grid(column=1, row=1, columnspan=100, padx=10, pady=10)
        directoryCurrent1.grid(column=1, row=3, columnspan=100, padx=10, pady=10)
        modelCurrent1.grid(column=1, row=5, columnspan=100, padx=10, pady=10)

        searchButton1.grid(column=0, row=1, columnspan=1, padx=10, pady=10, sticky='ew')
        searchButton2.grid(column=0, row=3, columnspan=1, padx=10, pady=10, sticky='ew')
        searchButton3.grid(column=0, row=5, columnspan=1, padx=10, pady=10, sticky='ew')

        checkBox.grid(column=0, row=6, columnspan=1, padx=10, pady=10)

        startButton1.grid(column=0, row=7, columnspan=1, padx=10, pady=10)
        stopButton1.grid(column=1, row=7, columnspan=1, padx=10, pady=10)
        startButtonProt.grid(column=0, row=9, columnspan=1, padx=10, pady=10)
        stopButtonProt.grid(column=1, row=9, columnspan=1, padx=10, pady=10)

        pb1.grid(column=2, row=7, columnspan=2, padx=10, pady=10)
        pbProt.grid(column=2, row=9, columnspan=2, padx=10, pady=10)

        # Defining the thread for the filter and tracking algorithm
        def thread1():
            # Creates file directory if it does not exist
            if not os.path.isdir(vars[13]):
                os.makedirs(vars[13])

            # Load test data creation option to vars[18]
            vars[18] = option.get()

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
                            vars[13],
                            vars[17],
                            vars[18],
                            )

            # Stops progress bar animation
            pb1.stop()

        # Defining the thread for the Object Trajectory Prototype
        def threadProt():
            # Creates file directory if it does not exist
            if not os.path.isdir(vars[13] + '\\Prototype\\'):
                os.makedirs(vars[13] + '\\Prototype\\')

            Object_Trajectory_Algorithm()

            # Stops progress bar animation
            pbProt.stop()

        # Declares the threads
        t1 = threading.Thread(target=thread1)
        tProt = threading.Thread(target=threadProt)

        # Makes the threads into daemons so it would stop when the application (GUI) is closed
        t1.daemon = True
        tProt.daemon = True

        # Funtion to browes Aedat4 files to use.
        def browseFiles1():
            # Search for a file popup
            vars[12] = tk.filedialog.askopenfilename(initialdir='/',
                                                     title='Select an Aedat4 File',
                                                     filetypes=(('aedat4 files', '*.aedat4*'), ('all files', '*.*')))

            # If a file is chosen, enable the buttons
            if vars[12] != '':
                fileCurrent1.config(text='File Selected: ' + vars[12], anchor="w")
                startButton1.config(state='normal')
                stopButton1.config(state='normal')

                # If redults directory does not exist, make one
                if not os.path.isdir(vars[13]):
                    os.makedirs(vars[13])

        # Funtion to browes files to use.
        def browseFiles2():
            # Search for a file popup
            vars[17] = tk.filedialog.askopenfilename(initialdir='/',
                                                     title='Select a Model',
                                                     filetypes=(
                                                     ('h5 files', '*.h5*'), ('all files', '*.*')))
            modelCurrent1.config(text='Model Selected: ' + vars[17], anchor="w")

        # Funstion to browse for a results directory
        def browseDirectory1():
            vars[13] = tk.filedialog.askdirectory() + '/'
            directoryCurrent1.config(text='Directory Selected: ' + vars[13], anchor="w")

# Run PNGs to MP4 screen
class Page4(Page):
    def __init__(self, *args, **kwargs):
        Page.__init__(self, *args, **kwargs)

        ### GUI widgets placement, text, and commands. Similar to the ones in Page3 but modified for the PNGs to MP4 script. ###

        option = tk.IntVar()  # Delete PNGs

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

        checkBox3 = tk.Checkbutton(self, text='Delete PNGs after making the video PERMANENTLY. (CAREFUL!)', variable=option, onvalue=1, offvalue=0, fg='red')

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

            generateVideo(vars[13],
                          vars[14],
                          option.get(),
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

            test_train_split(vars[13],
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

        path1 = os.path.dirname(__file__) + '\\DAVIS346.pdf'
        path2 = os.path.dirname(__file__) + '\\Documentation.pdf'

        helpButton1 = tk.Button(self, text='DAVIS346 Specs', command=lambda: subprocess.Popen([path1], shell=True))
        helpButton2 = tk.Button(self, text='Documentation', command=lambda: subprocess.Popen([path2], shell=True))

        helpButton1.grid(column=0, row=1, columnspan=1, padx=10, pady=10, sticky='ew')
        helpButton2.grid(column=0, row=2, columnspan=1, padx=10, pady=10, sticky='ew')

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
        p6.place(in_=container, x=0, y=0, relwidth=1, relheight=1)


        # Buttons to show the different pages
        b1 = tk.Button(buttonframe, text='Filter', command=p1.show)
        b2 = tk.Button(buttonframe, text='Tracking', command=p2.show)
        b3 = tk.Button(buttonframe, text='Run Algorithms', command=p3.show)
        b4 = tk.Button(buttonframe, text='Convert to MP4', command=p4.show)
        b5 = tk.Button(buttonframe, text='Split Data', command=p5.show)
        b6 = tk.Button(buttonframe, text='Help', command=p6.show)

        # Placing buttons on the top left of the window
        b1.pack(side='left')
        b2.pack(side='left')
        b3.pack(side='left')
        b4.pack(side='left')
        b5.pack(side='left')
        b6.pack(side='right')


        # Start the GUI on Page1
        p1.show()

# Main loop for tkinter to function
if __name__ == '__main__':
    root = tk.Tk()
    main = MainView(root)
    main.pack(side='top', fill='both', expand=True)
    root.geometry('800x500')
    root.grid()
    root.mainloop()
