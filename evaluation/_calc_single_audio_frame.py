'''
This scirpt provides a function to calc a single frame of audio data
'''
import acoular as ac
import numpy as np
import time


def calc_audio_frame(
      currentFreqBand, 
      index_frame, 
      index_FreqBand, 
      start, 
      stop, 
      framerate, 
      frameLength,
      name,
      ac_RectGrid3D,
      ac_MicGeom,
      bandwidth
      ):
    
    calcTime = time.time()

    print(f"Frame {index_frame+1} of {int((stop-start)*framerate)}")
    print(f"Frequency Band: {index_FreqBand + 1} ({currentFreqBand}) Hz)")
    print(f"Frame length: {(start + (frameLength*(index_frame+1))) - (start+(frameLength*index_frame))} seconds")

    data = ac.MaskedTimeSamples(name = name, start = (start+(frameLength*index_frame))*data.sample_freq, stop = (start+(frameLength*(index_frame+1)))*data.sample_freq)
    st = ac.SteeringVector(grid=ac_RectGrid3D, mics=ac_MicGeom, steer_type='true location')
    b = ac.BeamformerCleansc(freq_data=f, steer=st)

    result_frame = b.synthetic(currentFreqBand, bandwidth)

    print('Calculation time:', np.round(time.time()-calcTime, 2), "seconds")
    print("")

    return result_frame