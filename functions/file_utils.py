#######################################################################
#                          
# File Utils
#
# Utility functions for file and directory operations
# Handles path verification and error management
#
#######################################################################

import os
from enum import Enum

class FileUtilsError(str, Enum):
    # Directory related errors
    OUTSIDE_WORKING_DIR = 'Error: Cannot list {directory} as it is outside the permitted working directory'
    NOT_A_DIRECTORY = 'Error: {directory} is not a directory'
    # File related errors
    # Read file errors
    FILE_READ_OUTSIDE_WORKING_DIR = 'Error: Cannot read {file_path} as it is outside the permitted working directory'
    FILE_READ_NOT_FOUND_OR_NOT_REGULAR = 'Error: File not found or is not a regular file: "{file_path}"'
    # Write file errors
    FILE_WRITE_OUTSIDE_WORKING_DIR = 'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    FILE_WRITE_NOT_FOUND_OR_NOT_REGULAR = 'Error: File not found or is not a regular file: "{file_path}"\n    Create the file before writing to it.'


class FileOperator(str, Enum):
    READ_FILE = 'read_file'
    WRITE_FILE = 'write_file'

def file_verify_path(working_directory, directory):
    path_to_directory = os.path.join(working_directory, directory)

    if not path_to_directory.startswith(working_directory) or ".." in os.path.relpath(path_to_directory, working_directory):   
        return FileUtilsError.OUTSIDE_WORKING_DIR.value.format(directory=directory)
    
    if not os.path.isdir(path_to_directory):
        return FileUtilsError.NOT_A_DIRECTORY.value.format(directory=directory)
    
    return path_to_directory

def file_verify_file(working_directory, file, options=None):
    path_to_file = os.path.join(working_directory, file)
    match options:
        case FileOperator.READ_FILE, None:
            if not path_to_file.startswith(working_directory) or ".." in os.path.relpath(path_to_file, working_directory):   
                return FileUtilsError.FILE_OUTSIDE_WORKING_DIR.value.format(directory=file)
            
            if not os.path.isfile(path_to_file):
                return FileUtilsError.FILE_NOT_FOUND_OR_NOT_REGULAR.value.format(directory=file)
        case FileOperator.WRITE_FILE:
            if not path_to_file.startswith(working_directory) or ".." in os.path.relpath(path_to_file, working_directory):
                return FileUtilsError.FILE_WRITE_OUTSIDE_WORKING_DIR.value.format(file_path=file)
            
            if not os.path.isfile(path_to_file):
                return FileUtilsError.FILE_WRITE_NOT_FOUND_OR_NOT_REGULAR.value.format(file_path=file)

        case _:
            raise ValueError("Invalid file operation option provided.")
    
    return path_to_file