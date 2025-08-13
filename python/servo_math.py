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


def brute_force_inverse_kinematics(
    target_xy: tuple[float, float],
    step_deg: float = 2.0,
    error_threshold: float = 0.01,
    enforce_order: bool = True,
    min_sep_deg: float = 0.0,
) -> tuple[tuple[float, float] | None, float]:
    """
    Multi-resolution brute-force IK search that enforces angle2 >= angle1 + min_sep_deg.
    Returns (best_angles_rad, min_error_sq) or (None, inf) if nothing under threshold.
    """
    def search(t1_lo: float, t1_hi: float, t2_lo: float, t2_hi: float, step: float):
        best_local = None
        min_err_local = float("inf")

        # Ensure ranges are valid
        t1_lo = max(0.0, t1_lo); t1_hi = min(180.0, t1_hi)
        t2_lo = max(0.0, t2_lo); t2_hi = min(180.0, t2_hi)

        for t1_deg in np.arange(t1_lo, t1_hi + 1e-9, step):
            # Enforce order constraint by starting t2 at t1 + min_sep if requested
            t2_start = max(t2_lo, t1_deg + (min_sep_deg if enforce_order else 0.0))
            for t2_deg in np.arange(t2_start, t2_hi + 1e-9, step):
                t1 = np.radians(t1_deg)
                t2 = np.radians(t2_deg)
                try:
                    xk, yk = compute_kinematics((t1, t2))
                except Exception:
                    continue
                err = (xk - target_xy[0])**2 + (yk - target_xy[1])**2
                if err < min_err_local:
                    min_err_local = err
                    best_local = (t1, t2)
                    if err <= error_threshold:
                        return best_local, min_err_local  # early accept
        return best_local, min_err_local

    # Coarse-to-fine steps (coarse first, then refine)
    steps: list[float] = []
    steps.append(max(step_deg, 0.5))  # coarse (>= 0.5°)
    if 0.5 not in steps:
        steps.append(0.5)
    if 0.25 not in steps:
        steps.append(0.25)
    if 0.1 not in steps:
        steps.append(0.1)

    best = None
    min_error = float("inf")

    # Pass 1: global coarse search
    b, e = search(0.0, 180.0, 0.0, 180.0, steps[0])
    if b is not None:
        best, min_error = b, e
        if min_error <= error_threshold:
            return best, min_error

    # Pass 2..n: refinements around the current best
    for s in steps[1:]:
        if best is None:
            # If no best yet, keep searching globally with finer step
            b, e = search(0.0, 180.0, 0.0, 180.0, s)
        else:
            c1, c2 = map(np.degrees, best)
            margin = max(4 * s, 2.0)  # refinement window in degrees
            b, e = search(
                c1 - margin, c1 + margin,
                c2 - margin, c2 + margin,
                s
            )
        if b is not None and e < min_error:
            best, min_error = b, e
            if min_error <= error_threshold:
                return best, min_error

    # Final acceptance only if under threshold
    if min_error <= error_threshold:
        return best, min_error
    return None, float("inf")


def process_absolute_points(points: list[tuple[bool, int, int]]) -> list[tuple[float, float, int]]:
    """
    Converts grid points into angle sequences for the servos using brute-force inverse kinematics only.
    Discards solutions with excessive error; prints stay exactly as in the original flow.
    """
    result = []
    cache: dict[tuple[int, int], tuple[float, float]] = {}

    for draw, x_cell, y_cell in points:
        key = (x_cell, y_cell)
        if key in cache:
            t1, t2 = cache[key]
        else:
            x = x_cell * CELL_SIZE
            y = y_cell * CELL_SIZE
            target = (x, y)

            # Enforce angle2 >= angle1 during the search; require good accuracy
            best_solution, error = brute_force_inverse_kinematics(
                target_xy=target,
                step_deg=2.0,            # coarse step to start
                error_threshold=0.01,    # accept only good fits
                enforce_order=True,      # enforce angle2 >= angle1
                min_sep_deg=0.0,         # you can set to >0 to keep a safety gap
            )

            if best_solution is None:
                print(f"❌ Point ({x_cell}, {y_cell}) unreachable or inaccurate (error² = {error:.6f}).")
                continue

            xk, yk = compute_kinematics(best_solution)
            print(f"✅ FK result: ({xk:.2f}, {yk:.2f})")
            print(f"🎯 Error²: {(xk - x) ** 2 + (yk - y) ** 2:.6f}")
            t1, t2 = np.degrees(best_solution)
            print(f"🦾 Angles: t1 = {t1:.2f}°, t2 = {t2:.2f}°")

            cache[key] = (t1, t2)

        pen = 125 if draw else 90
        result.append((round(t1, 1), round(t2, 1), pen))

    return result
