# functions/get_file_content.py
from .file_utils import file_verify_file, FileUtilsError, FileOperator
import config
from my_logging import log

def get_file_content(working_directory, file_path):
    path_to_file = file_verify_file(working_directory, file_path, options=FileOperator.READ_FILE)
    ret_string = f"Result for {'current' if file_path == '.' else file_path} directory:\n"
    log(f"Attempting to read file: {file_path}")
    if isinstance(path_to_file, str) and path_to_file.startswith("Error:"):
        log(f"Error accessing file: {path_to_file}")
        return ret_string + "    " + path_to_file
    with open(path_to_file, 'r') as file:
        content = file.read()
    if len(content) > config.CHARACTER_LIMIT:
        content = content[:config.CHARACTER_LIMIT] + f"[...File \"{file_path}\" truncated at {config.CHARACTER_LIMIT} characters]."
    return ret_string + content