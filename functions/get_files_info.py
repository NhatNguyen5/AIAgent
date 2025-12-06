import os

def get_files_info(working_directory, directory="."):
    path_to_directory = os.path.join(working_directory, directory)
    directory = "current" if directory == "." else f"'{directory}'"
    ret_string = f"Result for {directory} directory:\n"

    if not path_to_directory.startswith(working_directory) or ".." in os.path.relpath(path_to_directory, working_directory):   
        return ret_string + f'   Error: Cannot list {directory} as it is outside the permitted working directory'
    if not os.path.isdir(path_to_directory):
        return ret_string + f'   Error: {directory} is not a directory'
    
    list_of_files = os.listdir(path_to_directory)   
    for file_name in list_of_files:
        file_path = os.path.join(path_to_directory, file_name)
        file_size = os.path.getsize(file_path)
        is_directory = os.path.isdir(file_path)
        ret_string += display_info(file_name, file_size, is_directory)
    return ret_string


def display_info(file_name, file_size, is_directory):
    return f"- {file_name}: file_size={file_size} bytes, is_dir={is_directory}\n"