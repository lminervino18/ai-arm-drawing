import time
from ai_client import chat_with_ai
from validation import validate_instruction_list
from rescale import auto_close_shape
from prompt_engineer import build_correction_prompt

def get_valid_instruction_list(initial_prompt: str, user_prompt: str):
    """
    Repeatedly tries to get a valid instruction list from the AI.
    If the first result is valid, a refinement step is requested.
    Returns a validated and auto-closed instruction list.
    """
    retries = 0

    while True:
        try:
            ai_raw = chat_with_ai(initial_prompt)
        except Exception as e:
            print(f"AI error: {e}")
            time.sleep(5)
            continue

        instructions = validate_instruction_list(ai_raw)
        if instructions:
            correction_prompt = build_correction_prompt(ai_raw, user_prompt)
            try:
                refined_raw = chat_with_ai(correction_prompt)
                refined_instructions = validate_instruction_list(refined_raw)
                if refined_instructions:
                    return auto_close_shape(refined_instructions)
            except Exception as e:
                print(f"Refinement AI error: {e}")

            # Fall back to original if correction fails
            return auto_close_shape(instructions)

        retries += 1
        print(f"Retrying generation... attempt {retries}")
        time.sleep(1)
