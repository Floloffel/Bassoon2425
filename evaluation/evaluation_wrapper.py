import time
import numpy as np
from evaluation_config import eval_config
from efficient_evaluation import efficient_eval



time_start = time.time()

# load and trim stats
stats = np.load("./evaluation/in/audioFileStats.npy")
stats  = stats[0:11,:]

# estimator for total time needed
total_time = []
for row in stats:
    time_s = float(row[3]) - float(row[2])
    total_time.append(time_s)

total_time = sum(total_time)
estimated_time_per_seconds = 90
estimate_time = np.round(total_time * estimated_time_per_seconds / 60 / 60, 2)
print(f"Estimated need time with {estimated_time_per_seconds} seconds of calculation for 1 second of audio data:")
print(f"{estimate_time} hours")


for row in stats:
    file_name = row[0] + ".h5"
    out_folder_name = f"result_{eval_config["frame_rate_fps"]}_{file_name}"
    efficient_eval(file_name, out_folder_name, eval_config, float(row[2]), float(row[3]))


time_needed = np.round(time.time() - time_start, 2)

print(f"Calculated all files @ {eval_config["frame_rate_fps"]} fps")
print(f"Needed time: {time_needed/60} minutes.")