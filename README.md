# Bassoon2425
Microphone array project WiSe 24/25. Topic: Sound Radiation of a Bassoon

This repository has two important folders: `mic_positions` and `evaluation`. \
**mic_positions** contains all files needed to plan, build, and verify the microphone array. \
**evaluation** contains all files needed to process the recorded array data.

## Workflow Mic Positions

1. **Vogel_plot.ipynb:** Determines the appropriate microphone number per plane.
2. **generate_ideal_mic_side_positions_as_excel.py:** Calculates and saves ideal 2D microphone positions.
3. **2d_to_3d_coords.ipynb:** Converts 2D positions to 3D positions.
4. **plot_and_measure_3d_coords.ipynb:** Plots ideal 3D positions. Also used for measuring distances between microphones.
5. **position_optimizer.ipynb:** Optimizes ideal microphone positions with measured microphone distances.
6. **calc_other_positions.ipynb:** Calculates positions like cameras, bassoon, and reference from real-world distance measurements.
7. **mic_calib_FileExport.ipynb:** Takes microphone calibration data and formats it for further use with Acoular.

## Workflow Evaluation Folder

There are 4 types of files:

* _[...] are custom functions.
* evaluation_[...] for calculating the beamforming results from raw array data.
* video_[...] for converting the beamforming result to a video (acoustic camera).
* SODIX_[...] for using the SODIX algorithm on raw array data.

### evaluation_[...] files

1. Copy array measurements to `evaluation\in\array_audio_data`.
2. Set up via **evaluation_config.py**.
3. **efficient_evaluation.py:** Calculates a single beamforming result at a given grid, fps, band, etc. Can be used for testing. \
   **evaluation_wrapper.py:** Calculates multiple beamforming results at a given grid, fps, band, etc. This can take a very long time (>10 hours).

### video_[...] files

1. Find optimal video parameters with **video_export.ipynb**: It shows a single frame of a video. Could also be used to export a single video.
2. **video_wrapper.py:** Creates multiple video files at once.

The video processing is about five times faster than the beamforming.

### SODIX_[...] files

**--Not finished--**\
The structure is the same as with the evaluation_[...] files.
The SODIX algorithm is used to describe the 3D directivity.

## Set Up Environment

All non-standard Python packages should be listed in `requirements.txt`. Install the required packages using `requirements.txt`:

```sh
pip install -r requirements.txt
conda install -c conda-forge ffmpeg
```

The ffmpeg writer installation was only successful via conda. Therefore, not using conda could lead to problems.