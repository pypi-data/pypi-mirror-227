import argparse
import openai
import os
import subprocess

# Path to the configuration file
CONFIG_FILE_PATH = os.path.expanduser("~/.aifix_config")

# Load API key from the configuration file if available
if os.path.exists(CONFIG_FILE_PATH):
    with open(CONFIG_FILE_PATH, "r") as config_file:
        api_key = config_file.read().strip()
        openai.api_key = api_key

model_id = "gpt-3.5-turbo"

def save_api_key(api_key):
    with open(CONFIG_FILE_PATH, "w") as config_file:
        config_file.write(api_key)

def ChatGPT_conversation(conversation):
    response = openai.ChatCompletion.create(
        model=model_id,
        messages=conversation
    )
    conversation.append({'role': 'AI', 'content': response.choices[0].message['content']})
    return conversation

def setup_api_key():
    api_key = input("Enter your OpenAI API key: ")
    openai.api_key = api_key
    save_api_key(api_key)

def enable_assistance():
    # Logic to enable AI assistance
    print("AI assistance enabled.")

def disable_assistance():
    # Logic to disable AI assistance
    print("AI assistance disabled.")

def main():
    parser = argparse.ArgumentParser(description="AI-powered error fixer")
    parser.add_argument("--config", action="store_true", help="Setup OpenAI API key")
    parser.add_argument("--enable", action="store_true", help="Enable AI assistance")
    parser.add_argument("--disable", action="store_true", help="Disable AI assistance")
    parser.add_argument("--plz", type=str, help="Request AI assistance for an error message along with the file name")
    args = parser.parse_args()

    if args.config:
        setup_api_key()
    elif args.enable:
        enable_assistance()
    elif args.disable:
        disable_assistance()
    elif args.plz:
        file_name = args.plz
        previous_command = subprocess.check_output("history | tail -n 2 | head -n 1", shell=True, text=True)
        previous_command_lines = previous_command.strip().split("\n")
        last_command = previous_command_lines[-1]
        print("Last command:", last_command)
        if not os.path.exists(file_name):
            print(f"File '{file_name}' not found in the current directory.")
            return

        with open(file_name, "r") as code_file:
            code = code_file.read()

        prompt = input("Enter the prompt or the error message: ")
        conversation = [
            {"role": "user", "content": "You are a coding assistant and help me with this code and the prompt: \n" + code + "\n\n" + last_command + "\nPrompt:\n" + prompt},
        ]
        ai_response = ChatGPT_conversation(conversation)
        print("AI Response: \n", ai_response[-1]['content'])
    else:
        parser.print_help()

if __name__ == "__main__":
    main()