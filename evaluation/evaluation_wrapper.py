import acoular # needed to import before numpy to enable parallel processing with numba
import numpy as np
import time
import logging
from datetime import datetime
import os

from evaluation_config import eval_config
from efficient_evaluation import efficient_eval

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
stats = stats[0:11, :]


# Estimator for total time needed
total_time = []
for row in stats:
    time_s = float(row[3]) - float(row[2])
    total_time.append(time_s)

total_time = sum(total_time)
estimated_time_per_seconds = int(5*25)
estimate_time = np.round(total_time * estimated_time_per_seconds / 60 / 60, 2)
logging.info(f"Estimated needed time: {estimate_time} hours")
print(f"Estimated needed time with {estimated_time_per_seconds} seconds of calculation for 1 second of audio data:")
print(f"{estimate_time} hours")


# Main processing loop
start_time = time.time()
for i, row in enumerate(stats):
    file_name = row[0] + ".h5"
    out_folder_name = f"result_{eval_config['frame_rate_fps']}_{file_name}"
    logging.info(f"Processing file {file_name} ({i+1}/{len(stats)})")
    
    efficient_eval(file_name, (results_folder_name + "/" + file_name), eval_config, float(row[2]), float(row[3]))

    # Cool down period
    if i+1 < len(stats):
        time_cooldown = 60
        print(f"Taking a {time_cooldown}s break to cool down...")
        time.sleep(time_cooldown)

time_needed = np.round(time.time() - time_start, 2)
logging.info(f"Script completed. Total time needed: {time_needed/60} minutes.")
print(f"Calculated all files @ {eval_config['frame_rate_fps']} fps")
print(f"Needed time: {time_needed/60} minutes.")