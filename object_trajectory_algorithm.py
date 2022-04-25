import time
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.patches as mpatches
import math as math
# numba is a library that must be install by running "pip install numba" It takes a function and re-writes in machine code to run extremely fast. It works best if numpy arrays are used.
from numba import jit, njit, vectorize
from scipy import stats
from dv import AedatFile
import os

#MODIFIED MATTHEW'S AND JEREMY'S CODE TO INCLUDE SEPERATE VARIABLES FILE

def Object_Trajectory_Algorithm():

    start_time_Prot = time.time()

    ##### FILTER Variables #####

    # The time_range is how far back in time and in the future of the current index does the program check for hits
    # This has the largest hit on performance (Exponentially).
    time_range_Prot = 7

    # Positive is the minimum number of neighbor hits that must be attained for the hit to be added to the plot.
    positive_Prot = 2

    # The max_distance is the maximum distance in a 3d space
    # Where z is time that a hit must be under to be added to the plot.
    max_distance_Prot = 10

    # The increment is the duration of time stamps the program will process at a time then plot to a graph.
    increment_Prot = 30000

    # The event number after the increment from which the filter starts
    min_Prot = 4230000  # starts at 1 min 16 sec on DV video

    # The number of events filtered into a single frame
    max_Prot = 4270000

    ##### TRACKING Variables #####

    # Determines how large a sample size we should take for averaging pixels to find the center of an object
    sample_size_Prot = 40

    # Threshold for number of misses in a row before we "give up" and use the last hit as a bound
    min_distance_Prot = 10

    # Minimum number of hits within a sample required to identify it as an object and draw a box
    min_hits_Prot = 50

    # How much bigger should the box be then the object
    tolerance_Prot = 5

    # How many times should we iterate the tracking function before we give up
    max_tracking_iterations_Prot = 50

    ## Note: Filter 1 takes the data from the Aedat file and filters it based on distances from a specific point and its distance from its
    ## neighbors, calculated using the X and Y values, as well as time in the form of a Z axis.
    ## Filter 2 takes the output from Filter 1 and filters it just using the distances from a hit point and its nearest neighbors, not taking
    ## into account the time variable.
    ## The thing that effects computation time the most is the time_range (Higher = more time) and the total number of points on the graph
    ## before passing it to filter 2.

    # Load data from Aedat file.
    with AedatFile(os.path.dirname(__file__) + '\\Night_Vapor.aedat4') as f:
        events = np.hstack([packet for packet in f['events'].numpy()])
        timestamps, x, y, polarities = events['timestamp'], events['x'], events['y'], events['polarity']


        ############
        # Filter 1 #
        ############

        def Filter1_Prot(events, min_Prot, max_Prot):
            index = min_Prot
            x_hits = np.empty(0)
            y_hits = np.empty(0)
            while index < max_Prot:
                # If a hit is found, write down its x and y, and its current timestamp stored as temp1_time to act as a z variable.
                if (events[index]['polarity'] == 1) :
                    temp1_x = events[index]['x']
                    temp1_y = events[index]['y']
                    temp1_time = index
                    index2 = index - time_range_Prot
                    # Reset number of found hits
                    hits = 0
                    # Indexes through timestamps with a range from index-time_rance to index+time_range
                    while index2 <= index + time_range_Prot:
                        if (events[index2]['polarity'] == 1) :
                            temp2_x = events[index2]['x']
                            temp2_y = events[index2]['y']
                            temp2_time = index2
                            # Uses a distance formula to calculate the distance between hits found in time range, accounting for distance through time.
                            distance = math.sqrt(
                                (temp2_x - temp1_x) ** 2 + (temp2_y - temp1_y) ** 2 + (temp1_time - temp2_time) ** 2)
                            # If distance calculated is less then or equal to max_distance, add one to hit variable.
                            if distance <= max_distance_Prot:
                                hits += 1
                        index2 += 1
                    # If number of hits is greater then or equal to the set positive value, add it to the plot.
                    if hits >= positive_Prot:
                        x_hits = np.append(x_hits, events[index]['x'])
                        y_hits = np.append(y_hits, 250 - events[index]['y'])
                index += 1
            return x_hits, y_hits


        # The jit function converts Filter1 into a jitted function, basically re-writting the code in a much faster to run machine code.
        jitted_filter1_Prot = jit(nopython=True)(Filter1_Prot)


        ################
        ### FILTER 2 ###
        ################

        # Below this point is a function that takes the plot data and further filters it, removing points that do not have enough neighbors.
        def plot_filter_Prot(x_hits, y_hits):
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
        jitted_filter2_Prot = jit(nopython=True)(plot_filter_Prot)

        ################
        ### TRACKING ###
        ################

        # Function below takes filtered data and outputs the object center and left, right, top, and bottom bounds
        # min_distance is the minimum distance that the algorithm reaches before it "gives up" trying to find more pixels and just sets the last pixel hit as the bound
        # min_hits is the minimum number of hits required to actually create a box
        # tolerance is the number of pixels to go past the original bounds to create a box that is bigger then the object

        def tracking_Prot(sample_size_Prot, min_distance_Prot, min_hits_Prot, tolerance_Prot, x_hits, y_hits):
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
            if x_hits[0] + sample_size_Prot <= 345:
                sample_right = x_hits[0] + sample_size_Prot
            else:
                sample_right = 345
            if x_hits[0] - sample_size_Prot >= 1:
                sample_left = x_hits[0] - sample_size_Prot
            else:
                sample_left = 1
            if y_hits[0] + sample_size_Prot <= 249:
                sample_top = y_hits[0] + sample_size_Prot
            else:
                sample_top = 249
            if y_hits[0] - sample_size_Prot >= 1:
                sample_bottom = y_hits[0] - sample_size_Prot
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
            if index < min_hits_Prot:
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
                if no_hit > min_distance_Prot:
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
                if no_hit > min_distance_Prot:
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
                if no_hit > min_distance_Prot:
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
                if no_hit > min_distance_Prot:
                    flag = False
                index1 -= 1

            if index1 == 1:
                y_bottom = 1

            if hit_bool == False and y_average - 10 >= 1:
                y_bottom = y_average - 10

            # Apply tolerance (user defined)
            if x_right + tolerance_Prot < 345:
                x_right = x_right + tolerance_Prot
            if x_left - tolerance_Prot > 1:
                x_left = x_left - tolerance_Prot
            if y_top + tolerance_Prot < 250:
                y_top = y_top + tolerance_Prot
            if y_bottom - tolerance_Prot > 1:
                y_bottom = y_bottom - tolerance_Prot

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

        jitted_filter5_Prot = jit(nopython=True)(tracking_Prot)

        ############################
        # Filter10 For -1 Polarity #
        ############################

        def Filter10_Prot(events, min_Prot, max_Prot):
            index = min_Prot
            x_hits = np.empty(0)
            y_hits = np.empty(0)
            while index < max_Prot:
                # If a hit is found, write down its x and y, and its current timestamp stored as temp1_time to act as a z variable.
                if events[index]['polarity'] == 0:
                    temp1_x = events[index]['x']
                    temp1_y = events[index]['y']
                    temp1_time = index
                    index2 = index - time_range_Prot
                    # Reset number of found hits
                    hits = 0
                    # Indexes through timestamps with a range from index-time_rance to index+time_range
                    while index2 <= index + time_range_Prot:
                        if events[index2]['polarity'] == 0:
                            temp2_x = events[index2]['x']
                            temp2_y = events[index2]['y']
                            temp2_time = index2
                            # Uses a distance formula to calculate the distance between hits found in time range, accounting for distance through time.
                            distance = math.sqrt(
                                (temp2_x - temp1_x) ** 2 + (temp2_y - temp1_y) ** 2 + (temp1_time - temp2_time) ** 2)
                            # If distance calculated is less then or equal to max_distance, add one to hit variable.
                            if distance <= max_distance_Prot:
                                hits += 1
                        index2 += 1
                    # If number of hits is greater then or equal to the set positive value, add it to the plot.
                    if hits >= positive_Prot:
                        x_hits = np.append(x_hits, events[index]['x'])
                        y_hits = np.append(y_hits, 250 - events[index]['y'])
                index += 1
            return x_hits, y_hits

        # The jit function converts Filter10 into a jitted function, basically re-writting the code in a much faster to run machine code.
        jitted_filter10_Prot = jit(nopython=True)(Filter10_Prot)

        # X, Y, and Z coordinates for the center of mass of the object. These are used for the 3D object trajectory model
        x_center = np.empty(0)
        y_center = np.empty(0)
        z_center = np.empty(0)

        max_x = 0 # Stores maximum width of boxes for 3D object trajectory model

        # Below here is a while loop that loops through the video data in increments.
        index3 = 0
        while index3 < 39: #Iterations needed for current 3D object trajectory model
            # Call the first filter and return the data to x_hits and y_hits.
            x_hits, y_hits = jitted_filter1_Prot(events, min_Prot, max_Prot)

            # Call filter10 and return the data to x_hits0 and y_hits0.
            x_hits0, y_hits0 = jitted_filter10_Prot(events, min_Prot, max_Prot)

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
                x_hits, y_hits = jitted_filter2_Prot(x_hits, y_hits)
                x_hits0, y_hits0 = jitted_filter2_Prot(x_hits0, y_hits0)
                index += 1

            # Combine pixels of 1 and -1 polarity
            x_combined = np.concatenate((x_hits, x_hits0))
            y_combined = np.concatenate((y_hits, y_hits0))

            # Prints time to console
            total_time = round((time.time() - start_time_Prot), 2)
            print("Total points on plot after second (+1) filter: ", len(x_hits))
            print("Total points on plot after second (-1) filter: ", len(x_hits0))
            print("Execution time: %s seconds" % (total_time))
            print("On Image #", index3)

            # Plots data
            #bisque_patch = mpatches.Patch(color='pink', label='First (+1) Filter output')
            #red_patch = mpatches.Patch(color='red', label='Second (+1) Filter output')
            #skyblue_patch = mpatches.Patch(color='skyblue', label='First (-1) Filter output')
            #blue_patch = mpatches.Patch(color='blue', label='Second (-1) Filter output')
            title = "Time Increment: " + str(min_Prot) + " to " + str(max_Prot)
            plt.title(title)
            #plt.legend(handles=[red_patch, bisque_patch, blue_patch, skyblue_patch], loc=1)
            plt.xlim(0, 350)
            plt.ylim(0, 250)
            plt.scatter(x_hits, y_hits, s=0.5, c='pink')
            plt.scatter(x_hits0, y_hits0, s=0.5, c='skyblue')

            #temporary variables for holding the output of the last tracking function
            temp_x_hits = x_combined
            temp_y_hits = y_combined

            #Positive pixels inside all of the boxes drawn
            x_inside1_p = np.empty(0)
            y_inside1_p = np.empty(0)

            #Negative pixels inside all of the boxes drawn
            x_inside1_n = np.empty(0)
            y_inside1_n = np.empty(0)

            #Execute tracking function until we hit a certain number of loops or there are no pixels left to track
            index = 0
            while len(temp_x_hits) > 0 and index < max_tracking_iterations_Prot:
                x_object, y_object, x_right, y_right, x_left, y_left, x_top, y_top, x_bottom, y_bottom, x_outside, y_outside, x_inside, y_inside = jitted_filter5_Prot(sample_size_Prot, min_distance_Prot, min_hits_Prot, tolerance_Prot, temp_x_hits, temp_y_hits)

                #Use updated list of pixels for the next function (will either have pixels deleted from the sample square not having enough pixels or from a box that was already drawn)
                temp_x_hits = x_outside
                temp_y_hits = y_outside

                #If there wasn't enough pixels, don't draw a box
                no_object = False
                if x_object == 0 and y_object == 0:
                    no_object = True

                if not no_object:
                    #Store coordinates for center of mass of object for 3D model
                    x_center = np.append(x_center, x_object)
                    y_center = np.append(y_center, y_object)
                    z_center = np.append(z_center, x_right - x_left) #For now, z_center is the width of the box. This is manipulated later

                    #Store the maximum width of boxes for 3D object trajectory model
                    if max_x < x_right - x_left:
                        max_x = x_right - x_left

                    #Draw square as well as the center, top, bottom, left, and right
                    plt.scatter(x_object, y_object, s=10, c='g')
                    plt.scatter(x_right, y_right, s=10, c='g')
                    plt.scatter(x_left, y_left, s=10, c='g')
                    plt.scatter(x_top, y_top, s=10, c='g')
                    plt.scatter(x_bottom, y_bottom, s=10, c='g')
                    rectangle = plt.Rectangle((x_left, y_bottom), x_right - x_left, y_top - y_bottom, fc='none', ec="green") #Draw rectangle around the object
                    plt.gca().add_patch(rectangle)

                    #Find positive pixels inside all of the boxes drawn
                    index1 = 0
                    while index1 < len(x_hits):
                        if x_hits[index1] <= x_right and x_hits[index1] >= x_left and y_hits[index1] <= y_top and y_hits[index1] >= y_bottom:
                            x_inside1_p = np.append(x_inside1_p, x_hits[index1])
                            y_inside1_p = np.append(y_inside1_p, y_hits[index1])
                        index1 += 1

                    #Find negative pixels inside all of the boxes drawn
                    index1 = 0
                    while index1 < len(x_hits0):
                        if x_hits0[index1] <= x_right and x_hits0[index1] >= x_left and y_hits0[index1] <= y_top and y_hits0[index1] >= y_bottom:
                            x_inside1_n = np.append(x_inside1_n, x_hits0[index1])
                            y_inside1_n = np.append(y_inside1_n, y_hits0[index1])
                        index1 += 1
                index += 1

            #Highlight pixels inside of boxes
            plt.scatter(x_inside1_p, y_inside1_p, s=0.5, c='r')
            plt.scatter(x_inside1_n, y_inside1_n, s=0.5, c='b')
            plt.savefig(os.path.dirname(__file__) + '\\Results\\Prototype\\' + str(index3))
            plt.clf()

            # Increment time.
            min_Prot = min_Prot + increment_Prot
            max_Prot = max_Prot + increment_Prot
            index3 += 1

        z_temp = 0 #Used for saving the last Z coordinate
        max_z = 0 #Used for finding the largest Z coordinate. This is used for scaling

        i = 0
        while i < len(z_center):
            z_center[i] = z_temp + ((z_center[i] / abs(z_center[i])) * (max_x - abs(z_center[i]))) #Add difference between max width and the current width to the last z coordinate to get the current z coordinate. Factor in front is used for when it's negative, denoting travel towards the camera
            z_temp = z_center[i] #Set z_temp to the current coordinate for next iteration
            if max_z < z_temp: #Set the max z coordinate for scaling
                max_z = z_center[i]
            i += 1

        #Scale z axis between 0 and 300
        i = 0
        while i < len(z_center):
            z_center[i] = (300 * (z_center[i])) / max_z
            i += 1

        #Plot 3D figure
        threeD = plt.figure()
        ax = threeD.add_subplot(111, projection='3d')
        ax.set_xlabel("X")
        ax.set_ylabel("Z")
        ax.set_zlabel("Y")
        ax.set_xlim(0, 350)
        ax.set_ylim(0, 350)
        ax.set_zlim(0, 250)

        ax.scatter(x_center, z_center, y_center, color='black') #Plot points

        #Arrays containing phi and theta angles for 3D vectors
        pose_phi = np.empty(0)
        pose_theta = np.empty(0)

        #Calculate angles for vectors and plot them as arrows
        i = 1
        while i < len(x_center) - 1: #Do not calculate vectors for first and last points
            #phi1/theta1 are angles for vector from previous point to current point
            phi1 = np.arctan((x_center[i + 1] - x_center[i]) / (z_center[i + 1] - z_center[i]))
            theta1 = np.arctan((y_center[i + 1] - y_center[i]) / np.sqrt(np.square(x_center[i + 1] - x_center[i]) + np.square(z_center[i + 1] - z_center[i])))

            #phi2/theta2 are angles for vector from current point to next point
            phi2 = np.arctan((x_center[i] - x_center[i - 1]) / (z_center[i] - z_center[i - 1]))
            theta2 = np.arctan((y_center[i] - y_center[i - 1]) / np.sqrt(np.square(x_center[i] - x_center[i - 1]) + np.square(z_center[i] - z_center[i - 1])))

            #Average vectors before and after current point to get vector of current point
            phi = (phi1 + phi2) / 2
            pose_phi = np.append(pose_phi, 180 - np.degrees(phi)) #Phi is flipped for ease of view because z axis is flipped
            theta = (theta1 + theta2) / 2
            pose_theta = np.append(pose_theta, theta)

            print("Pose " + str(i - 1) + ": " + "phi = " + str(180 - np.degrees(phi)) + ", theta = " + str(np.degrees(theta)))

            #Show arrows on graph
            x_point = 25 * np.sin(phi)
            z_point = 25 * np.cos(phi)
            y_point = 25 * np.sin(theta)
            ax.quiver(x_center[i], z_center[i], y_center[i], x_point, z_point, y_point, length=15, normalize=True, arrow_length_ratio=0.1)
            ax.text(x_center[i], z_center[i], y_center[i], str(i - 1))

            i += 1


        plt.savefig(os.path.dirname(__file__) + '\\Results\\Prototype\\' + "3D.pdf")
        plt.show()
