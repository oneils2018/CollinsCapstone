import numpy as np
import matplotlib.pyplot as mplib
from dv import AedatFile
import os
min = 0  #index ranges
max = 40000
positive = 5 #minimum number of hits required to generate a positive pixel
"""

Description:

    Open the AedatFile. The events will be a stored as numpy arrays.
    We then access information of all events by type 

    The xavg and yavg  holds all x and y values for pixels of polarity=1 with more than 'postive' hits 

    len(avg) make sure that we don't consider pixels that have already been added as positives to reduce 
    processing time.

    if xvar[index1] == xvar[index3] and yvar[index1] == yvar[index3] will assign x and y coordinate of a pixel with polarity = 1 generates a hit

    if xvar[index1] == xvar[index3] and yvar[index1] == yvar[index3] will add pixel if we get more hits than the threshold 'positive

    It will check if hit is larger then or equal to the postive varaible and it will append the X hits and Y hits.

    print x and y coordinates of every positive pixel index1 += 1

    plots x and y through entire time interval, s = 0.5 sets the size of dot on scatter plot

"""


with AedatFile(r"C:\Users\jerem\Downloads\dvSave-2021_08_24_10_44_21.aedat4") as f:

    events = np.hstack([packet for packet in f['events'].numpy()])

    timestamps, x, y, polarities = events['timestamp'], events['x'], events['y'], events['polarity']

    xvar = []
    yvar = []

    index = min
    while index < max:
        if events[index]['polarity'] != 0:
            xvar.append(events[index]['x'])
            yvar.append(events[index]['y'])
        index += 1
    xavg = []
    yavg = []

    index1 = 0
    while index1 < len(xvar) - 1:
        flag = 1
        hit = 0

        if len(xavg) > 1:
            index2 = 0
            while index2 < len(xavg):
                if xvar[index1] == xavg[index2] and yvar[index1] == yavg[index2]:
                    flag = 0
                index2 += 1

        index3 = 0
        while index3 < len(xvar) and flag == 1:
            if xvar[index1] == xvar[index3] and yvar[index1] == yvar[index3]:
                hit += 1
            index3 += 1

        if hit >= positive:
            xavg.append(xvar[index1])
            yavg.append(yvar[index1])
            print("x: " + str(xavg[len(xavg) - 1]) + '  y: ' + str(yavg[len(xavg) - 1])
            index1 += 1

            max = max - min
            min = 0
            fig, ax = mplib.subplots()
            ax.scatter(xavg[min:max:1], yavg[min:max:1], s = 0.5)
            mplib.show()
