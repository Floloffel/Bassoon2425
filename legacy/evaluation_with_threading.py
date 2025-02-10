'''
This script is based on the jupyter notebook Auswerteschleife.ipynb from 09.02.2025. 
'''

# Import libraries
import os
import acoular as ac
import numpy as np
import pyfar as pf
import time
import h5py

from evaluation_config import eval_conf
from _calc_single_audio_frame import calc_audio_frame

# define paths
path_audio_data = "./evaluation/" + eval_conf["in_folder"] + "array_audio_data/2025-01-28_15-59-01_400437.h5"
path_mic_geom = "./evaluation/"+  eval_conf["in_folder"] + "array_position_data/bassoon_cage_64_optimized.xml"
path_result_file = "./evaluation/" + eval_conf["out_folder"] + "2025-01-28_15-59-01_400437_eval_test2"

# define parameters
resolution = eval_conf["calc_grid_res_meters"]
start = 0 #seconds
stop = 105 
bandwith = eval_conf["bandwidth"]
frequency_bands = eval_conf["frequency_bands"]
sample_freq = ac.MaskedTimeSamples(name = path_audio_data).sample_freq

frame_rate = eval_conf["framereate_fps"]
frame_length = 1/frame_rate
frame_amount = int((stop-start)*frame_rate)




# acoular set up

m = ac.MicGeom(from_file=path_mic_geom)
g = ac.RectGrid3D(
    x_min=eval_conf["x_min"], 
    x_max=eval_conf["x_max"], 
    y_min=eval_conf["y_min"], 
    y_max=eval_conf["y_max"], 
    z_min=eval_conf["z_min"], 
    z_max=eval_conf["z_max"], 
    increment=eval_conf["calc_grid_res_meters"]
    )
result = np.zeros(
    [len(frequency_bands),
     frame_amount,
     g.nxsteps,
     g.nysteps,
     g.nzsteps]
     )

###############################################
# start calculation
time_initial = time.time()

# open .h5 file to keep in RAM
with h5py.File(path_audio_data, "r") as h5_file:
    audio_data = h5_file[""]

for index_freq_band, currentFreqBand in enumerate(frequency_bands):
    for index_frame in range(0, frame_amount):
        time_calc = time.time()

        result[index_freq_band, index_frame] = calc_audio_frame(
            currentFreqBand, 
            index_frame, 
            index_freq_band, 
            bandwith, 
            start,
            stop,
            sample_freq,
            frame_rate,
            frame_length,
            path_audio_data,
            g,
            m
            )
        
time_total = np.round(time.time()-time_initial, 2)

print("##############################################")
print(f"Total calculation time: {np.round(time_total/60 , 2)} minutes")
print("##############################################")
#########################################

# save Data
np.save(path_result_file, result)
print(f"Saved NumPy result to {path_result_file}")

pf.io.write(path_result_file, 
           start = start, 
           stop = stop, 
           framerate = frame_rate, 
           frames = frame_amount, 
           frequency_bands = frequency_bands, 
           bandwith = bandwith,
           resolution = resolution,
           name = path_audio_data)
print(f"Saved PyFar result to {path_result_file}")

#####################################

# read Data

result = np.load(path_result_file + ".npy")
start, stop, framerate, frames, frequency_bands, bandwith, resolution, name = pf.io.read(path_result_file+".far")
result_Lp = ac.L_p(result)        # convert results in sound pressure Level