def rescale_for_arm(points: list[tuple[bool, int, int]]) -> list[tuple[bool, int, int]]:
    """
    Shift all grid points by -7 in X and +5 in Y to align with the robot arm's workspace.
    """
    return [(draw, x - 7, y + 5) for (draw, x, y) in points]


def auto_close_shape(points: list[tuple[bool, int, int]]) -> list[tuple[bool, int, int]]:
    """
    Automatically closes the shape by connecting the last drawn point to the first, if needed.
    """
    if not points:
        return points
    drawn = [p for p in points if p[0]]
    if len(drawn) < 2:
        return points
    first = drawn[0][1:]
    last = drawn[-1][1:]
    if last != first:
        points.append((True, *first))
    return points
