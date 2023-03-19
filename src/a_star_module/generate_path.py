import cv2
import numpy as np
import matplotlib.pyplot as plt

# import sys

class Node:
  def __init__(self, pos, f=0, g=0, h=0, parent=None):
    self.pos = pos
    self.name = np.array2string(pos)
    self.parent = parent
    self.f = f
    self.g = g
    self.h = h

class nodeDict:
  def __init__(self):
    self._D = {}

  def get(self, node):
    return self._D[node.name]
    
  def add(self, node):
    self._D[node.name] = node

  def delete(self, node):
    self._D.pop(node.name)
  
  def length(self):
    return len(self._D)
  
  def contains(self, node):
    return (node.name in self._D)
  
  def pop_lowest_weight(self):
    lowest = None
    for node in self._D.values():
      if lowest == None or lowest.f > node.f:
        lowest = node

    return self._D.pop(lowest.name)
  


class path_generator:
  def __init__(self, map, resolution):
    # blur_const must be an odd integer no smaller than 3
    blur_const = int(resolution/10)*2 + 1
    blur_const = max(blur_const, 3)
    blur_map = cv2.GaussianBlur(map, (blur_const,blur_const), cv2.BORDER_DEFAULT)

    # 2D map for A* operations
    self.map = blur_map * (map==255)
    # self.map = map

    self.map_basic = np.repeat(map[:, :, np.newaxis], 3, axis=2)

    # 'Color' B&W map to combine with self.overlay
    self.map_img = np.repeat(self.map[:, :, np.newaxis], 3, axis=2)

    # Overlay used for visualizations without changin map
    self.overlay = np.ones(np.append(self.map.shape,3))   #Add 3 layers to create an RGB image

    # Resolution of map used for unit conversion back to meters
    self.resolution = resolution

    # Solved path as np array of (x,y) points in image coordinate frame
    self.path = None


    # If Plotting from this script, uncomment:
    # ---------------------------------------------------------------------

    # self.fig = plt.figure()
    # self.viewer = self.fig.add_subplot(111)

    # self.viewer.tick_params(labelbottom=False)
    # self.viewer.tick_params(labelleft=False)

    # mng = plt.get_current_fig_manager()
    # mng.resize(*mng.window.maxsize())

    # ---------------------------------------------------------------------

  def A_star(self, start, end, path_num):
    start = start.astype(int)
    end = end.astype(int)

    open = nodeDict()
    open.add(Node(start))

    closed = nodeDict()

    progress = np.inf

    while open.length() != 0:
      q = open.pop_lowest_weight()
      closed.add(q)

      # progress = min(progress, self.distance(q.pos, end))
      # sys.stdout.write("\033[K")
      # print("Connection ", path_num, ": Pathfinding Progress = %", (1- progress/self.distance(start, end))*100, end='\r')

      if np.array_equal(q.pos, end):
        print("")
        print("Solution Found")

        path = []
        node = q
        while node.parent != None:
          path.append(node.pos.tolist())

          node = node.parent

          self.update_overlay(node.pos, np.array([1, .6, .6]))
          # Redraw start and end points over
          self.update_overlay(start, np.array([0,1,0]))
          self.update_overlay(end, np.array([1,.5,0]))

          # self.show()

        # Final Step: Update member path variable and plot start and endpoints over drawn lines
        self.path = np.flipud(np.asarray(path) / self.resolution)

        # self.show()
        # plt.pause(1)

        break

      # set each neighbor as distance 1 from q
      descendants = [ Node(q.pos + [-1, 1], parent=q),
                      Node(q.pos + [ 0, 1], parent=q),
                      Node(q.pos + [ 1, 1], parent=q),
                      Node(q.pos + [-1, 0], parent=q),
                      Node(q.pos + [ 1, 0], parent=q),
                      Node(q.pos + [-1,-1], parent=q),
                      Node(q.pos + [ 0,-1], parent=q),
                      Node(q.pos + [ 1,-1], parent=q)]

      # # for successor in descendants
      for s in descendants:
        # if outside map
        if not ((0<=s.pos[1]<self.map.shape[0]) and (0<=s.pos[0]<self.map.shape[1])):
          break
        # if on an obstacle
        if self.map[s.pos[1], s.pos[0]] == 0.0:
          break

        # ===============================================================================
        # A* Heuristics Behavior
        proximity_penalty = 100* (1 - self.map[s.pos[1], s.pos[0]]/255)

        # s.g = self.distance(s.pos, start)
        s.g = self.distance(s.pos, q.pos) + q.g
        # s.g = 1 + q.g
        s.h = self.distance(s.pos, end)
        s.f = s.g + s.h + proximity_penalty

        # ===============================================================================

        # if discovered and on open
        if open.contains(s):
          s_prior = open.get(s)
          if s_prior.f > s.f:
            open.delete(s_prior)
            open.add(s)
        # if discovered and on closed
        elif closed.contains(s):
          s_prior = closed.get(s)
          if s_prior.f > s.f:
            closed.delete(s_prior)
            open.add(s)
        # if undiscovered
        else:
          open.add(s)

        # Show q's neighbors as grey on the map
        # self.update_overlay(s.pos, np.array([.9,.9,.9]))

      # Show q and it's trail path as it solves the map
      # self.update_overlay(q.pos, np.array([0, 1, 0]))
      # self.update_overlay(last_drawn, np.array([.7,.7,.7]))
      # last_drawn = q.pos

      # self.show()
    
  def distance(self, p1, p2):
    return np.linalg.norm(p1 - p2)
    # return np.sqrt((p1[1]**2 + p2[1]**2) - (p1[0]**2 + p2[0]**2))

  def update_overlay(self, point, color):
    self.overlay[point[1], point[0], :] = color
    
  def show(self):
    self.viewer.clear()

    self.viewer.imshow((self.map_img*self.overlay).astype('uint8'), interpolation='nearest')

    self.fig.canvas.draw()

    plt.pause(.01)