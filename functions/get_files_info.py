import os
from .file_utils import file_verify_path, FileUtilsError
from my_logging import log

def get_files_info(working_directory, directory="."):   
    path_to_directory = file_verify_path(working_directory, directory)
    ret_string = f"Result for {'current' if directory == '.' else directory} directory:\n"
    log(f"Attempting to access directory: {directory}")
    if path_to_directory in (FileUtilsError.OUTSIDE_WORKING_DIR.value.format(directory=directory),
                             FileUtilsError.NOT_A_DIRECTORY.value.format(directory=directory)):
        log(path_to_directory)
        return ret_string + "    " + path_to_directory
    list_of_files = os.listdir(path_to_directory)   
    for file_name in list_of_files:
        file_path = os.path.join(path_to_directory, file_name)
        file_size = os.path.getsize(file_path)
        is_directory = os.path.isdir(file_path)
        ret_string += display_info(file_name, file_size, is_directory)
        log(f"    Read file info: {file_name}, size: {file_size}, is_dir: {is_directory}")
    return ret_string

def display_info(file_name, file_size, is_directory):
    return f"- {file_name}: file_size={file_size} bytes, is_dir={is_directory}\n"