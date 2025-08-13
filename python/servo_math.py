import numpy as np

CELL_SIZE = 0.5  # cm per cell

# Arm segment lengths (in cm)
L0 = 1.3
L1 = 4.0
L2 = 5.0


def compute_kinematics(angles: tuple[float, float]) -> tuple[float, float]:
    """
    Computes the (x, y) position from joint angles (theta1, theta2).
    """
    theta1, theta2 = angles

    m = 2 * L0 + L2 * (np.cos(theta2) - np.cos(theta1))
    n = L1 * np.abs(np.sin(theta1) - np.sin(theta2))

    phi1 = np.arccos(np.clip(np.sqrt(m**2 + n**2) / (2 * L2), -1, 1))
    phi2 = np.arctan2(n, m)

    alpha1 = phi1 + phi2
    alpha2 = np.pi - phi1 + phi2

    x1 = -L0 + L1 * np.cos(theta1) + L2 * np.cos(alpha1)
    y1 =      L1 * np.sin(theta1) + L2 * np.sin(alpha1)

    x2 =  L0 + L1 * np.cos(theta2) + L2 * np.cos(alpha2)
    y2 =      L1 * np.sin(theta2) + L2 * np.sin(alpha2)

    return ((x1 + x2) / 2, (y1 + y2) / 2)


def brute_force_inverse_kinematics(target_xy: tuple[float, float], step_deg=0.5, error_threshold=1e-6):
    """
    Searches the joint space for a valid solution using brute force.
    """
    best = None
    min_error = float("inf")

    for t1_deg in np.arange(0, 180 + step_deg, step_deg):
        for t2_deg in np.arange(0, 180 + step_deg, step_deg):
            t1 = np.radians(t1_deg)
            t2 = np.radians(t2_deg)
            try:
                xk, yk = compute_kinematics((t1, t2))
                err = (xk - target_xy[0])**2 + (yk - target_xy[1])**2
                if err < min_error:
                    min_error = err
                    best = (t1, t2)
                    if err <= error_threshold:
                        return best, min_error
            except:
                continue

    return best, min_error


def process_absolute_points(points: list[tuple[bool, int, int]]) -> list[tuple[float, float, int]]:
    """
    Converts grid points into angle sequences for the servos using brute-force inverse kinematics only.
    """
    result = []
    cache = {}

    for draw, x_cell, y_cell in points:
        key = (x_cell, y_cell)
        if key in cache:
            t1, t2 = cache[key]
        else:
            x = x_cell * CELL_SIZE
            y = y_cell * CELL_SIZE
            target = (x, y)

            best_solution, error = brute_force_inverse_kinematics(target)

            if best_solution is None:
                print(f"❌ Point ({x_cell}, {y_cell}) unreachable via brute force.")
                continue

            xk, yk = compute_kinematics(best_solution)
            print(f"✅ FK result: ({xk:.2f}, {yk:.2f})")
            print(f"🎯 Error²: {(xk - x)**2 + (yk - y)**2:.6f}")
            t1, t2 = np.degrees(best_solution)
            print(f"🦾 Angles: t1 = {t1:.2f}°, t2 = {t2:.2f}°")

            cache[key] = (t1, t2)

        pen = 125 if draw else 90
        result.append((round(t1, 1), round(t2, 1), pen))

    return result
