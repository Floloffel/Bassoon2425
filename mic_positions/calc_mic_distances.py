import pandas as pd
import numpy as np

def calculate_distance(df, name1, name2, x_col="X", y_col="Y", z_col="Z", print_coords=False, print_dist=True):
    point1 = df[df["Mic_Index"] == name1][[x_col, y_col, z_col]].iloc[0]
    point2 = df[df["Mic_Index"] == name2][[x_col, y_col, z_col]].iloc[0]
    
    # euklidische Distanz berechnen
    dist = np.sqrt((point2[x_col] - point1[x_col])**2 + 
                   (point2[y_col] - point1[y_col])**2 + 
                   (point2[z_col] - point1[z_col])**2)
    
    if print_coords == True:
        print(name1)
        print(x_col, ":", round(point1[x_col], 3))
        print(y_col, ":", round(point1[y_col], 3))
        print(z_col, ":", round(point1[z_col], 3))
        print("")
        print(name2)
        print(x_col, ":", round(point2[x_col], 3))
        print(y_col, ":", round(point2[y_col], 3))
        print(z_col, ":", round(point2[z_col], 3))

    if print_dist == True:
        print(f"{round(dist, 3)} = distance {name1} to {name2}")


    return dist