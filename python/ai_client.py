import os
from openai import OpenAI
from dotenv import load_dotenv

# Load API key and project ID from .env or environment
load_dotenv()
api_key = os.getenv("OPENAI_API_KEY")
project_id = os.getenv("OPENAI_PROJECT_ID")

if not api_key or not project_id:
    raise ValueError("Both OPENAI_API_KEY and OPENAI_PROJECT_ID must be set.")

# Configure OpenAI client with API key and project
client = OpenAI(
    api_key=api_key,
    project=project_id
)

def chat_with_ai(prompt: str) -> str:
    """
    Send a prompt to OpenAI and get a response.

    Args:
        prompt (str): The user's input message or question.

    Returns:
        str: The AI's text response.
    """

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # You can change to "gpt-4-turbo" if needed
        messages=[
            {
                "role": "system",
                "content": "You are an AI that converts prompts into robotic arm instructions in a 14x10 grid."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.4,
        max_tokens=1024
    )
    return response.choices[0].message.content.strip()
