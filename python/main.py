from ai_client import chat_with_ai
import os

def validate_input(ai_response):
    # Parse response into instructions
    instructions = []
    lines = ai_response.strip().splitlines()
    for idx, line in enumerate(lines):
        parts = line.strip().split()
        if len(parts) != 3:
            print(f"Error: Line {idx+1} does not have exactly 3 elements.")
            return False
        try:
            draw_flag = int(parts[0])
            delta_x = int(parts[1])
            delta_y = int(parts[2])
        except ValueError:
            print(f"Error: Line {idx+1} contains non-integer values.")
            return False
        if draw_flag not in (0, 1):
            print(f"Error: Line {idx+1} draw_flag must be 0 or 1.")
            return False
        instructions.append([draw_flag, delta_x, delta_y])

    # Simulate movement and check bounds
    x, y = 0, 0
    for idx, (draw_flag, delta_x, delta_y) in enumerate(instructions):
        x_new = x + delta_x
        y_new = y + delta_y
        if not (0 <= x_new < 14 and 0 <= y_new < 10):
            print(f"Error: Movement in line {idx+1} goes out of bounds ({x_new}, {y_new}).")
            return False
        x, y = x_new, y_new
    return instructions

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_ascii_arm():
    print(r"""
      ████  IA DRAW ARM  ████
    """)

def main():
    
    instructions_prompt = (
        "You are a robotic arm that moves a pen over a 14×10 grid (14 columns, 10 rows).\n"
        "Each cell is 0.5 cm, forming a 7 cm × 5 cm whiteboard.\n"
        "You always start at position (0, 0), the bottom-left corner of the grid — this is just your starting point, not necessarily where the drawing begins.\n"
        "\n"
        "You will receive a natural language prompt (e.g. “draw a cat”, “write the number 3”) and must respond with a list of movement instructions to draw a symbolic, simplified version of the requested figure.\n"
        "\n"
        "Each instruction must follow this format:\n"
        "<draw_flag> <delta_x> <delta_y>\n"
        "\n"
        "Where:\n"
        "- `<draw_flag>` is `1` to draw a line, or `0` to move without drawing.\n"
        + "`<delta_x>` is the number of grid cells to move horizontally (positive = right, negative = left).\n"
        + "`<delta_y>` is the number of grid cells to move vertically (positive = up, negative = down).\n"
        "\n"
        "✏️ When draw_flag is `1`, draw a **single straight line** directly from your current position to the new position. This can include diagonal lines if both delta_x and delta_y are non-zero.\n"
        "📐 To draw perfectly horizontal or vertical lines, make one of the deltas zero.\n"
        "\n"
        "📏 Make the drawing as large as possible, filling most of the 14×10 grid while staying within bounds.\n"
        "🧩 Center the drawing both horizontally and vertically when appropriate, rather than always starting from (0, 0).\n"
        "➕ Use as many steps as needed — 20, 30, or more — to represent the shape clearly.\n"
        "\n"
        "🧠 Be symbolic but expressive. Use a minimal set of lines that give a clear idea of the requested drawing.\n"
        "\n"
        "🎯 Return ONLY the list of instructions, one per line. Do not include explanations, titles, or extra text.\n"
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
        "Now respond to this prompt: "
    )
    print("AI Chat - Type 'exit' to quit")
    while True:
        clear_terminal()
        print_ascii_arm()
        print("="*40)
        print("Prompt to draw with IA ARMY")
        print("="*40)
        user_input = input("> ")
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting chat...")
            break
        ai_response = chat_with_ai(instructions_prompt + user_input)
        instructions = validate_input(ai_response)
        while instructions is False:
            clear_terminal()
            print_ascii_arm()
            print("="*40)
            print("Prompt to draw with IA ARM DRAWING")
            print("="*40)
            user_input = input("> ")
            if user_input.lower() in ["exit", "quit"]:
                print("Exiting chat...")
                return
            ai_response = chat_with_ai(instructions_prompt + user_input)
            instructions = validate_input(ai_response)
        print("Numeric matrix of instructions:")
        print(instructions)

if __name__ == "__main__":
    main()
