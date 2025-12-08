import os
from datetime import datetime
from functions.file_utils import FileUtilsError, file_verify_path
from inspect import getframeinfo, stack
from config import LOGGING_ENABLED

def log(message):
    if not LOGGING_ENABLED:
        return
    date = datetime.now().strftime("%Y-%m-%d")
    time = datetime.now().strftime("%H:%M:%S")
    timestamp = f"{date} {time}"
    frameinfo = getframeinfo(stack()[1][0])
    logistic_data = f"[{timestamp}][{frameinfo.filename.rsplit('/', 1)[-1]}:{frameinfo.lineno}]"
    padded_space = "".rjust(len(logistic_data))
    message = message.replace("\n", f"\n{padded_space}")  # Ensure single line log entries
    log_entry = f"{logistic_data} {message}\n"
    file_path = file_verify_path("./", "logs")
    if file_path == FileUtilsError.NOT_A_DIRECTORY.value.format(directory="logs"):
        os.makedirs(os.path.join("./", "logs"), exist_ok=True)
    if isinstance(file_path, str) and not file_path.startswith("Error"):
        file_name = os.path.join("./", "logs", f"{date}_logging.txt")
        if not os.path.isfile(file_name):
            with open(file_name, "w") as log_file:
                log_file.write(f"Log file created on {date} at {time}\n")
        with open(file_name, "a") as log_file:
            log_file.write(log_entry)