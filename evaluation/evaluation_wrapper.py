import os
import time
import acoular
import numpy as np
from evaluation_config import eval_config
from efficient_evaluation import efficient_eval



path_audio_data = eval_config["in_folder"] + "array_audio_data/"
h5_files_list = os.listdir(path_audio_data)

start_list = [] # must be filled
stop_list = [] # must be filled

time_start = time.time()

for file_name, start, stop in zip(h5_files_list, start_list, stop_list):
    out_folder_name = f"result_{eval_config["frame_rate_fps"]}_{file_name}"
    try:
        efficient_eval(file_name, out_folder_name, eval_config)
        print("###############################################")
        print("###############################################")
        print(file_name, "finished")
        print("###############################################")
        print("###############################################")
    except:
        print("###############################################")
        print("###############################################")
        print(file_name, "not successfull")
        print("###############################################")
        print("###############################################")


time_needed = np.round(time.time() - time_start, 2)

print(f"Calculated all files @ {eval_config["frame_rate_fps"]} fps")
print(f"Needed time: {time_needed/60} minutes.")