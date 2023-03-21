import numpy as np
import cv2

from src.a_star_module.a_star_main import A_star

import streamlit as st
from streamlit_image_coordinates import streamlit_image_coordinates as get_image_coord
from PIL import Image

import time

import matplotlib.pyplot as plt

class StreamlitInterface:
  def __init__(self):
    self.figure_width = 600
    self.image_scalar = 0

    self.placeholder = st.empty()

    self.run()

    # try:
    #   self.run()
    # except:
    #   st.write("Error Occured, Refreshing...")
    #   time.sleep(1)
    #   self.rerun_button()

  #===================================================================================
  #=== Streamlit Callbacks ===========================================================
  
  def res_slider(self):
    st.session_state['waypoint_list'] = []

  def rerun_button(self):
    st.session_state['waypoint_list'] = []
  
  #=== Streamlit Callbacks ===========================================================
  #===================================================================================

  def config_for_streamlit(self, img):
    """ Resize an image to the desired 'figure_width' dislpayed in streamlit
        and save conversion scalar for later """
    self.image_scalar = int(self.figure_width / img.shape[1])

    dim = np.array(img.shape[0:2]) * self.image_scalar
    resized = cv2.resize(img, dim[::-1], interpolation = cv2.INTER_AREA)

    return Image.fromarray(np.uint8(resized)).convert('RGB')

  def waitfor_mouse_point(self, img):
    """ Wait for mouse pointer to click an image and save the coordinates
        to session_state """
    coord = get_image_coord(img, key="start")

    if not coord:
      return
    
    point = np.array([float(p) for p in coord.values()]) / self.image_scalar

    if len(st.session_state["waypoint_list"]) > 0:
      if np.all(point == st.session_state["waypoint_list"][-1]):
          return
      
    st.session_state["waypoint_list"].append(point)
    st.experimental_rerun()

  def run(self):
    # Initialize waypoint list on first run loop
    if 'waypoint_list' not in st.session_state:
      st.session_state['waypoint_list'] = []

# ==========================================================================================
# == Streamlit Interface Buttons ===========================================================

    # Set resolution with sidebar slider. Use callback to trigger page refresh
    resolution_update = st.sidebar.slider("Map Resolution (in px/m)", min_value=8, max_value=100, value=28, step=1, on_change=self.res_slider)
    
    # Set the number of waypoints with a sidebar slider
    num_waypoints = st.sidebar.slider("Number of waypoints", min_value=2, max_value=5, value=2, step=1, on_change=self.res_slider)

    # Place re-run button on the bottom of page. Use callback to trigger page refresh
    st.sidebar.button("Re-Run", on_click=self.rerun_button)

# ==========================================================================================

    # Initialize a_star node with a resolution and the current list of waypoints
    a = A_star(resolution_update, st.session_state["waypoint_list"])

    # Check if all waypoints have been defined
    if len(st.session_state['waypoint_list']) < num_waypoints:
      PIL_image = self.config_for_streamlit(a.get_map())

      self.waitfor_mouse_point(PIL_image)

    else:      
      a.calculate_path()
      line = a.get_lines()

      fig, ax = plt.subplots()
      plt.cla()
      plt.imshow(a.get_map2())
      plt.plot(line[:,0], line[:,1], 'b', alpha=.7, linewidth=3)
      plt.axis('equal')

      ax.patch.set_edgecolor('black')  
      ax.patch.set_linewidth(1)

      plt.tick_params(which='both',
                      bottom=False, top=False, left=False, right=False,
                      labelbottom=False, labeltop=False, labelleft=False, labelright=False
                    )

      st.pyplot(fig)

if __name__ == "__main__":
  # Main streamlit interface. Reruns with each user input
  page = StreamlitInterface()