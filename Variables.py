##### FILTER Variables #####

# The time_range is how far back in time and in the future of the current index does the program check for hits
# This has the largest hit on performance (Exponentially).
time_range = 7

# Positive is the minimum number of neighbor hits that must be attained for the hit to be added to the plot.
positive = 2

# The max_distance is the maximum distance in a 3d space
# Where z is time that a hit must be under to be added to the plot.
max_distance = 10

# The increment is the duration of time stamps the program will process at a time then plot to a graph.
increment = 10000

# The event number after the increment from which the filter starts
min = 0

# The number of events filtered into a single frame
max = 40000



##### TRACKING Variables #####

# Determines how large a sample size we should take for averaging pixels to find the center of an object
sample_size = 40

# Threshold for number of misses in a row before we "give up" and use the last hit as a bound
min_distance = 10

# Minimum number of hits within a sample required to identify it as an object and draw a box
min_hits = 50

# How much bigger should the box be then the object
tolerance = 5

# How many times should we iterate the tracking function before we give up
max_tracking_iterations = 50