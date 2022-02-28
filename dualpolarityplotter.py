import numpy as np
from Variables import *
import math as math

# Definition for function that takes the found hits and both polariteis, that if have a pixel on the same point are combined and plotted in a new color.
def dualpolarityplotter(x_hits,y_hits,x_hits0,y_hits0):
        xdouble_hits = np.empty(0)
        ydouble_hits = np.empty(0)
        index2 = 0
        index = 0
        while index < x_hits.size:
            index2 = 0
            while index2 < x_hits0.size:
                
                if(x_hits[index] == x_hits0[index2] and y_hits[index] == y_hits0[index2]):
                    xdouble_hits = np.append(xdouble_hits, x_hits[index])
                    ydouble_hits = np.append(ydouble_hits, y_hits[index])
                    x_hits = np.delete(x_hits, index)
                    x_hits0 = np.delete(x_hits0, index2)
                    y_hits = np.delete(y_hits, index)
                    y_hits0 = np.delete(y_hits0, index2)
                    index2 = x_hits0.size
                index2 = index2+1
            index = index+1
        return xdouble_hits, ydouble_hits
