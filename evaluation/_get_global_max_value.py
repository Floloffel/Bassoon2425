import acoular as ac
import numpy as np

def find_global_max(npy_file_paths):
    local_maxes = []
    for path in npy_file_paths:
        # read Data
        result = np.load(path)
        map = ac.fbeamform.L_p(result) # p0 = 4 * 10**-10
        max_value = np.max(map)
        local_maxes.append(max_value)

    global_max_value = np.max(local_maxes)

    return float(global_max_value)