'''
This script is based on the jupyter notebook Auswerteschleife.ipynb from 09.02.2025. 
'''

# import libraries
import os
import acoular as ac
import numpy as np
import json
import time
import gc

import cProfile
import pstats

from evaluation_config import eval_config
from _calc_single_audio_frame2 import calc_audio_frame

def efficient_eval(name_h5_file, out_folder_name, config, start_seconds, stop_seconds):

    gc.collect() 

    ac.config.global_caching = "all"
    #ac.config.cache_dir = "C:/Projekte TEMPORÄR/Bassoon2425 Cache"

    # define paths
    path_audio_data = config["in_folder"] + "array_audio_data/" + name_h5_file
    path_mic_geom = config["in_folder"] + "array_position_data/bassoon_cage_64_optimized.xml"
    path_result_files = config["out_folder"] + out_folder_name + "/"

    # define parameters

    frequency_bands = config["frequency_bands"]
    sample_freq = ac.MaskedTimeSamples(name = path_audio_data).sample_freq

    frame_rate = config["frame_rate_fps"]
    frame_length_seconds = 1/frame_rate
    frame_length_samples = int(frame_length_seconds * sample_freq)
    frame_amount = int((stop_seconds-start_seconds)*frame_rate)

    if frame_length_samples < config["fft_block_size"]:
        raise ValueError(f"frame_length shorter than fft block ({frame_length_samples} < {np.min(config["fft_dynamic_block_sizes"])})")

    # acoular set up

    m = ac.MicGeom(from_file=path_mic_geom)
    g = ac.RectGrid3D(
        x_min=config["x_min"], 
        x_max=config["x_max"], 
        y_min=config["y_min"], 
        y_max=config["y_max"], 
        z_min=config["z_min"], 
        z_max=config["z_max"], 
        increment=config["calc_grid_res_meters"]
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
        data = ac.MaskedTimeSamples( # das muss nicht jeden frame aufgerufen werden. es kann nach dem aufrufen einfach data.start und data.stop geändert werden.
            name = path_audio_data, 
            start = start_seconds + frame_length_samples * index_frame,
            stop = start_seconds + frame_length_samples * (index_frame+1)
        )

        for index_freq_band, currentFreqBand in enumerate(frequency_bands):
            result[index_freq_band, index_frame] = calc_audio_frame(
                currentFreqBand, 
                index_frame, 
                index_freq_band, 
                start_seconds,
                stop_seconds,
                frame_length_seconds,
                g,
                m,
                data,
                config
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
        json.dump(config, outfile, indent=4)


    print(f"Saved results to {path_result_files}")
    #####################################

def main():
    name_h5_file = "2025-01-28_15-59-01_400437.h5"
    out_folder_name = "testing"
    start_seconds = 26 #seconds
    stop_seconds = 36 
    efficient_eval(name_h5_file, out_folder_name, eval_config, start_seconds, stop_seconds)

if __name__ == "__main__":
    # run main with profiler to check for bottlenecks
    profiler = cProfile.Profile()
    profiler.enable()
    main()

    profiler.disable()
    stats = pstats.Stats(profiler).sort_stats("cumtime")
    #stats.print_stats()
    stats.dump_stats("./evaluation/out/testing/profile_results.prof")