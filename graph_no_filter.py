import numpy as np
import matplotlib.pyplot as mplib
from dv import AedatFile
import os
min = 0  #index ranges
max = 25000

with AedatFile(r"C:\Users\jerem\Downloads\dvSave-2021_08_24_10_44_21.aedat4") as f:
    #events will be a named numpy array
    events = np.hstack([packet for packet in f['events'].numpy()])

    #access information of all events by type
    timestamps, x, y, polarities = events['timestamp'], events['x'], events['y'], events['polarity']

    #holds all x and y values for pixels of polarity = 1
    xvar = []
    yvar = []

    index = min
    while index < max:
        if events[index]['polarity'] != 0:
            xvar.append(events[index]['x'])
            yvar.append(events[index]['y'])
        index += 1

max = max - min
min = 0
fig, ax = mplib.subplots()
ax.scatter(xvar[min:max:1], yvar[min:max:1], s = 0.5)       #plots x and y through entire time interval, s = 0.5 sets the size of dot on scatter plot
mplib.show()