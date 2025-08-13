from config import GRID_WIDTH, GRID_HEIGHT

def validate_instruction_list(ai_response: str):
    """
    Validates an AI-generated list of instructions.
    Returns a list of tuples (draw_flag: bool, x: int, y: int) if valid, or False if invalid.
    """
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
    

    return instructions
