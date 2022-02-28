import time
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import math as math
from Variables import *
from Filter1 import *
from Filter2 import *
from Filter10 import *
from tracking import *
from image_classifier import *
from dualpolarityplotter import *
from object_tracking import *
# numba is a library that must be install by running "pip install numba" It takes a function and re-writes in machine code to run extremely fast. It works best if numpy arrays are used.
from numba import jit, njit, vectorize


jitted_filter1 = jit(nopython=True)(Filter1)
jitted_filter2 = jit(nopython=True)(plot_filter)
jitted_filter5 = jit(nopython=True)(tracking)
jitted_filter10 = jit(nopython=True)(Filter10)
jitted_dualpolarityplotter = jit(nopython=True)(dualpolarityplotter)
jitted_object_tracking = jit(nopython=True)(object_tracking)

#Note: Cannot jit the object_tracking function. Numba has some issue with the image when
#passing it to the tensorflow model.
