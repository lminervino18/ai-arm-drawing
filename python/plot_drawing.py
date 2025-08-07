import matplotlib.pyplot as plt

GRID_WIDTH = 14
GRID_HEIGHT = 10

def plot_drawing(absolute_points):
    strokes = []
    current_stroke = []
    current_pos = (0, 0)

    for draw, x, y in absolute_points:
        if draw:
            current_stroke.append(current_pos)
            current_stroke.append((x, y))
        else:
            if current_stroke:
                strokes.append(current_stroke)
                current_stroke = []
        current_pos = (x, y)

    if current_stroke:
        strokes.append(current_stroke)

    # Draw grid
    fig, ax = plt.subplots(figsize=(7, 5))
    ax.set_xlim(0, GRID_WIDTH)
    ax.set_ylim(0, GRID_HEIGHT)
    ax.set_xticks(range(GRID_WIDTH + 1))
    ax.set_yticks(range(GRID_HEIGHT + 1))
    ax.grid(True)
    ax.set_aspect('equal')
    ax.set_title("Robotic Arm Drawing Simulation")

    # Draw strokes
    for stroke in strokes:
        if len(stroke) > 1:
            xs, ys = zip(*stroke)
            ax.plot(xs, ys, color='black')
        elif len(stroke) == 1:
            ax.plot(*stroke[0], marker='o', color='black')

    # Optional: show starting point
    ax.plot(0, 0, marker='o', color='red', label='Start')
    ax.legend()
    plt.show()

if __name__ == "__main__":
    absolute_points = [
        (0, 2, 1),
        (1, 6, 1),
        (1, 6, 7),
        (0, 4, 6),
        (1, 0, 6),
        (1, 0, 0),
        (0, 1, 2),
        (1, 3, 2),
        (1, 3, 4),
        (0, 2, 2),
        (1, 0, 2)
    ]

    plot_drawing(absolute_points)
