'''
This script provides a function to calc a single frame of audio data
'''
import acoular as ac
import numpy as np
import time
from evaluation_config import eval_conf


def calc_audio_frame(
      currentFreqBand, 
      index_frame, 
      index_FreqBand,
      bandwidth, 
      start, 
      stop,
      sample_freq, 
      framerate, 
      frameLength,
      name,
      ac_RectGrid3D,
      ac_MicGeom
      ):
    
    calcTime = time.time()

    print(f"Frame {index_frame+1} of {int((stop-start)*framerate)}")
    print(f"Frequency Band: {index_FreqBand + 1} ({currentFreqBand}) Hz)")
    print(f"Frame length: {(start + (frameLength*(index_frame+1))) - (start+(frameLength*index_frame))} seconds")

    data = ac.MaskedTimeSamples(
        name = name, 
        start = (start+(frameLength*index_frame))*sample_freq, 
        stop = (start+(frameLength*(index_frame+1)))*sample_freq)
    
    f = ac.PowerSpectra(
            source=data, 
            window='Hanning', 
            overlap=eval_conf["fft_overlap"], 
            block_size=eval_conf["fft_block_size"]
            )
    
    st = ac.SteeringVector(
        grid=ac_RectGrid3D, 
        mics=ac_MicGeom, 
        steer_type='true location')
    
    b = ac.BeamformerCleansc(
        freq_data=f, 
        steer=st)

    result_frame = b.synthetic(currentFreqBand, bandwidth)

    print('Calculation time:', np.round(time.time()-calcTime, 2), "seconds")
    print("")

    return result_frame