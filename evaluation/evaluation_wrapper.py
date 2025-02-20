'''
This script runs the evaluation function on all measurements. 
Besides measurement data, a "stas" file with measurement name, start and stop is needed.
Running this script can take a very long time. Logging is implemented.
'''

import acoular # needed to import before numpy to enable parallel processing with numba
import numpy as np
import time
import logging
from datetime import datetime
import os

from evaluation_config import eval_config
from efficient_evaluation import efficient_eval


############################################
# change theese to select files to evaluate
stats_start_index = 0
stats_stop_index = 11
############################################

# set up variables
estimated_time_per_seconds = int(4*25)
time_cooldown = 60

# create out folder
results_folder_name = "beamforming_results"
os.makedirs((eval_config["out_folder"] + results_folder_name), exist_ok=True)

# Setup logging
date_str = datetime.now().strftime("%y_%m_%d")
logging.basicConfig(
    filename=f'{eval_config["out_folder"] + results_folder_name}/evaluation_{date_str}.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

time_start = time.time()
logging.info("Script started")

# Load and trim stats
stats = np.load("./evaluation/in/audioFileStats.npy")
stats = stats[stats_start_index:stats_stop_index, :]
print(stats)


# Estimator for total time needed
total_time = []
for row in stats:
    time_s = float(row[3]) - float(row[2])
    total_time.append(time_s)

total_time = sum(total_time)
estimate_time = np.round(total_time * estimated_time_per_seconds / 60 / 60, 2)
logging.info(f"Estimated needed time: {estimate_time} hours")
print(f"Estimated needed time with {estimated_time_per_seconds} seconds of calculation for 1 second of audio data:")
print(f"{estimate_time} hours")



# Main processing loop
start_time = time.time()
for i, row in enumerate(stats):
    file_name = row[0] + ".h5"
    out_folder_name = f"result_{eval_config['frame_rate_fps']}_{file_name}"
    
    # logging
    logging.info(f"Processing file {file_name} ({i+1}/{len(stats)})")
    file_length_seconds = float(row[3]) - float(row[2])
    logging.info(f"File length: {np.round(file_length_seconds, 2)} seconds")
    logging.info(f"Frame amount: {int(file_length_seconds * eval_config['frame_rate_fps'])}")
    

    efficient_eval(file_name, (results_folder_name + "/" + file_name), eval_config, float(row[2]), float(row[3]))


    # Cool down period
    if i+1 < len(stats):
        print(f"Taking a {time_cooldown}s break to cool down...")
        time.sleep(time_cooldown)


# logging
time_needed = np.round(time.time() - time_start, 2)
logging.info(f"Script completed. Total time needed: {np.round(time_needed/60/60, 2)} hours.")
print(f"Calculated all files @ {eval_config['frame_rate_fps']} fps")
print(f"Needed time: {time_needed/60} minutes.")