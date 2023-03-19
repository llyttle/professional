import numpy as np
from scipy.interpolate import splprep, splev

def spline_path(x, y, fit):
    """ Takes x, y path points in meters and fits a smooth curve to the path. 
        Also calculates the yaw and makes all z values 1 m.
    """
    tck, _ = splprep([x, y], s=fit, per=False)
    u = np.linspace(0,1,num=100)
    new_points = splev(u, tck)

    return np.array(new_points)
