def beamform(
    data_file_wav: str,
    output_mp4: str,
    chunk_analysis_secs: float = 0.25,
    tmp_output_dir: str = "./tmp_output",
    block_size: int = 512,
    freq_range: tuple = (375, 3),
):
    if os.path.exists(tmp_output_dir):
        shutil.rmtree(tmp_output_dir)
    os.makedirs(tmp_output_dir)

    mic_geometry_file = os.path.join(
        os.path.split(acoular.__file__)[0], "xml", "minidsp_uma-16.xml"
    )
    mic_geom = acoular.MicGeom(from_file=mic_geometry_file)

    audio_data, sample_rate = sf.read(data_file_wav)

    # Custom colormap for visualization
    colors = ["navy", "blue", "cyan", "yellow", "red"]

    ny, nx, X, Y, grid = get_grid()
    steering_vector = acoular.SteeringVector(grid=grid, mics=mic_geom)
    samples_per_chunk = int(chunk_analysis_secs * sample_rate)
    num_chunks = audio_data.shape[0] // samples_per_chunk

    images = []
    for start_sample in range(0, audio_data.shape[0], samples_per_chunk):
        print(f"Doing {start_sample} / {num_chunks}")

        end_sample = min(start_sample + samples_per_chunk, audio_data.shape[0])
        data_ = audio_data[start_sample:end_sample, :]

        time_samples = acoular.TimeSamples(data=data_, sample_freq=sample_rate)
        power_spectra = acoular.PowerSpectra(
            time_data=time_samples, block_size=block_size, window="Hanning"
        )

        bb = acoular.BeamformerBase(freq_data=power_spectra, steer=steering_vector)
        pm = bb.synthetic(freq_range[0], freq_range[1])
        Lm = acoular.L_p(pm).reshape(ny, nx)

        # Plot the beamforming map
        fig, ax = plt.subplots(figsize=(20, 20))

        n_bins = 100
        for i in range(5):
            try:
                levels = np.linspace(Lm.min(), Lm.max(), n_bins)
                cmap = LinearSegmentedColormap.from_list("custom", colors, N=n_bins)
                cf = ax.contourf(X, Y, Lm, levels=levels, cmap=cmap)
            except Exception as e:
                print(f"Exception: {e} ... {i}")
                n_bins = int(n_bins * 0.9)

        plt.colorbar(cf, ax=ax, label="dB")
        images.append(os.path.join(tmp_output_dir, f"beamforming_{start_sample}.png"))
        fig.savefig(images[-1])
        plt.close()

    frame = cv2.imread(images[0])
    height, width, _ = frame.shape

    # Initialize video writer
    fourcc = cv2.VideoWriter_fourcc(*"mp4v")
    fps = int(1 / chunk_analysis_secs)
    video_writer = cv2.VideoWriter(output_mp4, fourcc, fps, (width, height))

    # Write each image to the video
    for image_path in images:
        print(image_path)
        frame = cv2.imread(image_path)
        video_writer.write(frame)

    video_writer.release()

    shutil.rmtree(tmp_output_dir)