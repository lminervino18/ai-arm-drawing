import numpy as np

CELL_SIZE = 0.5  # cm per cell

L0 = 2.5
L1 = 6.0
L2 = 6.0

def verify_reachability(distance):
    """
    Check if the point (x, y) is reachable by the robotic arms.
    """
    return distance <= (L1 + L2) and distance >= abs(L1 - L2)

def compute_inverse_kinematics(x, y):
    """
    Calculate the angles for the two arms to reach the point (x, y).
    Returns (None, None) if unreachable.
    """

    # The RS is in the middle of the 2 servos
    distance_1 = np.sqrt((L0 + x)**2 + y**2)
    distance_2 = np.sqrt((L0 - x)**2 + y**2)
    for distance in [distance_1, distance_2]:
        if not verify_reachability(distance):
            return []

    # Argument has to be between -1 and 1 to do arccos
    arg_1 = np.clip((L1**2 + ((L0 + x)**2 + y**2) - L2**2) / (2 * L1 * distance_1), -1, 1)
    arg_2 = np.clip((L1**2 + ((L0 - x)**2 + y**2) - L2**2) / (2 * L1 * distance_2), -1, 1)

    alpha_1 = np.arccos(arg_1)
    alpha_2 = np.arccos(arg_2)

    beta_1 = np.arctan2(y, L0 + x)
    beta_2 = np.arctan2(y, L0 - x)

    # We have 4 solutions (theta_1 and theta_2 can go from 0 to pi)
    theta_1 = [beta_1 - alpha_1, beta_1 + alpha_1]
    theta_2 = [np.pi - beta_2 + alpha_2, np.pi - beta_2 - alpha_2]

    solutions = []
    for t1 in theta_1:
        for t2 in theta_2:
            if 0 <= t1 <= np.pi and 0 <= t2 <= np.pi: # Check if the angles are in a valid range
                solutions.append((t1, t2))

    return solutions


def pick_solution(solutions, prev_angles):
    """
    Pick the best solution from the list of solutions based on the previous angles.
    """
    if not solutions:
        return None

    # If there's no previous angle, just return the first solution
    if prev_angles is None:
        return solutions[0]

    # Compute the distances from the previous angles, returns the minimum
    distances = np.linalg.norm(np.array(solutions) - np.array(prev_angles), axis=1)
    idx_min = np.argmin(distances)

    return solutions[idx_min]


def process_absolute_points(points):
    """
    Convert absolute grid cell points to servo angles and pen positions.
    """
    result = []
    prev_solution = None

    for draw, x_cell, y_cell in points:
        x = x_cell * CELL_SIZE
        y = y_cell * CELL_SIZE

        solutions = compute_inverse_kinematics(x, y)
        best_solution = pick_solution(solutions, prev_solution)
        if best_solution is None:
            print(f"Point ({x_cell}, {y_cell}) is unreachable.")
            continue

        pen = 30 if draw else 90 # Pen up/down angle
        result.append((round(np.degrees(best_solution[0]), 0), round(np.degrees(best_solution[1]), 0), pen))

        prev_solution = best_solution

    return result

if __name__ == "__main__":
    # Example test points
    points = [
        (True, 0, 5),
        (False, 1, 5),
        (True, 2, 10),
        (False, 3, 10)
    ]

    result = process_absolute_points(points)
    for angles in result:
        print(f"Angles: {angles[0]}°, {angles[1]}°, Pen: {angles[2]}")