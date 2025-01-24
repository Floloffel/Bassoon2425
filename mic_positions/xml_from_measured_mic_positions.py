'''
script to generate xml file from measured mic positions
'''


import pandas as pd

path_to_measured_mic_positions = "mic_positions/side_postions_measured.xlsx"
df = pd.read_excel(path_to_measured_mic_positions)
print(df)

# grid dimensions
side_grid_width = 1.38 #x values in 2D plane
side_grid_height = 1.82 #y values in 2D plane 
top_grid_width = 1.42 #x values in 2D plane
top_grid_depth = 1.19 #y values in 2D plane

# distance between grid


