import acoular as ac
import json
import os
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as anim
from matplotlib.colors import LinearSegmentedColormap


def video_export(path, name, config, frequency_band, camera_position):
    ######################
    # Set up
    ######################

    frequency_band_index = config["frequency_bands"].index(frequency_band)
    
    # don't be a fool, count like a computer
    camPos = int(camera_position - 1)

    # Camera Angles
    azimuth =  np.array([-133.33136452241695,164.2465834869733+15])[camPos]
    elevation = np.array([-27.020027669675454,64.11592446841624-10])[camPos]

    ax_xlim = [[1.4, 0.2], [1.4, 0.2]][camPos]
    ax_ylim = [[0, 1.4], [0, 1.4]][camPos]
    ax_zlim = [[0, 2], [0, 2]][camPos]

    # plot parameters
    dotsize = 10**-6
    size_exponent = 5
    vmin = 60 #dB
    vmax = 90 #dB
    alpha = 0.7
    init_frame = 42
    width_pixels = 1440
    height_pixels = 1920
    dpi = 80
    resolution = config['calc_grid_res_meters']

    colors = ["navy", "blue", "cyan", "yellow", "red", "darkred", "black"]
    custom_cmap = LinearSegmentedColormap.from_list("custom", colors, N=100)

    video_path = os.path.join(
        config["video_out"],
        f"{name}_{frequency_band}Hz_cam{camera_position}.mov"
        )
    
    ######################
    # Processing Data
    ######################

    # read Data
    bf_result = np.load(path)
    map = ac.fbeamform.L_p(bf_result) # p0 = 4 * 10**-4

  
    # get x, y, z values
    x_m, y_m, z_m = np.meshgrid(np.linspace(0,map.shape[2]*resolution,map.shape[2]),
                                np.linspace(0,map.shape[3]*resolution,map.shape[3]), 
                                np.linspace(0,map.shape[4]*resolution,map.shape[4]))
    
    # Filter the points above the threshold
    x_m_flat = x_m.flatten()
    y_m_flat = y_m.flatten()
    z_m_flat = z_m.flatten()
  
    map_flat = map[frequency_band_index, init_frame].flatten()
    above_threshold = map_flat > vmin
    x_m_thresh = x_m_flat[above_threshold]
    y_m_thresh = y_m_flat[above_threshold]
    z_m_thresh = z_m_flat[above_threshold]
    values_thresh = map_flat[above_threshold]


    ######################
    # Plotting
    ######################
    
    size = (values_thresh)**size_exponent * dotsize
    # Calculate figsize in inches (pixels / dpi)
    figsize = (width_pixels / dpi, height_pixels / dpi)

    # init figure
    fig = plt.figure(figsize = figsize, dpi=dpi)

    # camera perspective
    ax = fig.add_subplot(projection='3d')
    ax.set_proj_type('persp', focal_length=0.1)#0.547)
    ax.view_init(elev=elevation, azim=azimuth, roll=0)

    # plot Beamforming data
    scat = ax.scatter(x_m_thresh, y_m_thresh, z_m_thresh,
                      c=values_thresh,
                      cmap=custom_cmap,
                      alpha=alpha,
                      s=size,
                      vmin=vmin,
                      vmax = vmax)

    # correct grid
    ax.set_xlim(ax_xlim)
    ax.set_ylim(ax_ylim)
    ax.set_zlim(ax_zlim)
    ax.set_aspect('equal')

    # remove background and axis
    fig.patch.set_facecolor('none')
    ax.set_axis_off()
    ax.set_facecolor('none')


    # update function also works with global variables
    def update(frame):

        # Extract values for this specific frame
        values = map[frequency_band_index, frame, :, :, :].flatten()

        # Apply a threshold to filter the data
        mask = values > vmin  # Define a threshold for visibility
        filtered_values = values[mask]

        # Get the coordinates for these filtered values
        x_filtered = x_m.flatten()[mask]
        y_filtered = y_m.flatten()[mask]
        z_filtered = z_m.flatten()[mask]

        # Update color, size, alpha
        color = filtered_values  # Can apply normalization or scaling
        size = (filtered_values ** size_exponent) * dotsize  # Adjust size based on values

        # Update the scatter plot with new values
        scat._offsets3d = (x_filtered, y_filtered, z_filtered)  # Update the 3D coordinates
        scat.set_array(color)  # Update color
        scat.set_sizes(size)  # Update size

        return scat,

    ani = anim.FuncAnimation(fig=fig, func=update, frames=map.shape[1], interval=(1/config["frame_rate_fps"])*1000)

    #plt.show()

    writer = anim.FFMpegWriter(fps=config["frame_rate_fps"], codec='png', extra_args=[
        '-pix_fmt', 'yuva444p',  # Ensure transparency (RGBA)
        '-c:v', 'prores_ks',  # Use ProRes 4444 codec for alpha channel support
        '-profile:v', '4',  # ProRes 4444 profile (supports alpha)
        '-b:v', '10M'  # Increase bitrate for better quality
    ])
    ani.save(filename=video_path, writer=writer)

    plt.close()