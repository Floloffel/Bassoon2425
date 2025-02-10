# needs to beat 0.53 minutes @ 0.5 fps
# new time: 0.43 minutes at 0.5 fps

# new highsocre: 3.94 min @ 1fps

'''
This script is based on the jupyter notebook Auswerteschleife.ipynb from 09.02.2025. 
'''

# Import libraries
import os
import acoular as ac
import numpy as np
import json
import time
import gc
gc.collect() 

from evaluation_config import eval_conf
from _calc_single_audio_frame2 import calc_audio_frame

ac.config.global_caching = "all"

# define names
name_h5_file = "2025-01-28_15-59-01_400437"
out_folder_name = "testing"

# define paths
path_audio_data = eval_conf["in_folder"] + "array_audio_data/" + name_h5_file + ".h5"
path_mic_geom = eval_conf["in_folder"] + "array_position_data/bassoon_cage_64_optimized.xml"
path_result_files = eval_conf["out_folder"] + out_folder_name + "/"

# define parameters
resolution = eval_conf["calc_grid_res_meters"]
start = 0 #seconds
stop = 105 
bandwith = eval_conf["bandwidth"]
frequency_bands = eval_conf["frequency_bands"]
sample_freq = ac.MaskedTimeSamples(name = path_audio_data).sample_freq

frame_rate = eval_conf["framereate_fps"]
frame_length_seconds = 1/frame_rate
frame_length_samples = int(frame_length_seconds * sample_freq)
frame_amount = int((stop-start)*frame_rate)

if frame_length_samples < eval_conf["fft_block_size"]:
    raise ValueError(f"frame_length shorter than fft block ({frame_length_samples} < {eval_conf["fft_block_size"]})")

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
result = np.empty(
    [len(frequency_bands),
     frame_amount,
     g.nxsteps,
     g.nysteps,
     g.nzsteps], 
     dtype=float
     )

###############################################
# start calculation
time_initial = time.time()

for index_frame in range(0, frame_amount):
    data = ac.MaskedTimeSamples(
        name = path_audio_data, 
        start = start + frame_length_samples * index_frame,
        stop = start + frame_length_samples * (index_frame+1)
    )

    for index_freq_band, currentFreqBand in enumerate(frequency_bands):
        result[index_freq_band, index_frame] = calc_audio_frame(
            currentFreqBand, 
            index_frame, 
            index_freq_band, 
            bandwith, 
            start,
            stop,
            frame_rate,
            frame_length_seconds,
            g,
            m,
            data
            )
    
    #garbage collection every 20 frames to free up computing power
    if index_frame % 20 == 0:    
        gc.collect() 

        
time_total = np.round(time.time()-time_initial, 2)

print("##############################################")
print(f"Total calculation time: {np.round(time_total/60 , 2)} minutes")
print("##############################################")
#########################################

# save Data
os.makedirs(path_result_files, exist_ok=True)
np.save(path_result_files + "result_" + name_h5_file, result)

# save config
with open(path_result_files + "evaluation_config.json", "w") as outfile:
    json.dump(eval_conf, outfile, indent=4)


print(f"Saved results to {path_result_files}")
#####################################
