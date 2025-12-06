import os
from .file_utils import file_verify_file, FileUtilsError
import config

def get_file_content(working_directory, file_path):
    path_to_file = file_verify_file(working_directory, file_path)
    ret_string = f"Result for {'current' if file_path == '.' else file_path} directory:\n"
    if path_to_file in (FileUtilsError.FILE_OUTSIDE_WORKING_DIR.value.format(file_path=file_path),
                             FileUtilsError.FILE_NOT_FOUND_OR_NOT_REGULAR.value.format(file_path=file_path)):
        return ret_string + "    " + path_to_file
    with open(path_to_file, 'r') as file:
        content = file.read()
    if len(content) > config.CHARACTER_LIMIT:
        content = content[:config.CHARACTER_LIMIT] + f"[...File \"{file_path}\" truncated at {config.CHARACTER_LIMIT} characters]."
    return ret_string + content