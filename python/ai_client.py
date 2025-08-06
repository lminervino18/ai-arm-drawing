import os
import google.generativeai as genai

# Load API key from environment variable
# Make sure you set GEMINI_API_KEY in your system environment
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    raise ValueError("GEMINI_API_KEY is not set. Please configure your environment variable.")

# Configure Gemini client
genai.configure(api_key=api_key)

def chat_with_ai(prompt: str) -> str:
    """
    Send a prompt to Gemini and get a response.
    
    Args:
        prompt (str): The user's input message or question.
    
    Returns:
        str: The AI's text response.
    """
    # Create a Gemini model instance
    model = genai.GenerativeModel("models/gemini-1.5-flash")
    
    # Generate a response from the model
    response = model.generate_content(prompt)

    # Return the generated text
    return response.text.strip()


