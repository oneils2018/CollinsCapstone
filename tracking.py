import numpy as np
from Variables import *
import math as math

    ################
    ### TRACKING ###
    ################

    #Function below takes filtered data and outputs the object center and left, right, top, and bottom bounds
    #min_distance is the minimum distance that the algorithm reaches before it "gives up" trying to find more pixels and just sets the last pixel hit as the bound
    #min_hits is the minimum number of hits required to actually create a box
    #tolerance is the number of pixels to go past the original bounds to create a box that is bigger then the object



def tracking(sample_size, min_distance, min_hits, tolerance, x_hits, y_hits):
        #Arrays for keeping track of hits outside the box
        x_outside = x_hits
        y_outside = y_hits

        #Arrays for keeping track of hits inside the box
        x_inside = np.empty(0)
        y_inside = np.empty(0)

        #Coordinates for center of object
        x_average = 0
        y_average = 0

        #If the sample square goes past the edge of the frame, set the bound of the sample to the edge
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

        #Holds pixels found within the sample square
        sample_hits_x = np.empty(0)
        sample_hits_y = np.empty(0)

        #Find all pixels within the sample square
        index = 0
        while index < len(x_hits):
            if x_hits[index] <= sample_right and x_hits[index] >= sample_left and y_hits[index] <= sample_top and y_hits[index] >= sample_bottom:
                sample_hits_x = np.append(sample_hits_x, x_hits[index])
                sample_hits_y = np.append(sample_hits_y, y_hits[index])
            index += 1

        #Calculate the average for pixels within the sample square to find the center of object
        index = 0
        while index < len(sample_hits_x):
            x_average += sample_hits_x[index]
            y_average += sample_hits_y[index]
            index += 1

        #If there are not enough points within the sample square, return 0 for everything except x_outside and y_outside
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

            #Store all pixels that are outside of the sample square in x_outside and y_outside and delete everything inside. The outside pixels will be used as inputs for the next tracking function
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
        #If there's enough pixels, calculate the average
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

        # Apply tolerance (user defined)
        if x_right + tolerance < 345:
            x_right = x_right + tolerance
        if x_left - tolerance > 1:
            x_left = x_left - tolerance
        if y_top + tolerance < 250:
            y_top = y_top + tolerance
        if y_bottom - tolerance > 1:
            y_bottom = y_bottom - tolerance

        #Separate pixels inside and outside of the box that we just found
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
