import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import math as math
# numba is a library that must be install by running "pip install numba" It takes a function and re-writes in machine code to run extremely fast. It works best if numpy arrays are used.
from numba import jit, njit, vectorize
from scipy import stats
from dv import AedatFile
import os

#MODIFIED MATTHEW'S CODE TO INCLUDE -1 POLARITY#

start_time = time.time()
# The time_range is how far back in time and in the future of the current index does the program check for hits
# This has the largest hit on performance (Exponentially).
time_range = 7
# Positive is the minumun number of neighbor hits that must be attained for the hit to be added to the plot.
positive = 2
# The max_distance is the maximum distance in a 3d space where z is time, that a hit must be under to be added to the plot.
max_distance = 10
# The increment is the duration of time stamps the program will process at a time then plot to a graph.
increment = 10000
## Note: Filter 1 takes the data from the Aedat file and filters it based on distances from a specific point and its distance from its
## neighbors, calculated using the X and Y values, as well as time in the form of a Z axis.
## Filter 2 takes the output from Filter 1 and filters it just using the distances from a hit point and its nearest neighbors, not taking
## into account the time variable.
## The thing that effects computation time the most is the time_range (Higher = more time) and the total number of points on the graph
## before passing it to filter 2.


### FILTER 1 ###
min = 5
max = 40000
test = 0

