import numpy as np
from Variables import *
import math as math

    ############################
    # Filter10 For -1 Polarity #
    ############################

#This function takes the output from Filter 1 and filters it just using the distances from a hit point and its nearest neighbors, not taking
#into account the time variable.


def Filter10(events, min, max, time_range, max_distance, positive):
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
