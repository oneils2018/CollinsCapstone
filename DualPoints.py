import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import math as math
from numba import jit, njit, vectorize
from dv import AedatFile
import os
"""

 the time.time() returns the number of seconds passed since epoch.  IT returns the time as floating time.   
 
 The time_range is how far back in the past and the future if the current index does the program checks if hits occur.
 his becomes the largest hit on performance
 
 positive =2 -> checks the minimum number of hits that must be attained for the hot to be added to the graph 
 
 The max_distance is the maximum amount of distance that is in three dimension  space where Z is time, that a hit 
 must be under to be added to the plot.
    
 The increment will be the amount of time that the program will process at a time then plot it to a graph 

"""
start_time = time.time()
time_range = 7
positive = 2
max_distance = 10
increment = 10000



min = 5
max = 40000
test = 0

"""
    This  will Load the data from AEDAT file 
"""
with AedatFile(r"C:\Users\111gu\Desktop\Data\DV_FILES\dvSave-2021_08_24_10_44_21.aedat4") as f:
    events = np.hstack([packet for packet in f['events'].numpy()])
    timestamps, x, y, polarities = events['timestamp'], events['x'], events['y'], events['polarity']


"""
  Filter1:

    The purpose of this filter is to absorb the data from the Aedat file and will filter it depending on the distance from one point and the 
    distance from a neighbor. It calculates the X and Y values and the time that is corresponding to the Z axis.

    This function will first  empty the x and y hits, it will go through a loop and will check if a hit is found. 
    If a hit is found note down the X and Y spots. It will also store the timestamp as temp1_time to be the Z variable.

    Computation time is effect by the time_range. When there is higher time_range, it results in more time and the total number of points on the graph
    before its passed down to the second filter
    
    It will then reset the number of found hits. Then it will loop through timestamps with a range from index-time_range to the index+time_range    
    
    In that while loop, it will utilize distance formula where D=squareRoot of (x2-x1)squared +(y2-y1) squared.
    It used between hits found in time range, accounting for distance through time 

    
    Once the distance formula is calculate, it check if it's less than or equal to max_distance,+1 to the variable that supposed to represent a hit. 
    else if the number of hits is greater then or equal to the set positive value, we will add it to plot. 
        
    It will add the x hits to x_hit and the y hits to y_hits 
    
    The def function will return the x hits and the y hits and then jits the function
"""
def Filter1(events, min, max):
    index = min
    x_hits = np.empty(0)
    y_hits = np.empty(0)
    while index < max:
        if (events[index]['polarity'] == 1) :
            temp1_x = events[index]['x']
            temp1_y = events[index]['y']
            temp1_time = index
            index2 = index - time_range
            hits = 0
            while index2 <= index + time_range:
                if (events[index2]['polarity'] == 1) :
                    temp2_x = events[index2]['x']
                    temp2_y = events[index2]['y']
                    temp2_time = index2
                    distance = math.sqrt(
                        (temp2_x - temp1_x) ** 2 + (temp2_y - temp1_y) ** 2 + (temp1_time - temp2_time) ** 2)
                    if distance <= max_distance:
                        hits += 1
                index2 += 1
            if hits >= positive:
                x_hits = np.append(x_hits, events[index]['x'])
                y_hits = np.append(y_hits, events[index]['y'])
        index += 1
    return x_hits, y_hits

jitted_filter1 = jit(nopython=True)(Filter1)

"""
    Filter 2
 
   Filter 2 will take the output from Filter 1 and filters it by using the distances from a hit point and its nearest neighbors.
    
   time_range effect computation time and the total number of points on the graph before passing it to filter 2.

   Takes the plot data and will filter it by taking away points that do not have enough neighbors. 
   
   It uses the distance formula and will check if less than 5 or if the hits is less than 8 and it will delete the x hits and y hits that follow that criteria.
   
   It will then return the X hits and Y hits 
   
   It jits filter 2  
"""
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


jitted_filter2 = jit(nopython=True)(plot_filter)

"""
    The function10 for -1 polarity 
    
    IT will first empty the X hits and the Y hits
        
    If there is a hit, note down x and y and its current timestamp is put down as temp1_time to act 
    as a zi variable.x
    
    It will then reset the number of found hits. Indexes threw timestamps with a variety from index- time_rance to index+time range
    
    Utilize the  distance formula to calculate the distance between hits that is located in time range.
    It accounts for distance through time.
    
    If the distance that was calculated is less than or equal to the max_distance, add one to the hit 
    variable.
    
    If the number of hits is larger then or equal to the set positive value, add it to the graph
    
    It will return the X and Y hits
    
    We then use the jit function on filter 10.
    
"""
def Filter10(events, min, max):
    index = min
    x_hits = np.empty(0)
    y_hits = np.empty(0)
    while index < max:
        if events[index]['polarity'] == 0:
            temp1_x = events[index]['x']
            temp1_y = events[index]['y']
            temp1_time = index
            index2 = index - time_range
            hits = 0
            while index2 <= index + time_range:
                if events[index2]['polarity'] == 0:
                    temp2_x = events[index2]['x']
                    temp2_y = events[index2]['y']
                    temp2_time = index2
                    distance = math.sqrt(
                        (temp2_x - temp1_x) ** 2 + (temp2_y - temp1_y) ** 2 + (temp1_time - temp2_time) ** 2)
                    if distance <= max_distance:
                        hits += 1
                index2 += 1
            if hits >= positive:
                x_hits = np.append(x_hits, events[index]['x'])
                y_hits = np.append(y_hits, events[index]['y'])
        index += 1
    return x_hits, y_hits


jitted_filter10 = jit(nopython=True)(Filter10)

"""
    The while loop is used to through the data of the video in increments

    It will call the first filter and return the data for X and Y hits.
    The X and the Y hits of the first filter will be in Pink

    It will Call the Filter10 to return the data for X and Y hits
    The X and Y hits of Filter10 will be in Skyblue.
    
    Displays the total points on the plot after the (+1)filter and (-1)filter

    prints the time to console then we plot the data .

    The last step is increment time 

"""

index3 = 0
while index3 < 750:
    x_hits, y_hits = jitted_filter1(events, min, max)
    x_hits0, y_hits0 = jitted_filter10(events, min, max)
    plt.scatter(x_hits, y_hits, s=0.5, c='pink')
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

    total_time = round((time.time() - start_time), 2)
    print("Total points on plot after second (+1) filter: ", len(x_hits))
    print("Total points on plot after second (-1) filter: ", len(x_hits0))
    print("Execution time: %s seconds" % (total_time))
    print("On Image #", index3)

    bisque_patch = mpatches.Patch(color='pink', label='First (+1) Filter output')
    red_patch = mpatches.Patch(color='red', label='Second (+1) Filter output')
    skyblue_patch = mpatches.Patch(color='skyblue', label='First (-1) Filter output')
    blue_patch = mpatches.Patch(color='blue', label='Second (-1) Filter output')
    title = "Time Increment: " + str(min) + " to " + str(max)
    plt.title(title)
    plt.legend(handles=[red_patch, bisque_patch, blue_patch, skyblue_patch], loc=1)
    plt.xlim(0, 350)
    plt.ylim(0, 250)
    plt.scatter(x_hits, y_hits, s=0.5, c='r')
    plt.scatter(x_hits0, y_hits0, s=0.5, c='b')
    plt.savefig(str(index3))
    plt.clf()

    min = min + increment
    max = max + increment
    index3 += 1
