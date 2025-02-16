'''
This script contains all custom function that are used among the mic_position files.
Most of them are for the parametric position model.
'''


import numpy as np
import scipy as sp

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


# parametric model

def pandas_rotation(df_mic_coords, plane_to_rotate, roll, pitch, roll_axis, pitch_axis):
    
    # create rotation object
    planes_to_rotate_formatted = roll_axis+pitch_axis
    r = sp.spatial.transform.Rotation.from_euler(planes_to_rotate_formatted, [roll, pitch], degrees=True)
    
    # filter plane to rotate (left, rigth, etc.)
    filtered_df = df_mic_coords[df_mic_coords['Plane'].isin([plane_to_rotate])]

    coordinates = filtered_df[["X_optimized", "Y_optimized", "Z_optimized"]].to_numpy()

    # Apply the rotation to the filtered subset of coordinates
    rotated_coordinates = r.apply(coordinates)

    # Update the original DataFrame with the rotated coordinates
    df_mic_coords.loc[filtered_df.index, ['X_optimized', 'Y_optimized', 'Z_optimized']] = rotated_coordinates

    return df_mic_coords



def parametric_model(df_mic_coords, parameters):

    # copy initial coords to preserve them
    df_mic_coords["X_optimized"] = df_mic_coords["X"]
    df_mic_coords["Y_optimized"] = df_mic_coords["Y"]
    df_mic_coords["Z_optimized"] = df_mic_coords["Z"]

    # top plane x,y shift
    df_mic_coords.loc[df_mic_coords["Plane"].isin(["top"]), "X_optimized"] += parameters[0]
    df_mic_coords.loc[df_mic_coords["Plane"].isin(["top"]), "Y_optimized"] += parameters[1]

    # left plane y,z shift and rotation
    df_mic_coords.loc[df_mic_coords["Plane"].isin(["left"]), "Y_optimized"] += parameters[2]
    df_mic_coords.loc[df_mic_coords["Plane"].isin(["left"]), "Z_optimized"] += parameters[3]
    df_mic_coords = pandas_rotation(df_mic_coords, "left", parameters[4], parameters[5], "y", "z")

    # front plane x,z shift and rotation
    df_mic_coords.loc[df_mic_coords["Plane"].isin(["front"]), "X_optimized"] += parameters[6]
    df_mic_coords.loc[df_mic_coords["Plane"].isin(["front"]), "Z_optimized"] += parameters[7]
    df_mic_coords = pandas_rotation(df_mic_coords, "front", parameters[8], parameters[9], "x", "z")

    # right plane x,y,z shift & rotatiotn
    df_mic_coords.loc[df_mic_coords["Plane"].isin(["right"]), "X_optimized"] += parameters[10]
    df_mic_coords.loc[df_mic_coords["Plane"].isin(["right"]), "Y_optimized"] += parameters[11]
    df_mic_coords.loc[df_mic_coords["Plane"].isin(["right"]), "Z_optimized"] += parameters[12]
    df_mic_coords = pandas_rotation(df_mic_coords, "right", parameters[13], parameters[14], "y", "z")

    return df_mic_coords



def calc_error_optimized_coords(df_distances, df_mic_coords_moved):

    for index, row in df_distances.iterrows():
        dist_optimized = calculate_distance(
            df_mic_coords_moved, row[0], row[1], print_dist=False, 
            x_col="X_optimized", y_col="Y_optimized", z_col="Z_optimized"
            )    
        sq_error = (dist_optimized - df_distances["dist measured"][index])**2
        df_distances.loc[index, "squared error optimized"] = sq_error

    sum_sq_errors = df_distances["squared error optimized"].sum()
    return sum_sq_errors, df_distances


