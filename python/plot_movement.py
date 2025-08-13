import math
import matplotlib.pyplot as plt

plt.ion()

L0 = 2.5
L1 = 6.0
L2 = 6.0
CELL_SIZE = 0.5

def compute_positions(theta1, theta2):
    p1 = (-L0 + L1 * math.cos(theta1), L1 * math.sin(theta1))
    p2 = ( L0 + L1 * math.cos(theta2), L1 * math.sin(theta2))
    ef_x = (p1[0] + p2[0]) / 2
    ef_y = (p1[1] + p2[1]) / 2
    return (-L0, 0), p1, (ef_x, ef_y), p2, (L0, 0)

def plot_frame(left_base, joint1, ef, joint2, right_base, draw_line):
    plt.cla()

    plt.plot([left_base[0], joint1[0], ef[0]],
             [left_base[1], joint1[1], ef[1]], 'bo-', label="Left Arm")
    plt.plot([right_base[0], joint2[0], ef[0]],
             [right_base[1], joint2[1], ef[1]], 'go-', label="Right Arm")
    plt.plot(ef[0], ef[1], 'ro', label="End Effector")

    if draw_line:
        plot_frame.path.append((ef[0], ef[1]))
    if len(plot_frame.path) > 1:
        x_vals, y_vals = zip(*plot_frame.path)
        plt.plot(x_vals, y_vals, 'r-', label="Drawn Path")

    plt.title("Robot Arm Movement")
    plt.axis('equal')
    plt.xlim(-15, 15)
    plt.ylim(-5, 15)
    plt.legend(loc="upper right")
    plt.pause(1.2)

plot_frame.path = []

def visualize_movement(points, angles):
    final_ef_positions = []
    try:
        plot_frame.path = []
        for (draw, x, y), (t1_deg, t2_deg, _) in zip(points, angles):
            theta1 = math.radians(t1_deg)
            theta2 = math.radians(t2_deg)
            left_base, joint1, ef, joint2, right_base = compute_positions(theta1, theta2)
            plot_frame(left_base, joint1, ef, joint2, right_base, draw)

            if draw:
                final_ef_positions.append(ef)

        # Show only the final red path
        plt.cla()
        if len(plot_frame.path) > 1:
            x_vals, y_vals = zip(*plot_frame.path)
            plt.plot(x_vals, y_vals, 'r-', label="Final Drawing")
        plt.title("Final Drawing")
        plt.axis('equal')
        plt.xlim(-15, 15)
        plt.ylim(-5, 15)
        plt.legend()
        plt.pause(5)

        print("\n📌 Expected draw positions (after rescaling):")
        for i, (draw, x, y) in enumerate(points):
            if draw:
                print(f"{i+1}: ({x * CELL_SIZE:.2f}, {y * CELL_SIZE:.2f})")

        print("\n📍 Final end-effector positions where drawing occurred:")
        for i, (x, y) in enumerate(final_ef_positions):
            print(f"{i+1}: ({x:.2f}, {y:.2f})")

        input("⏹️ Press Enter to close the window...")
        plt.ioff()
        plt.close('all')

    except KeyboardInterrupt:
        print("\n⏹️ Animation stopped by user.")
        plt.ioff()
        plt.close('all')
