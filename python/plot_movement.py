import math
import matplotlib.pyplot as plt
from servo_math import compute_kinematics

plt.ion()

L0 = 1.3
L1 = 4.0

def reconstruct_joints(theta1, theta2):
    # Base positions
    left_base = (-L0, 0)
    right_base = (L0, 0)

    # Joint positions
    joint1 = (-L0 + L1 * math.cos(theta1), L1 * math.sin(theta1))
    joint2 = ( L0 + L1 * math.cos(theta2), L1 * math.sin(theta2))

    # End effector (from compute_kinematics)
    ef_x, ef_y = compute_kinematics((theta1, theta2))

    return left_base, joint1, (ef_x, ef_y), joint2, right_base

def plot_frame(left_base, joint1, ef, joint2, right_base, draw_line):
    plt.cla()
    plt.plot([left_base[0], joint1[0], ef[0]],
             [left_base[1], joint1[1], ef[1]], 'bo-', label="Left Arm")
    plt.plot([right_base[0], joint2[0], ef[0]],
             [right_base[1], joint2[1], ef[1]], 'go-', label="Right Arm")
    plt.plot(ef[0], ef[1], 'ro', label="End Effector")

    if draw_line:
        plot_frame.path.append(ef)
    if len(plot_frame.path) > 1:
        xs, ys = zip(*plot_frame.path)
        plt.plot(xs, ys, 'r-', label="Drawn Path")

    plt.title("Robot Arm Movement")
    plt.axis('equal')
    plt.xlim(-3.5, 3.5)
    plt.ylim(0, 5.5)
    plt.legend(loc="upper right")
    plt.pause(0.03)

plot_frame.path = []

def visualize_movement(draw_flags, angles):
    final_ef_positions = []
    try:
        plot_frame.path = []
        print("\nDEBUG: Starting movement visualization...")

        for i, (draw, (t1_deg, t2_deg, _)) in enumerate(zip(draw_flags, angles), 1):
            theta1 = math.radians(t1_deg)
            theta2 = math.radians(t2_deg)

            left_base, joint1, ef, joint2, right_base = reconstruct_joints(theta1, theta2)
            plot_frame(left_base, joint1, ef, joint2, right_base, draw)

            if draw:
                final_ef_positions.append(ef)

            print(f"Step {i}: Draw={draw}, Target cm=({ef[0]:.2f}, {ef[1]:.2f})")

        # Final static image
        plt.cla()
        if len(plot_frame.path) > 1:
            xs, ys = zip(*plot_frame.path)
            plt.plot(xs, ys, 'r-', label="Final Drawing")
        plt.title("Final Drawing")
        plt.axis('equal')
        plt.xlim(-3.5, 3.5)
        plt.ylim(0, 5.5)
        plt.legend()
        plt.pause(5)

        print("\n📍 Final end-effector positions where drawing occurred:")
        for i, (x, y) in enumerate(final_ef_positions, 1):
            print(f"{i}: ({x:.2f}, {y:.2f})")

        input("⏹️ Press Enter to close the window...")
        plt.ioff()
        plt.close('all')

    except KeyboardInterrupt:
        print("\n⏹️ Animation stopped by user.")
        plt.ioff()
        plt.close('all')
