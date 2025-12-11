from google.genai import types
from functions.get_files_info import get_files_info
from functions.get_file_content import get_file_content
from functions.run_python_file import run_python_file
from functions.write_file import write_file
from my_logging import log, log_print

def call_function(function_call_part, verbose=False):
    function_name = function_call_part.name
    function_arguments = function_call_part.args
    if verbose:
        print(f"Calling function: {function_name}({function_arguments})")
    else:
        print(f" - Calling function: {function_name}")
    log(f"Calling function: {function_name} with arguments: {function_arguments}")
    working_directory = "./calculator"
    functions = ["get_file_content", "get_files_info", "run_python_file", "write_file"]
 
    if function_name in functions:
        function_result = ""
        if function_name == "get_files_info":
            function_result = get_files_info(working_directory, **function_arguments)
        elif function_name == "get_file_content":
            function_result = get_file_content(working_directory, **function_arguments)
        elif function_name == "run_python_file":
            function_result = run_python_file(working_directory, **function_arguments)
        elif function_name == "write_file":
            function_result = write_file(working_directory, **function_arguments)
        log(f"Function {function_name} returned: {function_result}")
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"result": function_result},
                )
            ],
        ) 
    else:
        log(f"Unknown function called: {function_name}")
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    
    