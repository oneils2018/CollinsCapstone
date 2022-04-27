import numpy as np
from Variables import *
import math as math

################
### FILTER 2 ###
################

#This function takes the output from Filter 1 or Filter 10 and filters it just using the distances from a hit point and its nearest neighbors, not taking
#into account the time variable.


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
