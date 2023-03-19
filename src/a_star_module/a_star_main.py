import numpy as np

from src.a_star_module.generate_map import map_generator
from src.a_star_module.generate_path import path_generator
from src.a_star_module.spline_path import spline_path

class A_star():
  def __init__(self, resolution, waypoints):
    self.map_size = np.array([2.1,3.3])

    self.resolution = resolution

    self.waypoints = waypoints

    # Obstacle polygon corners
    self.obstacle_list = [np.array([[0, .3], [0, .605], [1.22, .605], [1.22, .3]]),
                          np.array([[0,-.3], [0,-.605], [1.22,-.605], [1.22,-.3]])]

    self.M = map_generator(self.map_size, self.obstacle_list, self.waypoints, self.resolution)

  def calculate_path(self):
    # Initializes A* core node. Takes a B&W map and a resolution scalar
    P = path_generator(self.M.map, self.resolution)

    overlay = P.overlay

    path_cumulative = np.array([self.waypoints[0].astype(int)])

    for i in range(len(self.waypoints)-1):
      P.A_star(self.waypoints[i], self.waypoints[i+1], i)

      overlay += P.overlay

      path_cumulative = np.append(path_cumulative, P.path * self.resolution, axis=0)
    
    smoothed_path = spline_path(path_cumulative[:,0], path_cumulative[:,1], self.resolution/10)

    self.pts = smoothed_path.transpose()

    self.final = (overlay*P.map_basic).astype('uint8')

  def get_map(self):
    return self.M.get_map()

  def get_map2(self):
    return self.final

  def get_lines(self):
    return self.pts