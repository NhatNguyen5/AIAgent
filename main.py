import argparse
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types, errors
from config import *
from prompts import *
from my_logging import log
from functions.my_schemas import available_functions

def main():
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key:
        print("GEMINI_API_KEY loaded successfully.")
        client = genai.Client(api_key=api_key)
    else:
        raise Exception("GEMINI_API_KEY not found.")
    
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt
            )   
        )
    except errors.ClientError as e:
        log(f"Error during content generation: {e.code} | {e.message}")
        print(f"An error occurred: {e.message}")
        return
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    log(f"User prompt: {args.user_prompt}, Prompt tokens: {response.usage_metadata.prompt_token_count}, Response tokens: {response.usage_metadata.candidates_token_count}")
    log(f"Response: {response}")
    print(f"Response:\n{response.text}")
    if response.function_calls != None:
        for function_call in response.function_calls:
            print(f"Calling function: {function_call.name}({function_call.args})")

if __name__ == "__main__":
    main()
