import os
from evaluation_config import eval_config
from efficient_evaluation import efficient_eval



path_audio_data = eval_config["in_folder"] + "array_audio_data/"

print(path_audio_data)
h5_files_list = os.listdir(path_audio_data)

for file_name in h5_files_list[2:5]:
    out_folder_name = f"result_{eval_config["framereate_fps"]}_{file_name}"
    efficient_eval(file_name, out_folder_name, eval_config)