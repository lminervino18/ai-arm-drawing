from ai_client import chat_with_ai

def main():
    print("AI Chat - Type 'exit' to quit")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Exiting chat...")
            break
        
        # Get AI response
        ai_response = chat_with_ai(user_input)
        
        # Show AI response
        print("AI:", ai_response)

if __name__ == "__main__":
    main()
