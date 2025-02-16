# Bassoon2425
Repo for Microphone array project WiSe 24/25. Topic: Sound Radiation of a Bassoon

This repository has two important folders: mic_positions and evaluation. \
**mic_positions** contains all files needed to plan, build and verify the microphone array.
**evaluation** contains all files needed to process the recorded array data.
There's also a **legacy** folder, which contains old scripts, that have no further use in the current workflow.

## Workflow Mic Positions

1. **Vogel_plot.ipynb:** determine appropriate microphone number per plane.
2. **generate_ideal_mic_side_positions_as_excel.py:** calculates and saves ideal 2D microphone positions.
3. **2d_to_3d_coords.ipynb:** converts 2D positions to 3D positions
4. **plot_and_measure_3d_coords.ipynb:** plots ideal 3D positions. Also used for measurin distances between microphones.
5. **position_optimizer.ipynb:** Optimizes ideal microphone positions with measured microphone distances.
6. **calc_other_positions.ipynb**: Calculates positions like cameras, bassoon, reference from real world distance measurements.

## Workflow evaluation

1. Copy array measurements to evaluation\in\array_audio_data
2. Set up via **evaluation_config.py**
3. **evaluation_config.py:** calculates beamforming results at given grid, fps, band, etc. This can take a very long time (>10 hours)
4. ???
