import numpy as np

CELL_SIZE = 0.5 # cm per cell

X_SERVO_2 = 10
Y_SERVO_2 = 5

X_SERVO_1 = 5
Y_SERVO_1 = 5

# Parameters [cm]
left_upper_arm = 6.0 # L1
left_lower_arm = 6.0 # R1
right_upper_arm = 6.0 # L2
right_lower_arm = 6.0 # R2

# Servo positions
servo_positions = np.array([[X_SERVO_1, Y_SERVO_1], [X_SERVO_2, Y_SERVO_2]])

# Arm lengths
arm_lengths = np.array([[left_upper_arm, left_lower_arm], [right_upper_arm, right_lower_arm]])

def compute_inverse_kinematics(x, y):
    """
    Calculate the angles for the two arms to reach the point (x, y) using vectorized operations.
    """

    # Deltas and distances
    deltas = np.array([x, y]) - servo_positions
    distances = np.linalg.norm(deltas, axis=1)

    # Angles using cosine law and arctangent
    phis = np.arccos((arm_lengths[:, 0]**2 + distances**2 - arm_lengths[:, 1]**2) / (2 * arm_lengths[:, 0] * distances))

    betas = np.arctan2(deltas[:, 1], deltas[:, 0])

    # Compute final angles
    theta_1 = betas[0] - phis[0]
    theta_2 = betas[1] + phis[1]

    return theta_1, theta_2


def process_absolute_points(points):
    """
    Convert absolute points to angles and pen positions for the robot arm.
    """
    result = []

    for dibujar, x_cell, y_cell in points:
        x = x_cell * CELL_SIZE
        y = y_cell * CELL_SIZE

        theta1, theta2 = compute_inverse_kinematics(x, y)
        pen = 30 if dibujar else 90 # See if 30 or 90 is ok

        result.append((round(theta1), round(theta2), pen))

    return result

if __name__ == "__main__":
    """
    Main function to test the inverse kinematics calculations.
    """
    points = [
        (True, 0, 0),   # Draw at (0, 0)
        (False, 1, 1), # Move to (0.5, 0.5) without drawing
        (True, 2, 2),  # Draw at (1.0, 1.0)
        (False, 3, 3)  # Move to (1.5, 1.5) without drawing
    ]

    result = process_absolute_points(points)
    for angles in result:
        print(f"Angles: {angles[0]}, {angles[1]}, Pen position: {angles[2]}")