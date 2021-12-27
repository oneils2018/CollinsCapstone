import numpy as np
import pandas as pd
import matplotlib.pyplot as mplib
import os
min = 0  #index ranges
max = 50000

cam_data = pd.read_csv('dvSave-2021_08_24_10_44_21.csv', delimiter=',', names=['timestamp' , 'x', 'y', 'polarity'])
#drops first two rows (no data is stored in them)
cam_data.drop(labels=[0,1], axis=0, inplace=True)
time = cam_data['timestamp']
pol = cam_data['polarity']
xvar = cam_data['x']
yvar = cam_data['y']
xvar = pd.to_numeric(xvar[min:max:1])     #converts from string type to integer
yvar= pd.to_numeric(yvar[min:max:1])
pol = pd.to_numeric(pol[min:max:1])

index = min + 2  #search index

for i in pol[0:max]:        #loops through len(pol) times, filters out all 0 pixels (only activations are graphed
   if pol[index] == 0:
      xvar.pop(index)       #drops all 0 values from x and y series
      yvar.pop(index)
   index += 1



max = max - min
min = 0
fig, ax = mplib.subplots()
ax.scatter(xvar[min:max:1], yvar[min:max:1], s = 0.5)       #plots x and y through entire time interval, s = 0.5 sets the size of dot on scatter plot
mplib.show()




