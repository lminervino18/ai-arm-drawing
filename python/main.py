import time
from ai_client import chat_with_ai
from servo_math import process_absolute_points
from serial_sender import send_angle_sequence
from plot_drawing import plot_drawing
from plot_movement import visualize_movement

from config import GRID_WIDTH, GRID_HEIGHT
from validation import validate_instruction_list
from rescale import rescale_for_arm, auto_close_shape
from prompt_engineer import build_initial_prompt, build_correction_prompt
from instruction_handler import get_valid_instruction_list


def handle_prompt(user_input: str):
    """
    Given a user text prompt, interact with the AI and return a validated and auto-closed list of drawing instructions.
    """
    initial_prompt = build_initial_prompt(user_input)
    return get_valid_instruction_list(initial_prompt, user_input)


def main():
    print("Type 'exit' to quit")
    while True:
        user_input = input("Draw prompt> ")
        if user_input.lower() in ["exit", "quit"]:
            break

        points = handle_prompt(user_input)
        #plot_drawing(points)
        points = rescale_for_arm(points)
        angles = process_absolute_points(points)
        visualize_movement(angles)
        send_angle_sequence(angles, port="COM3", baudrate=115200)

        time.sleep(1)
        #For remarking the drawing, we can mirror the angles
        mirrored_angles = list(reversed(angles))
        send_angle_sequence(mirrored_angles, port="COM3", baudrate=115200)



if __name__ == "__main__":
    main()