# Load data from Aedat file.
with AedatFile(r"C:\Users\jerem\Downloads\dvSave-2021_08_24_10_44_21.aedat4") as f:
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
            if (events[index]['polarity'] == 1) :
                temp1_x = events[index]['x']
                temp1_y = events[index]['y']
                temp1_time = index
                index2 = index - time_range
                # Reset number of found hits
                hits = 0
                # Indexes through timestamps with a range from index-time_rance to index+time_range
                while index2 <= index + time_range:
                    if (events[index2]['polarity'] == 1) :
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

    #Function below takes filtered data and outputs the object center and left, right, top, and bottom bounds
    #min_distance is the minimum distance that the algorithm reaches before it "gives up" trying to find more pixels and just sets the last pixel hit as the bound
    #min_hits is the minimum number of hits required to actually create a box
    #tolerance is the number of pixels to go past the original bounds to create a box that is bigger then the object
    def tracking(min_distance, min_hits, tolerance, x_hits, y_hits, x_hits0, y_hits0):
        #Combine pixels of 1 and -1 polarity
        x_hits = np.concatenate((x_hits, x_hits0))
        y_hits = np.concatenate((y_hits, y_hits0))

        #Arrays for keeping track of hits outside the box
        x_outside = x_hits
        y_outside = y_hits

        #Arrays for keeping track of hits inside the box
        x_inside = np.empty(0)
        y_inside = np.empty(0)

        #Coordinates for center of object
        x_average = 0
        y_average = 0

        #Calculate the average for x hits and y hits to find the center of object
        index = 0
        while index < len(x_hits):
            x_average += x_hits[index]
            y_average += y_hits[index]
            index += 1
        x_average /= len(x_hits)
        y_average /= len(y_hits)

        #CODE BELOW FINDS THE RIGHT BOUND
        index1 = int(x_average) #Start looking at pixels to the right of the center
        flag = True
        no_hit = 0 #Track number of pixels in a row without a hit
        hit_bool = False
        y_right = y_average #Look at pixels directly to the right of the center

        #Iterate through pixels left to right starting at the center and ending either at the right bound or the edge of the frame
        while flag and index1 < 346:
            hit = False #Reset hit flag
            #Iterate through all of x_hits to see if there's a hit
            index2 = 0
            while index2 < len(x_hits) and not hit:
                #If there's a hit, update the x coordinate for the right bound and exit the loop
                if x_hits[index2] == index1:
                    hit = True
                    x_right = index1
                #If not, keep looping
                else:
                    hit = False
                index2 += 1
            #If there's a hit, reset the no_hit counter since it only counts number of misses in a row
            if hit:
                no_hit = 0
                hit_bool = True
            #If there was no hit, increment the misses in a row counter
            else:
                no_hit += 1
            #If there hasn't been a hit for more then the given minimum distance, give up and exit the loop. x_right is left as the last x coordinate there was a hit
            if no_hit > min_distance:
                flag = False
            index1 += 1 #We are traveling to the right

        #If the object is cutoff by the edge of the frame, set the right bound to the edge of the frame
        if index1 == 345:
            x_right = 345

        #If there was no hit at all, set the bound to 10 pixels to the right of the center
        if hit_bool == False and x_average + 10 <= 345:
            x_right = x_average + 10


        #CODE BELOW FINDS THE LEFT BOUND
        #See comments for right bound
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

        #CODE BELOW FINDS THE TOP BOUND
        #See comments for right bound
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


        #CODE BELOW FINDS THE BOTTOM BOUND
        #See comments for right bound
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

        # Apply tolerance
        if x_right < 345:
            x_right = x_right + tolerance
        if x_left > 1:
            x_left = x_left - tolerance
        if y_top < 259:
            y_top = y_top + tolerance
        if y_bottom > 1:
            y_bottom = y_bottom - tolerance

        #If there are not enough points, return 0 for everything
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

        #Find all hits outside of the box
        index = 0
        while index < len(x_hits):
            if x_hits[index] <= x_right and x_hits[index] >= x_left and y_hits[index] <= y_top and y_hits[index] >= y_bottom:
                index1 = 0
                while index1 < len(x_outside):
                    if x_outside[index1] == x_hits[index] and y_outside[index1] == y_hits[index]:
                        x_outside = np.delete(x_outside, index1)
                        y_outside = np.delete(y_outside, index1)
                        x_inside = np.append(x_inside, x_hits[index])
                        y_inside = np.append(y_inside, y_hits[index])
                    index1 += 1
            index += 1

        #Return the coordinates for the center of the object and the right, left, top, and bottom bounds
        #Return the pixels that are inside and the pixels that are outside the box
        return x_average, y_average, x_right, y_right, x_left, y_left, x_top, y_top, x_bottom, y_bottom, x_outside, y_outside, x_inside, y_inside

    jitted_filter4 = jit(nopython=True)(tracking)

    def tracking2(sample_size, min_distance, min_hits, tolerance, x_hits, y_hits):
        #Arrays for keeping track of hits outside the box
        x_outside = x_hits
        y_outside = y_hits

        #Arrays for keeping track of hits inside the box
        x_inside = np.empty(0)
        y_inside = np.empty(0)

        #Coordinates for center of object
        x_average = 0
        y_average = 0

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

        sample_hits_x = np.empty(0)
        sample_hits_y = np.empty(0)

        index = 0
        while index < len(x_hits):
            if x_hits[index] <= sample_right and x_hits[index] >= sample_left and y_hits[index] <= sample_top and y_hits[index] >= sample_bottom:
                sample_hits_x = np.append(sample_hits_x, x_hits[index])
                sample_hits_y = np.append(sample_hits_y, y_hits[index])
            index += 1

        #Calculate the average for x hits and y hits to find the center of object
        index = 0
        while index < len(sample_hits_x):
            x_average += sample_hits_x[index]
            y_average += sample_hits_y[index]
            index += 1

        #If there are not enough points, return 0 for everything
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

            index1 = 0
            while index1 < len(sample_hits_x):
                index2 = 0
                while index2 < len(x_outside):
                    if x_outside[index2] == sample_hits_x[index1] and y_outside[index2] == sample_hits_y[index1]:
                        x_outside = np.delete(x_outside, index2)
                        y_outside = np.delete(y_outside, index2)
                    index2 += 1
                index1 += 1
            #print("not enough in the sample area")
            return x_average, y_average, x_right, y_right, x_left, y_left, x_top, y_top, x_bottom, y_bottom, x_outside, y_outside, x_inside, y_inside
        else:
            x_average /= len(sample_hits_x)
            y_average /= len(sample_hits_y)

        #CODE BELOW FINDS THE RIGHT BOUND
        index1 = int(x_average) #Start looking at pixels to the right of the center
        flag = True
        no_hit = 0 #Track number of pixels in a row without a hit
        hit_bool = False
        y_right = y_average #Look at pixels directly to the right of the center

        #Iterate through pixels left to right starting at the center and ending either at the right bound or the edge of the frame
        while flag and index1 < 346:
            hit = False #Reset hit flag
            #Iterate through all of x_hits to see if there's a hit
            index2 = 0
            while index2 < len(x_hits) and not hit:
                #If there's a hit, update the x coordinate for the right bound and exit the loop
                if x_hits[index2] == index1:
                    hit = True
                    x_right = index1
                #If not, keep looping
                else:
                    hit = False
                index2 += 1
            #If there's a hit, reset the no_hit counter since it only counts number of misses in a row
            if hit:
                no_hit = 0
                hit_bool = True
            #If there was no hit, increment the misses in a row counter
            else:
                no_hit += 1
            #If there hasn't been a hit for more then the given minimum distance, give up and exit the loop. x_right is left as the last x coordinate there was a hit
            if no_hit > min_distance:
                flag = False
            index1 += 1 #We are traveling to the right

        #If the object is cutoff by the edge of the frame, set the right bound to the edge of the frame
        if index1 == 345:
            x_right = 345

        #If there was no hit at all, set the bound to 10 pixels to the right of the center
        if hit_bool == False and x_average + 10 <= 345:
            x_right = x_average + 10


        #CODE BELOW FINDS THE LEFT BOUND
        #See comments for right bound
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

        #CODE BELOW FINDS THE TOP BOUND
        #See comments for right bound
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


        #CODE BELOW FINDS THE BOTTOM BOUND
        #See comments for right bound
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

        # Apply tolerance
        if x_right + tolerance < 345:
            x_right = x_right + tolerance
        if x_left - tolerance > 1:
            x_left = x_left - tolerance
        if y_top + tolerance < 250:
            y_top = y_top + tolerance
        if y_bottom - tolerance > 1:
            y_bottom = y_bottom - tolerance

        #Find all hits outside of the box
        index = 0
        while index < len(x_hits):
            if x_hits[index] <= x_right and x_hits[index] >= x_left and y_hits[index] <= y_top and y_hits[index] >= y_bottom:
                index1 = 0
                while index1 < len(x_outside):
                    if x_outside[index1] == x_hits[index] and y_outside[index1] == y_hits[index]:
                        x_outside = np.delete(x_outside, index1)
                        y_outside = np.delete(y_outside, index1)
                        x_inside = np.append(x_inside, x_hits[index])
                        y_inside = np.append(y_inside, y_hits[index])
                    index1 += 1
            index += 1

        #Return the coordinates for the center of the object and the right, left, top, and bottom bounds
        #Return the pixels that are inside and the pixels that are outside the box
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
    while index3 < 750:
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
        #bisque_patch = mpatches.Patch(color='pink', label='First (+1) Filter output')
        #red_patch = mpatches.Patch(color='red', label='Second (+1) Filter output')
        #skyblue_patch = mpatches.Patch(color='skyblue', label='First (-1) Filter output')
        #blue_patch = mpatches.Patch(color='blue', label='Second (-1) Filter output')
        title = "Time Increment: " + str(min) + " to " + str(max)
        plt.title(title)
        #plt.legend(handles=[red_patch, bisque_patch, blue_patch, skyblue_patch], loc=1)
        plt.xlim(0, 350)
        plt.ylim(0, 250)
        plt.scatter(x_hits, y_hits, s=0.5, c='pink')
        plt.scatter(x_hits0, y_hits0, s=0.5, c='skyblue')

        temp_x_hits = x_combined
        temp_y_hits = y_combined

        x_inside1_p = np.empty(0)
        y_inside1_p = np.empty(0)

        x_inside1_n = np.empty(0)
        y_inside1_n = np.empty(0)

        index = 0
        while len(temp_x_hits) > 0 and index < 50:
            x_object, y_object, x_right, y_right, x_left, y_left, x_top, y_top, x_bottom, y_bottom, x_outside, y_outside, x_inside, y_inside = jitted_filter5(40, 10, 50, 5, temp_x_hits, temp_y_hits)
            temp_x_hits = x_outside
            temp_y_hits = y_outside

            no_object = False
            if x_object == 0 and y_object == 0:
                no_object = True

            if not no_object:
                plt.scatter(x_object, y_object, s=10, c='g')
                plt.scatter(x_right, y_right, s=10, c='g')
                plt.scatter(x_left, y_left, s=10, c='g')
                plt.scatter(x_top, y_top, s=10, c='g')
                plt.scatter(x_bottom, y_bottom, s=10, c='g')
                rectangle = plt.Rectangle((x_left, y_bottom), x_right - x_left, y_top - y_bottom, fc='none', ec="green") #Draw rectangle around the object
                plt.gca().add_patch(rectangle)

                index1 = 0
                while index1 < len(x_hits):
                    if x_hits[index1] <= x_right and x_hits[index1] >= x_left and y_hits[index1] <= y_top and y_hits[index1] >= y_bottom:
                        x_inside1_p = np.append(x_inside1_p, x_hits[index1])
                        y_inside1_p = np.append(y_inside1_p, y_hits[index1])
                    index1 += 1

                index1 = 0
                while index1 < len(x_hits0):
                    if x_hits0[index1] <= x_right and x_hits0[index1] >= x_left and y_hits0[index1] <= y_top and y_hits0[index1] >= y_bottom:
                        x_inside1_n = np.append(x_inside1_n, x_hits0[index1])
                        y_inside1_n = np.append(y_inside1_n, y_hits0[index1])
                    index1 += 1
            index += 1

        plt.scatter(x_inside1_p, y_inside1_p, s=0.5, c='r')
        plt.scatter(x_inside1_n, y_inside1_n, s=0.5, c='b')
        plt.savefig(str(index3))
        plt.clf()

        # Increment time.
        min = min + increment
        max = max + increment
        index3 += 1