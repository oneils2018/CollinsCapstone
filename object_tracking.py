import numpy as np
import math as math
import os
import tensorflow as tf
import cv2
from keras.preprocessing import image
from matplotlib import pyplot as plt
from numba import jit, njit, vectorize
from Variables import *
from functions import *
    ################
    ### TRACKING ###
    ################

    #Function below takes filtered data and outputs the object center and left, right, top, and bottom bounds
    #min_distance is the minimum distance that the algorithm reaches before it "gives up" trying to find more pixels and just sets the last pixel hit as the bound
    #min_hits is the minimum number of hits required to actually create a box
    #tolerance is the number of pixels to go past the original bounds to create a box that is bigger then the object


jitted_filter5 = jit(nopython=True)(tracking)

def object_tracking(x_combined, y_combined, index3, x_hits, y_hits, x_hits0, y_hits0, sample_size, min_distance, min_hits, tolerance, max_tracking_iterations, directorySelVar, model, make_test_data):
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
    while len(temp_x_hits) > 0 and index < max_tracking_iterations:
        x_object, y_object, x_right, y_right, x_left, y_left, x_top, y_top, x_bottom, y_bottom, x_outside, y_outside, x_inside, y_inside = jitted_filter5(sample_size, min_distance, min_hits, tolerance, temp_x_hits, temp_y_hits)

        #Use updated list of pixels for the next function (will either have pixels deleted from the sample square not having enough pixels or from a box that was already drawn)
        temp_x_hits = x_outside
        temp_y_hits = y_outside

        #If there wasn't enough pixels, don't draw a box
        no_object = False
        if x_object == 0 and y_object == 0:
            no_object = True

        if not no_object:
            #Draw square as well as the center, top, bottom, left, and right
            plt.scatter(x_object, y_object, s=10, c='g')
            plt.scatter(x_right, y_right, s=10, c='g')
            plt.scatter(x_left, y_left, s=10, c='g')
            plt.scatter(x_top, y_top, s=10, c='g')
            plt.scatter(x_bottom, y_bottom, s=10, c='g')
            rectangle = plt.Rectangle((x_left, y_bottom), x_right - x_left, y_top - y_bottom, fc='none', ec="green") #Draw rectangle around the object
            plt.gca().add_patch(rectangle)

            #Save a zoomed in image on the object tracking box to be sent to the image classification funtion.
            plt.xlim(x_left, x_right)
            plt.ylim(y_top, y_bottom)
            plt.savefig(directorySelVar + str(index3)+"zoom"+str(index))

            #This if statement checks if the make_test_data is set to false, if so it makes a prediction on the data, and deletes the zoomed images used after
            #in order to only output the classified data.
            if(make_test_data == 0):
                #call image classification function to test image against a trained model, then return prediction.
                prediction = image_classifier(index,index3, directorySelVar, model)
                plt.text(x_left,y_bottom,prediction)
                os.remove(directorySelVar + str(index3)+"zoom"+str(index)+".png")

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


