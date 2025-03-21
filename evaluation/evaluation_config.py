'''
This is a config script for all evaluation scripts. It contains all relevant parameters that are shared among different evaluation files. All parameters are stored in a dictionary.
'''

out_folder = "./evaluation/out/"
in_folder = "./evaluation/in/"


calc_grid_res_meters = 0.05
frame_rate_fps = 25



#frequency_bands = [500, 1000]

# 3D evaluation area
x_min = 0
x_max = 1.2
y_min = 0
y_max = 1.2
z_min = 0
z_max = 1.75


#FFT parameters
fft_overlap = ["None", "50%", "75%", "87.5%"][0]
fft_block_size = [128, 256, 512, 2048, 4096][3]
fft_dynamic_block_sizes = [1024, 1024, 512, 256, 256]

frequency_bands = [125, 250, 500, 1000, 2000] # Array with mid frequencies of frequency bands
bandwidth = [1, 1/3][0]



######################################################
################# Dont change below ##################
######################################################

eval_config = {
    "out_folder": out_folder,
    "in_folder": in_folder,
    "calc_grid_res_meters": calc_grid_res_meters,
    "frame_rate_fps": frame_rate_fps,
    "bandwidth": bandwidth,
    "frequency_bands": frequency_bands,
    "x_min": x_min,
    "x_max": x_max,
    "y_min": y_min,
    "y_max": y_max, 
    "z_min": z_min,
    "z_max": z_max,
    "fft_overlap": fft_overlap, 
    "fft_block_size": fft_block_size,
    "fft_dynamic_block_sizes": fft_dynamic_block_sizes
}