import os
from .file_utils import file_verify_path, file_verify_file, FileUtilsError, FileOperator
from my_logging import log

def write_file(working_directory, file_path, content):
    ret_string = f'Result for writing to file "{'current' if file_path == '.' else file_path}":\n'
    # Handle nested directories in file path
    if "/" in file_path:
        # verify directory first (directory part only)
        dir_part = file_path.rsplit('/', 1)[0]
        path_to_directory = file_verify_path(working_directory, dir_part)
        
        # if directory is outside working dir, return error
        if path_to_directory == FileUtilsError.OUTSIDE_WORKING_DIR.value.format(directory=dir_part):
            log(f"Error accessing directory: {path_to_directory}")
            return ret_string + "    " + path_to_directory

        # if directory does not exist, create it
        if path_to_directory == FileUtilsError.NOT_A_DIRECTORY.value.format(directory=dir_part):
            create_dir = os.path.join(working_directory, dir_part)
            log(f'Creating directory "{create_dir}" for new file.')
            os.makedirs(create_dir, exist_ok=True)
    
    path_to_file = file_verify_file(working_directory, file_path, options=FileOperator.WRITE_FILE)
    # If the verifier returned an error string, propagate it back to caller
    if isinstance(path_to_file, str) and path_to_file.startswith("Error:"):
        log(f"Error accessing file: {path_to_file}")
        return ret_string + "    " + path_to_file

    with open(path_to_file, 'w') as file:
        file.write(content)
        log(f'Wrote to file "{path_to_file}".')
    return ret_string + f'Successfully wrote to "{file_path}" ({len(content)} characters written)'