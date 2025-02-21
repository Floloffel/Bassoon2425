import os
import json
from _video_func import video_export
import logging
from datetime import datetime
import time
import numpy as np

# define files to craete videos from
npy_paths = [
    #'./evaluation/out/beamforming_results_25_02_16/2025-01-28_14-18-42_192339/result_2025-01-28_14-18-42_192339.npy', #chromatic scale octave 1.1
    #'./evaluation/out/beamforming_results_25_02_16/2025-01-28_14-46-10_658617/result_2025-01-28_14-46-10_658617.npy', #chromatic scale octave 1.2
    #'./evaluation/out/beamforming_results_25_02_16/2025-01-28_14-49-22_442633/result_2025-01-28_14-49-22_442633.npy', #chromatic scale octave 2
    #'./evaluation/out/beamforming_results_25_02_16/2025-01-28_14-52-30_189465/result_2025-01-28_14-52-30_189465.npy', #chromatic scale octave 3.1
    #'./evaluation/out/beamforming_results_25_02_16/2025-01-28_14-57-26_453699/result_2025-01-28_14-57-26_453699.npy', #chromatic scale octave 3.2
    #'./evaluation/out/beamforming_results_25_02_16/2025-01-28_15-01-02_954236/result_2025-01-28_15-01-02_954236.npy', #chromatic scale octave 4
    #'./evaluation/out/beamforming_results_25_02_16/2025-01-28_15-11-46_550615/result_2025-01-28_15-11-46_550615.npy', #melody 1
    #'./evaluation/out/beamforming_results_25_02_16/2025-01-28_15-26-45_296613/result_2025-01-28_15-26-45_296613.npy', #long tones 1
    #'./evaluation/out/beamforming_results_25_02_16/2025-01-28_15-36-18_896862/result_2025-01-28_15-36-18_896862.npy', #long tones 2
    './evaluation/out/beamforming_results_25_02_16/2025-01-28_15-59-01_400437/result_2025-01-28_15-59-01_400437.npy', #long tones 3
    #'./evaluation/out/beamforming_results_25_02_19/2024-08-08_16-59-56_816742/result_2024-08-08_16-59-56_816742.npy', #reference speaker
    #'./evaluation/out/beamforming_results_25_02_19/2025-01-28_15-18-43_492418/result_2025-01-28_15-18-43_492418.npy', #melody 2
    #'./evaluation/out/beamforming_results_25_02_20/2025-01-28_15-59-01_400437/result_2025-01-28_15-59-01_400437.npy'  #long tones 3 2cmgrid
    ]


# Setup logging
logging_folder = "evaluation\\out\\video_data\\logging"
os.makedirs(logging_folder, exist_ok=True)

date_str = datetime.now().strftime("%y_%m_%d")
logging.basicConfig(
    filename=f'{logging_folder}/video_wrapper_{date_str}.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

time_start = time.time()
logging.info("Script started")



npy_paths = [path.replace("/", os.path.sep) for path in npy_paths]
for path in npy_paths:
    time_per_video = time.time()

    # load json config file
    path_dir = os.path.dirname(path)
    config_path = path_dir + "/evaluation_config.json"
    
    with open(config_path, "r") as file:
        json_config =json.load(file)


    # get variables for out folder name
    grid_size_cm = str(int(json_config["calc_grid_res_meters"] * 100))
    name = path.split(".")[-2]
    name = name.split(os.path.sep)[-1]
    name = name.replace("result_", "")
    json_config["video_out"] = os.path.join(
        "evaluation", "out", "video_data", f"{grid_size_cm}cm_grid", name, "")

    logging.info(f"Processing file: {name}.npy @ {grid_size_cm} cm grid")
    
    # create out folder
    os.makedirs(json_config["video_out"], exist_ok=True)

    frequency_bands = json_config["frequency_bands"]
    camera_postions = [1, 2]

    for band in frequency_bands:
        for camera_pos in camera_postions:
            logging.info(f"Processing {band} Hz octave, camera position {camera_pos}")
            print(f"Processing {name} @ {grid_size_cm} cm grid, {band} Hz, camera {camera_pos}")
            video_export(path, name, json_config, band, camera_pos)
    
    logging.info(f"Done processing file. Time needed: {np.round((time.time() - time_per_video)/60, 2)} minutes")
    logging.info(f"saved videos to {json_config["video_out"]}")
    print("---------------------------------------------")

logging.info(f"Done processing all files. Total time needed: {np.round((time.time() - time_start)/60, 2)} minutes")