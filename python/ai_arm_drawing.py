from ai_client import chat_with_ai
from servo_math import process_absolute_points
from serial_sender import send_angle_sequence
import os
import time

def validate_input(ai_response):
    invalid_keywords = ["answer", "sure", "let me", "here is", "drawing", "instructions", "this is"]
    instructions = []
    lines = ai_response.strip().splitlines()

    for idx, line in enumerate(lines):
        line_clean = line.strip().lower()
        if not line_clean:
            continue
        if any(bad_word in line_clean for bad_word in invalid_keywords):
            print(f"Invalid line {idx+1}: contains non-instructional text.")
            return False

        parts = line.strip().split()
        if len(parts) != 3:
            print(f"Error: Line {idx+1} must have exactly 3 elements.")
            return False
        try:
            draw_flag = int(parts[0])
            dx = int(parts[1])
            dy = int(parts[2])
        except ValueError:
            print(f"Error: Line {idx+1} contains non-integer values.")
            return False
        if draw_flag not in (0, 1):
            print(f"Error: Line {idx+1} draw_flag must be 0 or 1.")
            return False
        instructions.append((draw_flag, dx, dy))

    x = y = 0
    for idx, (draw_flag, dx, dy) in enumerate(instructions):
        x_new = x + dx
        y_new = y + dy
        if not (0 <= x_new < 14 and 0 <= y_new < 10):
            print(f"Error: Movement on line {idx+1} goes out of bounds ({x_new}, {y_new}).")
            return False
        x, y = x_new, y_new

    return instructions

def get_valid_response(prompt):
    retries = 0
    while True:
        try:
            response = chat_with_ai(prompt)
        except Exception as e:
            print(f"AI error: {e}")
            time.sleep(5)
            continue

        instructions = validate_input(response)
        if instructions is not False:
            return instructions
        else:
            retries += 1
            print(f"Retrying... attempt #{retries}")
            time.sleep(1)

def deltas_to_absolute(instructions):
    """
    Convert relative movement instructions to absolute grid coordinates.
    """
    absolute_points = []
    x = y = 0
    for draw_flag, dx, dy in instructions:
        x += dx
        y += dy
        absolute_points.append((draw_flag == 1, x, y))  # draw_flag as boolean
    return absolute_points

def main():
    instructions_prompt = (
        "You are a robotic arm that draws on a 14×10 grid (14 columns, 10 rows).\n"
        "Each cell is 0.5 cm, forming a 7 cm × 5 cm whiteboard.\n"
        "You always start at (0, 0), the bottom-left corner of the grid.\n"
        "\n"
        "Your job is to convert a prompt (e.g., 'draw a cat', 'write 3') into a list of movement instructions to draw that figure.\n"
        "\n"
        "⚠️ VERY IMPORTANT RULES:\n"
        "1. Your output must be ONLY movement instructions — no titles, explanations, or extra lines.\n"
        "2. Each instruction must follow this format (one per line):\n"
        "   <draw_flag> <delta_x> <delta_y>\n"
        "3. draw_flag: 1 = draw a straight line, 0 = move without drawing\n"
        "4. delta_x: horizontal movement (right = positive, left = negative)\n"
        "5. delta_y: vertical movement (up = positive, down = negative)\n"
        "\n"
        "✅ VALIDATION RULES:\n"
        "- Start from position (0, 0).\n"
        "- After each step, update your current position.\n"
        "- DO NOT let the new position go outside the grid: 0 <= x < 14 and 0 <= y < 10.\n"
        "- Track your position while generating instructions to ensure it always stays within bounds.\n"
        "- If any move would exceed the grid, CHANGE it to stay within the limits.\n"
        "\n"
        "✏️ Use many steps (20–40) to create symbolic but clear shapes.\n"
        "🎯 Center the figure within the grid as much as possible.\n"
        "📐 Use diagonal lines when needed. Only straight segments.\n"
        "\n"
        "Your response MUST be ONLY the raw list of instructions.\n"
        "Nothing else. No bullet points. No intro. No explanation.\n"
        "\n"
        "---\n"
        "\n"
        "Example input:\n"
        "\"draw a square\"\n"
        "Example output:\n"
        "0 3 1\n"
        "1 8 0\n"
        "1 0 8\n"
        "1 -8 0\n"
        "1 0 -8\n"
        "\n"
        "Now respond to this prompt: "
    )

    print("Type 'exit' to quit")
    while True:
        print("Prompt to draw with IA ARMY\n")
        user_input = input("> ")
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting chat...")
            break

        full_prompt = instructions_prompt + user_input
        instructions = get_valid_response(full_prompt)

        print("\n✅ Numeric matrix of instructions:")
        for instr in instructions:
            print(instr)

        absolute_points = deltas_to_absolute(instructions)
        angles = process_absolute_points(absolute_points)

        print("\n✅ Angles for the robotic arm:")
        for angle in angles:
            print(angle)

        print(f"\n✅ Reached {len(angles)}/{len(absolute_points)} points.")

        # Send to Arduino using external module
        send_angle_sequence(angles, port="/dev/ttyUSB0")  # Change port if needed

if __name__ == "__main__":
    main()
