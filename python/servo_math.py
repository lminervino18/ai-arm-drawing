import numpy as np

CELL_SIZE = 0.5  # cm per cell

X_SERVO_2 = 10
Y_SERVO_2 = 5

X_SERVO_1 = 5
Y_SERVO_1 = 5

# Arm segment lengths [cm]
left_upper_arm = 6.0  # L1
left_lower_arm = 6.0  # R1
right_upper_arm = 6.0  # L2
right_lower_arm = 6.0  # R2

# Servo positions
servo_positions = np.array([
    [X_SERVO_1, Y_SERVO_1],
    [X_SERVO_2, Y_SERVO_2]
])

# Arm lengths
arm_lengths = np.array([
    [left_upper_arm, left_lower_arm],
    [right_upper_arm, right_lower_arm]
])

def compute_inverse_kinematics(x, y):
    """
    Calculate the angles for the two arms to reach the point (x, y).
    Returns (None, None) if unreachable.
    """
    deltas = np.array([x, y]) - servo_positions
    distances = np.linalg.norm(deltas, axis=1)

    # Reject unreachable or too-close points
    for i, dist in enumerate(distances):
        l1, l2 = arm_lengths[i]
        if dist > (l1 + l2) or dist < abs(l1 - l2) or dist < 0.001:
            return None, None  # Out of range or too close

    # Angles using cosine law
    phis = np.arccos((arm_lengths[:, 0]**2 + distances**2 - arm_lengths[:, 1]**2) / (2 * arm_lengths[:, 0] * distances))
    betas = np.arctan2(deltas[:, 1], deltas[:, 0])

    theta_1 = betas[0] - phis[0]
    theta_2 = betas[1] + phis[1]

    return theta_1, theta_2

def process_absolute_points(points):
    """
    Convert absolute grid cell points to servo angles and pen positions.
    """
    result = []

    for draw, x_cell, y_cell in points:
        x = x_cell * CELL_SIZE
        y = y_cell * CELL_SIZE

        theta1, theta2 = compute_inverse_kinematics(x, y)
        if theta1 is None or theta2 is None:
            print(f"❌ Point ({x:.2f}, {y:.2f}) is unreachable.")
            continue

        pen = 30 if draw else 90
        result.append((round(theta1, 2), round(theta2, 2), pen))

    return result

if __name__ == "__main__":
    # Example test points
    points = [
        (True, 0, 0),
        (False, 1, 1),
        (True, 2, 2),
        (False, 3, 3)
    ]

    result = process_absolute_points(points)
    for angles in result:
        print(f"Angles: {angles[0]}°, {angles[1]}°, Pen: {angles[2]}")
