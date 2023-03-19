import cv2
import numpy as np

class map_generator():
  def __init__(self, size, obstacle_list, waypoints, resolution):
    self.size = (size * resolution).astype(int)
    self.resolution = resolution

    self.create_map(obstacle_list)

    if waypoints is not None:
      self.create_overlay(waypoints)
    
  def create_map(self, known_obstacles):
    self.map = np.zeros(self.size)+255

    for obj_corners in known_obstacles:
      # Flip the transform to the center of the image as pictures are (col, row) instead of (x, y)
      # All map objects must be scaled by the resolution of the map image and moved about the center
      obj_corners = (obj_corners * self.resolution) + (self.size[::-1] / 2)

      # Draw a filled polygon to represent the obstacle
      cv2.fillPoly(
        img = self.map,
        pts=[obj_corners.astype(int)],
        color=(0, 0, 0)
        )

  def create_overlay(self, point_list):
    # Initialize overlay as an array of ones * 3 for RGB
    self.overlay = np.ones(np.append(self.size,3))

    # Define a resolution scalar based on the resolution: somewhat arbitrary
    res_scalar = int(self.resolution/20)

    for point in point_list:
      waypoint = point.copy().astype(int)
      cv2.circle(self.overlay, waypoint, 0, (100, 210, 210), 1*res_scalar)
      # cv2.putText(self.overlay, label, point_dict[label] - np.array([-5,0]), cv2.FONT_HERSHEY_SIMPLEX, .1*res_scalar, (0,0,255), int(res_scalar/2))

  def get_map(self, overlay = True):
    img = np.repeat(self.map[:, :, np.newaxis], 3, axis=2)

    if overlay:
      img *= self.overlay

    return img