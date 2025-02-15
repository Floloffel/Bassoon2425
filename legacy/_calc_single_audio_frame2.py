'''
This script provides a function to calc a single frame of audio data
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
      frameLength,
      ac_RectGrid3D,
      ac_MicGeom,
      ac_data,
      config
      ):
    
    calcTime = time.time()

    print(f"Frame {index_frame+1} of {int((stop-start)*config["frame_rate_fps"])}")
    print(f"Frequency Band: {index_FreqBand + 1} ({currentFreqBand} Hz)")
    print(f"Frame length: {int(frameLength * ac_data.sample_freq)} samples")

    
    # PowerSpectra, SteeringVector and BeamformerCleansc müssen nicht jeden frame ausgeführt werden.
    # im loop muss nur synthetic ausgeführt werden. die anderen nur ein mal vorher. das sollte schon viel schneller sein.


    f = ac.PowerSpectra(
            source=ac_data, 
            window='Hanning', 
            overlap=config["fft_overlap"], 
            block_size=config["fft_dynamic_block_sizes"][index_FreqBand] # ist index_FreqBand richtig? geht es nicht um Block size?
            )
    
    st = ac.SteeringVector(
        grid=ac_RectGrid3D, 
        mics=ac_MicGeom, 
        steer_type='true location')
    
    b = ac.BeamformerCleansc(
        freq_data=f, 
        steer=st)

    result_frame = b.synthetic(currentFreqBand, config["bandwidth"])

    print('Calculation time:', np.round(time.time()-calcTime, 2), "seconds")
    print("")

    return result_frame