'''
SCript to generate mic positions on side (vertical) planes and save them as excel file
'''


## Seitenflächen
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

SideGrid_w = 1.38
SideGrid_h = 1.82

M = 20 #number of virtual mics
m = np.arange(M)
V = 5
R = SideGrid_h/2

# Vogel's plot
r = R*np.sqrt(m/M)
phi = 2*np.pi*m*((1+np.sqrt(V))/2)

x = np.asarray(r*np.cos(phi))
y = np.asarray(r*np.sin(phi))
coord = np.array([x,y])
coord_cut_side = np.array([x[(x >= -SideGrid_w/2) & (x <= SideGrid_w/2)],y[(x >= -SideGrid_w/2) & (x <= SideGrid_w/2)]])
coord_cut_side = coord_cut_side[:,1:]

# Sort coord_cut_side based on the y-values (second row)
sorted_indices = np.argsort(coord_cut_side[1, :])  # Get indices that sort the y-values
coord_cut_side_sorted = coord_cut_side[:, sorted_indices]  # Sort by y-values

len_side = len(coord_cut_side_sorted[1])

plane_names_short = ["B", "C", "D"]
plane_names_long = ["right", "front", "left"]

data = []
for letter, name in zip(plane_names_short, plane_names_long):
    for i in range(0, len_side):
        mic_index = letter + str(i+1)
        x = round(coord_cut_side_sorted[0,i]+SideGrid_w/2,3)
        y = round(coord_cut_side_sorted[1,i]+SideGrid_h/2,3)

        # Append the row as a dictionary
        data.append({"Mic_Index": mic_index, "Plane": name, "X": x, "Y": y})


# Convert the list of dictionaries to a pandas DataFrame
side_positions = pd.DataFrame(data)
side_positions["X measured"] = None
side_positions["Y measured"] = None
# Print the resulting DataFrame
print(side_positions)

# save as excel file

side_positions.to_excel("mic_positions/data/side_postions.xlsx")


