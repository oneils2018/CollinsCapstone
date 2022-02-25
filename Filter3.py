import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import math as math
from numba import jit, njit, vectorize
from dv import AedatFile
import os
start_time = time.time()
"""
    the time_range is how far back in the past and the future if the current index does the program checks if hits occur.
    This becomes the largest hit on performance
    
    positive =2 -> checks the minimum number of hits that must be attained for the hot to be added to the graph 
    
    the max_distance is the maximum amount of distance that is in three dimension  space where Z is time, that a hit 
    must be under to be added to the plot.
    
    The increment will be the amount of time that the program will process at a time then plot it to a graph 
"""
time_range = 7
positive = 2
max_distance = 10
increment = 40000

min = 0
max = 40000
test = 0

"""
the part under will load the data from the Aedat file.
"""
with AedatFile(r"C:\Users\Lenovo\Documents\Collins\CollinsCapstone\DV_FILES\dvSave-2021_08_24_10_44_21.aedat4") as f:
    events = np.hstack([packet for packet in f['events'].numpy()])
    timestamps, x, y, polarities = events['timestamp'], events['x'], events['y'], events['polarity']
""":
Filter 1:
    The purpose of this filter is to absorb the data from the Aedat file and will filter it depending on the distance from one point and the 
    distance from a neighbor. It calculates the X and Y values and the time that is corresponding to the Z axis.
    
    This function will first  empty the x and y hits, it will go through a loop and will check if a hit is found. 
    If a hit is found note down the X and Y spots. It will also store the timestamp as temp1_time to be the Z variable.
    
    It will then reset the number of found hits. Then it will loop through timestamps with a range from index-time_range to the index+time_range to
    
    It uses the distance formula where D=squareRoot of (x2-x1)squared +(y2-y1) squared. It used between hits found in time range, accounting for distance through time 
    
    Once the distance formula is calculate, it check if it's less than or equal to max_distance,+1 to the variable that supposed to represent a hit. 
    else if the number of hits is greater then or equal to the set positive value, we will add it to plot. 
    
    It will add the x hits to x_hit and the y hits to y_hits 
    
    The def function will return the x hits and the y hits and then jits the function 
    
"""

def Filter1(events,min,max):
    index = min
    x_hits=np.empty(0)
    y_hits=np.empty(0)
    while index < max:
        if events[index]['polarity'] != 0:
            temp1_x = events[index]['x']
            temp1_y = events[index]['y']
            temp1_time = index
            index2 = index - time_range
            hits = 0
            while index2 <= index + time_range:
                if events[index2]['polarity'] != 0:
                    temp2_x = events[index2]['x']
                    temp2_y = events[index2]['y']
                    temp2_time = index2
                    distance = math.sqrt((temp2_x - temp1_x)**2+(temp2_y-temp1_y)**2+(temp1_time-temp2_time)**2)
                    if distance <= max_distance:
                        hits += 1
                index2 += 1
            if hits >= positive:
                x_hits = np.append(x_hits,events[index]['x'])
                y_hits = np.append(y_hits,events[index]['y'])
        index += 1
    return x_hits,y_hits

jitted_filter1 = jit(nopython=True)(Filter1)


""" 
Filter 2 
    
   Filter 2 will take the output from Filter 1 and filters it by using the distances from a hit point and its nearest neighbors.
    
   time_range effect computation time and the total number of points on the graph before passing it to filter 2.

   Takes the plot data and will filter it by taking away points that do not have enough neighbors. 
   
   It uses the distance formula and will check if less than 5 or if the hits is less than 8 and it will delete the x hits and y hits that follow that criteria.
   
   It jits filter 2 .3
   
   The while loop (while index<20) will loop throughout  video data in incremental fashion.
   
   It will call the first filter with the X and Y hits and plot that data in silver 
   
   It will print the time too and increment the time.
   
   The last part of the program is ploting the data of both filter 1 and filter 2 and it prints the execution time 
   
   The red patch will represent filter 2 and the silver patch will be the filter 1 output 
"""
def plot_filter(x_hits,y_hits):
    index = 0
    while index < len(x_hits):
        temp1_x=x_hits[index]
        temp1_y=y_hits[index]
        index2=0
        hits=0
        while index2 < len(x_hits):
            temp2_x=x_hits[index2]
            temp2_y=y_hits[index2]
            distance = math.sqrt((temp2_x-temp1_x)**2+(temp2_y-temp1_y)**2)
            if distance < 5:
                hits += 1
            index2 += 1
        if hits < 8:
            x_hits = np.delete(x_hits, index)
            y_hits = np.delete(y_hits, index)
        index += 1
    return x_hits,y_hits

jitted_filter2 = jit(nopython=True)(plot_filter)

index3 = 0
while index3 < 20:
    x_hits,y_hits = jitted_filter1(events,min,max)
    plt.scatter(x_hits,y_hits,s=0.5,c='silver')
    x_hits = np.array(x_hits)
    y_hits = np.array(y_hits)
    print("Total points on plot after first filter: ", len(x_hits))
    index = 0
    while index < 7:
        x_hits,y_hits = jitted_filter2(x_hits,y_hits)
        index += 1
    total_time = round((time.time()-start_time),2)
    print("Total points on plot after second filter: ", len(x_hits))
    print("Execution time: %s seconds" % (total_time))
    print("On Image #",index3)

    red_patch = mpatches.Patch(color='red', label='Filter 2 output')
    gray_patch = mpatches.Patch(color='silver', label='Filter 1 output')
    title = "Time Increment: " + str(min) + " to " + str(max)
    plt.title(title)
    plt.legend(handles=[red_patch,gray_patch],loc=1)
    plt.xlim(0, 350)
    plt.ylim(0, 250)
    plt.scatter(x_hits,y_hits,s=0.5,c='r')
    plt.savefig(str(index3))
    plt.clf()
    min = min+increment
    max = max+increment
    index3 += 1

