import streamlit as st

import numpy as np

from map_navigation.generate_map import map_generator
from map_navigation.generate_path import path_generator

import matplotlib.pyplot as plt

from map_navigation.spline_path import spline_path

if __name__ == "__main__":
  # Obstacle polygon corners
  obstacle_list = [np.array([[0, .3], [0, .605], [1.22, .605], [1.22, .3]]),
                   np.array([[0,-.3], [0,-.605], [1.22,-.605], [1.22,-.3]])]

  waypoints = {"A": np.array([-1,-.8]),
               "B": np.array([ 1.2, .8]),
               "C": np.array([-.6,  0]),
               "D": np.array([-.6, .3]),
               "E": np.array([-.6, .6]),
               "F": np.array([1.3,-.6])}
  
  map_size = np.array([2.1,3.3])


  resolution = 50   # Resolution of solution in pixels per meter. Min = 8 px/m


  #BE WARNED: this funciton also changes the obstacle and waypoints lists
  M = map_generator(map_size, obstacle_list, waypoints, resolution)

  P = path_generator(M.map, resolution)

  P.A_star(waypoints["A"], waypoints["B"])

  P.path = np.flipud(P.path)

  new_waypoints = spline_path(P.path[:,0], P.path[:,1], 60)


  placeholder = st.empty()

  placeholder.image((M.overlay*P.overlay*P.map_basic).astype('uint8'))

  # if True:
  #   plt.cla()

  #   plt.imshow((M.overlay*P.overlay*P.map_basic).astype('uint8'), interpolation='nearest')
  #   plt.plot(new_waypoints[0]*resolution, new_waypoints[1]*resolution, 'b', alpha=.7, linewidth=3)
  #   plt.axis('equal')
  #   plt.show
  #   plt.pause(10)

