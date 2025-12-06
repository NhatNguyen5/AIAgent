import os
from .file_utils import file_verify_file, FileUtilsError, FileOperator

def write_file(working_directory, file_path, content):
    path_to_file = file_verify_file(working_directory, file_path, options=FileOperator.WRITE_FILE)
    ret_string = f"Writing to file '{file_path}':\n"
    if path_to_file == FileUtilsError.FILE_WRITE_OUTSIDE_WORKING_DIR.value.format(file_path=file_path):
        return ret_string + "    " + path_to_file
    if path_to_file == FileUtilsError.FILE_WRITE_NOT_FOUND_OR_NOT_REGULAR.value.format(file_path=file_path):
        os.makedirs(os.path.dirname(path_to_file), exist_ok=True)
    with open(path_to_file, 'w') as file:
        file.write(content)
    return ret_string + f'Successfully wrote to "{file_path}" ({len(content)} characters written)'