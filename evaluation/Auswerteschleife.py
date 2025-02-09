'''
This script is based on the jupyter notebook Auswerteschleife.ipynb from 09.02.2025. 
'''

# Import libraries
import os
import acoular as ac
import numpy as np
import pyfar as pf
import time

from evaluation_config import eval_conf

###############################################
print(os.getcwd())

initialTime = time.time()

# initial definitions

resFileName = "./evaluation/" + eval_conf["out_folder"] + "2025-01-28_15-59-01_400437_eval_test2"

# define microphone geometry
micgeofile = "./evaluation/"+  eval_conf["in_folder"] + "array_position_data/bassoon_cage_64_optimized.xml"
m = ac.MicGeom(from_file=micgeofile)

# define calculation grid
resolution = 0.05

g = ac.RectGrid3D(x_min=eval_conf["x_min"], x_max=eval_conf["x_max"], y_min=eval_conf["y_min"], y_max=eval_conf["y_max"], z_min=eval_conf["z_min"], z_max=eval_conf["z_max"], increment=eval_conf["calc_grid_res_meters"])

# define audio data
name = "./evaluation/" + eval_conf["in_folder"] + "array_audio_data/2025-01-28_15-59-01_400437.h5"
data = ac.MaskedTimeSamples(name = name)

# define time related variables
start = 0#83#26        # in s
stop = 105#35#92#36
framerate = eval_conf["framereate_fps"]         # in f/s

# define freqency resolution
bandwith = eval_conf["bandwidth"]            #
frequency_bands = eval_conf["frequency_bands"] #

#---------------------------------------------------------------------------------------------------------------
# calculation of fixed values

frameLength = 1/framerate

print('init time: ' + str(time.time()-initialTime) + ' s')

result = np.zeros(
    [len(frequency_bands),
     int((stop-start)*framerate),
     g.nxsteps,
     g.nysteps,
     g.nzsteps]
     )

# begin evaluation loop

for i, currentFreqBand in enumerate(frequency_bands):

    for frame in range(0, int((stop-start)*framerate)):
        calcTime = time.time()

        print('Frame ' + str(frame+1)+' of '+str(int((stop-start)*framerate)))
        print('Frequency Band: ' + str(i+1) + ' (' + str(currentFreqBand) + ' Hz)')
        print('Frame length: ' + str((start+(frameLength*(frame+1)))-(start+(frameLength*frame))) + ' s ')
        

        # data = ac.MaskedTimeSamples(name = name)
        data = ac.MaskedTimeSamples(name = name, start = (start+(frameLength*frame))*data.sample_freq, stop = (start+(frameLength*(frame+1)))*data.sample_freq)
        # print('length of cropped measurement: ' + str(data.numsamples/data.sample_freq) + ' s (' + str(data.numsamples) + ' samples)')

        f = ac.PowerSpectra(
            source=data, 
            window='Hanning', 
            overlap=eval_conf["fft_overlap"], 
            block_size=eval_conf["fft_block_size"]
            )
        st = ac.SteeringVector(grid=g, mics=m, steer_type='true location')
        b = ac.BeamformerCleansc(freq_data=f, steer=st)

        result[i,frame] = b.synthetic(currentFreqBand, bandwith)

        print('Calculation time:', np.round(time.time()-calcTime, 2), "seconds")
        print("")

totalCalcTime = np.round(time.time()-initialTime, 2)

print("##############################################")
print(f"Total calculation time: {np.round(totalCalcTime/60 , 2)} minutes")
print("##############################################")
#########################################

# save Data
np.save(resFileName, result)
print(f"Saved NumPy result to {resFileName}")

pf.io.write(resFileName, 
           start = start, 
           stop = stop, 
           framerate = framerate, 
           frames = int((stop-start)*framerate), 
           frequency_bands = frequency_bands, 
           bandwith = bandwith,
           resolution = resolution,
           name = name)
print(f"Saved PyFar result to {resFileName}")

#####################################

# read Data

result = np.load(resFileName + ".npy")
start, stop, framerate, frames, frequency_bands, bandwith, resolution, name = pf.io.read(resFileName+".far")
result_Lp = ac.L_p(result)        # convert results in sound pressure Level
