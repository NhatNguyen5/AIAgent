import subprocess
from functions.file_utils import file_verify_file, FileOperator, FileExecutionError
from my_logging import log

def run_python_file(working_directory, file_path, args=[]):
    path_to_file = file_verify_file(working_directory, file_path, options=FileOperator.EXECUTE_FILE)
    if isinstance(path_to_file, str) and path_to_file.startswith("Error:"):
        log(path_to_file)
        return path_to_file
    command = ["python", file_path] + args

    log(f"Executing command: {' '.join(command)}")
    try:
        completed_process = subprocess.run(command, capture_output=True, text=True, cwd=working_directory, timeout=30)
    except subprocess.CalledProcessError as e:
        log(FileExecutionError.EXECUTION_FAILED.value.format(file_path=file_path, error_message=str(e)))
        return FileExecutionError.EXECUTION_FAILED.value.format(file_path=file_path, error_message=str(e))
    
    output = completed_process.stdout
    error = completed_process.stderr
    if completed_process.returncode != 0:
        log(f"Process exited with code {completed_process.returncode}: error output:\n{error.strip()}")
        return f"Process exited with code {completed_process.returncode}"
    if output.strip() == "" and error.strip() == "":
        log("No output produced")
        return "No output produced"
    display_result_str = display_result(output.strip(), error.strip())
    log(f"Execution result for file '{file_path}':\n{display_result_str}")
    return display_result_str
    
def display_result(stdout, stderr):
    return f"STDOUT: {stdout}\nSTDERR: {stderr}"