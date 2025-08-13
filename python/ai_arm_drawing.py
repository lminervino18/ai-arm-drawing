from ai_client import chat_with_ai
from servo_math import process_absolute_points, CELL_SIZE
from serial_sender import send_angle_sequence
from plot_drawing import plot_drawing
from plot_movement import visualize_movement
import time

GRID_WIDTH = 14
GRID_HEIGHT = 10

def rescale_for_arm(points):
    """
    Shift all grid points by -7 in X and +5 in Y to align with the robot arm's workspace.
    """
    return [(draw, x - 7, y + 5) for (draw, x, y) in points]


def validate_input(ai_response):
    instructions = []
    lines = ai_response.strip().splitlines()

    for idx, line in enumerate(lines):
        parts = line.strip().split()
        if len(parts) != 3:
            print(f"Error: Line {idx+1} must have 3 parts.")
            return False
        try:
            draw_flag = int(parts[0])
            x = int(parts[1])
            y = int(parts[2])
        except ValueError:
            print(f"Error: Line {idx+1} has non-integer values.")
            return False
        if draw_flag not in (0, 1):
            print(f"Error: Line {idx+1}, invalid draw_flag.")
            return False
        if not (0 <= x < GRID_WIDTH and 0 <= y < GRID_HEIGHT):
            print(f"Error: Line {idx+1} point ({x},{y}) out of bounds.")
            return False
        flag_bool = (draw_flag == 1)
        if flag_bool and instructions and instructions[-1] == (True, x, y):
            print(f"Error: Line {idx+1} duplicates previous draw point.")
            return False
        instructions.append((flag_bool, x, y))

    if not instructions:
        print("Error: No instructions found.")
        return False
    if instructions[0][0]:
        print("Error: First instruction must not draw from origin.")
        return False

    return instructions

def auto_close_shape(points):
    if not points:
        return points
    drawn = [p for p in points if p[0]]
    if len(drawn) < 2:
        return points
    first = drawn[0][1:]
    last = drawn[-1][1:]
    if last != first:
        points.append((True, *first))
        print(f"Auto-closing shape: added line from {last} to {first}")
    return points

def build_correction_prompt(previous_output, user_prompt):
    return (
        "You are a visual design assistant helping improve symbolic drawings made by a robotic arm on a 14×10 grid.\n"
        "The grid is composed of 14 columns and 10 rows (each cell is 0.5 cm), forming a 7×5 cm drawing surface.\n"
        "The robotic arm receives absolute-position drawing instructions in this format:\n"
        "<draw_flag> <x> <y>\n"
        "- draw_flag: 1 = draw a straight line from the current position to (x, y)\n"
        "- draw_flag: 0 = move without drawing (pen lifted)\n"
        "- x and y are grid coordinates (0 ≤ x < 14, 0 ≤ y < 10)\n"
        "- The robot always starts at (0, 0)\n\n"
        "The following instruction list was generated from the prompt:\n"
        f"\"{user_prompt}\"\n\n"
        "Your job is to refine this list to improve clarity, structure, and visual consistency.\n\n"
        "🧠 RULES FOR CORRECTION:\n"
        "- The first instruction must always be draw_flag = 0 (a movement from origin, not a drawing).\n"
        "- Respect the original intent of each draw_flag — do NOT convert movements (0) into drawing (1) unless clearly incorrect.\n"
        "- Only use draw_flag = 1 when a straight-line drawing is intentional and meaningful.\n"
        "- Use draw_flag = 0 to jump between disconnected elements — do not draw unnecessary connectors.\n"
        "- Avoid overlapping or redundant lines (e.g., repeating the same point or unnecessary backtracking).\n"
        "- Improve coherence, clarity, and symbolic integrity of the figure.\n"
        "- Close open shapes when it adds visual meaning, and center the drawing within the grid.\n\n"
        "📌 IMPORTANT:\n"
        "- All coordinates must be valid: 0 ≤ x < 14 and 0 ≤ y < 10.\n"
        "- Instructions must follow this format exactly: <draw_flag> <x> <y>\n"
        "- Do NOT include any explanation, titles, or extra content — only return the corrected list.\n\n"
        "Current instruction list:\n"
        f"{previous_output.strip()}\n\n"
        "✏️ Return the corrected list below:"
    )

def get_valid_instruction_list(prompt_text, user_prompt):
    retries = 0
    while True:
        try:
            ai_raw = chat_with_ai(prompt_text)
        except Exception as e:
            print(f"AI error: {e}")
            time.sleep(5)
            continue

        instr = validate_input(ai_raw)
        if instr:
            reviewed_prompt = build_correction_prompt(ai_raw, user_prompt)
            reviewed = chat_with_ai(reviewed_prompt)
            final_instr = validate_input(reviewed) or instr
            return auto_close_shape(final_instr)

        retries += 1
        print(f"Retrying generation... attempt {retries}")
        time.sleep(1)

def handle_prompt(user_input):
    prompt = (
        "You are a robotic arm drawing on a 14×10 grid (14 columns, 10 rows).\n"
        "Each cell is 0.5 cm, forming a 7 cm × 5 cm whiteboard.\n\n"
        "Your task is to convert a drawing prompt into a coherent set of movement instructions.\n"
        "Follow this 3-step process:\n\n"
        "1. PLAN: Decide the main points and shape layout before generating any instructions.\n"
        "2. GENERATE: Create a list of absolute instructions in this format:\n"
        "   <draw_flag> <x> <y>\n"
        "   Where draw_flag is 1 to draw a line or 0 to move without drawing.\n"
        "   Each point (x, y) must be within: 0 ≤ x < 14 and 0 ≤ y < 10.\n"
        "   ⚠️ The first instruction must always be draw_flag = 0 (move from origin).\n"
        "3. REVIEW AND FIX:\n"
        "   - Ensure all points are inside grid boundaries.\n"
        "   - The first instruction must be a movement (pen lifted) from (0, 0).\n"
        "   - Avoid broken strokes, unfinished figures, or abrupt endings.\n"
        "   - Avoid excessive jumping or unnecessary noise.\n\n"
        "Only output the final list of corrected instructions, with no explanations or commentary.\n\n"
        "---\n\n"
        f"Prompt: {user_input}"
    )

    return get_valid_instruction_list(prompt, user_input)


def main():
    print("Type 'exit' to quit")
    while True:
        user_input = input("Draw prompt> ")
        if user_input.lower() in ["exit", "quit"]:
            break

        points = handle_prompt(user_input)
        plot_drawing(points)
        points = rescale_for_arm(points)
        angles = process_absolute_points(points)
        draw_flags = [draw for draw, x, y in points]
        visualize_movement(draw_flags, angles)

        send_angle_sequence(angles, port="COM3", baudrate=115200)

if __name__ == "__main__":
    main()
