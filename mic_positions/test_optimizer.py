import numpy as np
from scipy.optimize import minimize

def calculate_mic_positions(params, initial_positions):
    """
    Calculate adjusted microphone positions based on the optimization parameters.

    Parameters:
        params: List of optimization parameters (offsets and tilts).
        initial_positions: Initial calculated microphone positions (Nx3 array).

    Returns:
        Adjusted microphone positions (Nx3 array).
    """
    # Extract parameters
    y_offset = params[0]  # y offset for B, C, D planes
    x_offsets = params[1:4]  # x offsets for B, C, D planes
    y_offsets = params[4:7]  # y offsets for B, C, D planes
    tilt_c_y, tilt_c_z = params[7:9]  # tilt of C plane in y and z
    tilt_b_y, tilt_d_y = params[9:11]  # tilt of B and D planes in y

    adjusted_positions = np.copy(initial_positions)

    # Apply offsets and tilts to each plane
    for i, mic in enumerate(adjusted_positions):
        if mic[2] == 1:  # Top plane (A) -> no adjustment
            continue
        elif mic[0] == 0:  # Left plane (B)
            mic[0] += x_offsets[0]
            mic[1] += y_offsets[0] + tilt_b_y * mic[2]
        elif mic[1] == 0:  # Back plane (C)
            mic[0] += x_offsets[1]
            mic[1] += y_offsets[1] + tilt_c_y * mic[2]
            mic[2] += tilt_c_z * mic[0]
        elif mic[0] == 1:  # Right plane (D)
            mic[0] += x_offsets[2]
            mic[1] += y_offsets[2] + tilt_d_y * mic[2]

    return adjusted_positions

def sum_squared_errors(params, initial_positions, measured_distances):
    """
    Compute the sum of squared errors between calculated and measured distances.

    Parameters:
        params: List of optimization parameters.
        initial_positions: Initial calculated microphone positions (Nx3 array).
        measured_distances: Matrix of measured distances (NxN array).

    Returns:
        Sum of squared errors.
    """
    adjusted_positions = calculate_mic_positions(params, initial_positions)
    num_mics = adjusted_positions.shape[0]

    total_error = 0.0
    for i in range(num_mics):
        for j in range(i + 1, num_mics):
            if measured_distances[i, j] > 0:  # Use only points with measured distance
                calculated_distance = np.linalg.norm(adjusted_positions[i] - adjusted_positions[j])
                error = (calculated_distance - measured_distances[i, j]) ** 2
                total_error += error

    return total_error

def optimize_mic_positions(initial_positions, measured_distances):
    """
    Optimize microphone positions to minimize sum of squared errors.

    Parameters:
        initial_positions: Initial calculated microphone positions (Nx3 array).
        measured_distances: Matrix of measured distances (NxN array).

    Returns:
        Optimized parameters and adjusted microphone positions.
    """
    # Initial guess for parameters (11 parameters to optimize)
    initial_params = np.zeros(11)

    # Bounds for optimization parameters (optional, can be adjusted as needed)
    bounds = [(-1, 1)] * 11

    # Optimize parameters
    result = minimize(
        sum_squared_errors,
        initial_params,
        args=(initial_positions, measured_distances),
        bounds=bounds,
        method='L-BFGS-B'
    )

    optimized_params = result.x
    adjusted_positions = calculate_mic_positions(optimized_params, initial_positions)
    mean_error = result.fun / np.count_nonzero(measured_distances)

    return optimized_params, adjusted_positions, mean_error

# Example usage
if __name__ == "__main__":
    # Example initial microphone positions (Nx3 array)
    initial_positions = np.array([
        [0, 0.5, 1],  # Top plane (A)
        [0, 0.5, 0],  # Left plane (B)
        [0.5, 0, 0],  # Back plane (C)
        [1, 0.5, 0]   # Right plane (D)
    ])

    # Example measured distances (NxN array, symmetric, 0 for unknown distances)
    measured_distances = np.array([
        [0, 1.0, 1.2, 1.0],
        [1.0, 0, 0.8, 1.5],
        [1.2, 0.8, 0, 1.1],
        [1.0, 1.5, 1.1, 0]
    ])

    # Run optimization
    optimized_params, adjusted_positions, mean_error = optimize_mic_positions(initial_positions, measured_distances)

    print("Optimized Parameters:", optimized_params)
    print("Adjusted Microphone Positions:\n", adjusted_positions)
    print("Mean Error:", mean_error)
