import argparse
import os
from dotenv import load_dotenv
from google import genai
from google.genai import types, errors
from functions.call_function import call_function
from config import *
from prompts import *
from my_logging import log, log_print
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

    # create initial message
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    for _ in range(MAX_ATTEMPTS):
        log(f"Attempt {_ + 1} to get response.")
        response = generate_content(client, messages)
        candidate_no_function_call = True
        for candidate in response.candidates:
            log(f"Candidate of attempt {_ + 1} received: {candidate.content}")
            messages.append(candidate.content)
            if candidate.content.parts is None or candidate.content.parts[0].function_call is None:
                continue
            candidate_no_function_call = False
            response_function_call_result = do_response_call_function(response, args)
            if response_function_call_result is not None:
                messages.append(types.Content(role="user", parts=response_function_call_result.parts))        
        #log_print(f"Response candidate: {response.candidates[0].content}", 
                #f"Response candidate:\n{response.candidates[0].content}")   
        if candidate_no_function_call and response.text is not None:
            break
    print_response(response, args)
    
    return 0

def generate_content(client, messages):    
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions], system_instruction=system_prompt
            )   
        )       
    except errors.ClientError as e:
        log_print(f"Error during content generation: {e.code} | {e.message}",
                  f"An error occurred: {e.message}")
        return e
    return response

def print_response(response, args):
    # if verbose, print detailed info
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")
    log(f"User prompt: {args.user_prompt}, Prompt tokens: {response.usage_metadata.prompt_token_count}, Response tokens: {response.usage_metadata.candidates_token_count}")
    log_print(f"Response: {response.text}", 
              f"Response:\n{response.text}")
    #log(f"Response: {response.text}")

def do_response_call_function(response, args):
    # handle function calls
    if response.function_calls != None:
        for function_call in response.function_calls:
            try:
                function_call_result = call_function(function_call, verbose=args.verbose)
            except Exception as e:
                log_print(f"Error during function call: {str(e)}",
                          f"An error occurred while calling the function: {str(e)}")
                raise e
            if args.verbose:
                print(f"-> {function_call_result.parts[0].function_response.response}")
            #else:
                #print(f"Function response: {function_call_result.parts[0].function_response.response['result']}")
            return function_call_result

if __name__ == "__main__":
    main()
