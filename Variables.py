"""

Description:
    The variables down below are used for filters

    The time_range is how far back in the past and in the future of the current index does
    the program check for hits. It effects the performance the most.

    Positive represent the minimum number of neighbor hitts that will be attained for the hit to be added to the plot.

    max_distance represent the maximum distance in a 3d space. Z is time that a hit must be under to be added to the plot.

    Increment represent the duration of time stamps the program will process at a time then plot to a graph.
    The event number after the increment from which the filter starts the number of events filtered into a single frame

"""

"""

Description:
   Tracking variables:
        samples_size checks how large a sample size should be by averaging pixels to find the center of an object
        
        min_distance is the origin for the number of misses in a row before we "give up" and use the last hit as a bound
        
        min_hits is the minimum number of hits that is within a sample required to identify it as an object and draw the box 
        
        tolerance represent hos big should the box be 
        
        max_tacking_iterations is how many times should we iterate the tracking function before we give up
    
"""

time_range = 7
positive = 2
max_distance = 10
increment = 10000
min = 0
max = 40000
sample_size = 40
min_distance = 10
min_hits = 50
tolerance = 5
max_tracking_iterations = 50
