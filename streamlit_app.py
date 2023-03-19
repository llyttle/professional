# import numpy as np
# import cv2

# from map_navigation.a_star_main import A_star

import streamlit as st
# from streamlit_image_coordinates import streamlit_image_coordinates as get_image_coord
# from PIL import Image

# import matplotlib.pyplot as plt
# import plotly.express as px

# class StreamlitInterface:
#   def __init__(self):
#     self.figure_width = 600
#     self.image_scalar = 0

#     self.placeholder = st.empty()

#   def config_for_streamlit(self, img):
#       self.image_scalar = int(self.figure_width / img.shape[1])

#       dim = np.array(img.shape[0:2]) * self.image_scalar
#       resized = cv2.resize(img, dim[::-1], interpolation = cv2.INTER_AREA)

#       return Image.fromarray(np.uint8(resized)).convert('RGB')

#   def waitfor_mouse_point(self, img):
#     coord = get_image_coord(img, key="start")

#     if not coord:
#       return
    
#     point = np.array([float(p) for p in coord.values()]) / self.image_scalar

#     if len(st.session_state["waypoint_list"]) > 0:
#       if np.all(point == st.session_state["waypoint_list"][-1]):
#           return
      
#     st.session_state["waypoint_list"].append(point)
#     st.experimental_rerun()

#   def res_slider(self):
#     st.session_state['waypoint_list'] = []

#   def rerun_button(self):
#     st.session_state['waypoint_list'] = []

#   def run(self):
#     if 'waypoint_list' not in st.session_state:
#       st.session_state['waypoint_list'] = []


#     st.button("Re-Run", on_click=self.rerun_button)

#     resolution_update = st.slider("Map Resolution (in px/m)", min_value=8, max_value=100, value=12, step=1, on_change=self.res_slider)
#     a = A_star(resolution_update, st.session_state["waypoint_list"])


#     if len(st.session_state['waypoint_list']) < 3:
#       PIL_image = self.config_for_streamlit(a.get_map())

#       self.waitfor_mouse_point(PIL_image)

#     else:      
#       # PIL_image = self.config_for_streamlit(a.get_map())

#       # self.placeholder.image(PIL_image)

#       a.calculate_path()
#       line = a.get_lines()

#       fig, ax = plt.subplots()
#       plt.cla()
#       plt.imshow(a.get_map2())
#       plt.plot(line[:,0], line[:,1], 'b', alpha=.7, linewidth=3)
#       plt.axis('equal')

#       ax.patch.set_edgecolor('black')  
#       ax.patch.set_linewidth(1)

#       plt.tick_params(which='both',
#                       bottom=False, top=False, left=False, right=False,
#                       labelbottom=False, labeltop=False, labelleft=False, labelright=False
#                     )

#       st.pyplot(fig)

   

# if __name__ == "__main__":
# # Main streamlit interface. Reruns with each user input

#   page = StreamlitInterface()
#   page.run()


#   # a.calculate_path(resolution)
