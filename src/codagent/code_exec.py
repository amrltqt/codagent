
import io
import sys
import logging

from contextlib import redirect_stdout, redirect_stderr

from codagent.tools.get_directory_structure import get_directory_structure
from codagent.tools.read_source_file import read_source_file
from codagent.tools.update_code_file import create_or_update_code_file

safe_globals = {
    "__builtins__": {
        "print": print,
        "len": len,
        # Ajouter ici uniquement les fonctions nécessaires pour les actions
    },
    "read_source_file": read_source_file,
    "get_directory_structure": get_directory_structure,
    "update_code_file": create_or_update_code_file,
}


def execute_secure_action(action: str, allowed_globals: dict):
    """
    Executes a Python action string safely using exec(), capturing stdout and stderr.

    :param action: The Python code to execute as a string.
    :param allowed_globals: A dictionary of allowed functions and variables.
    :return: Tuple (stdout_output, stderr_output, error_flag)
    """
    logging.info(f"Executing action:\n{action}")

    # Capture stdout and stderr
    capture_output = io.StringIO()
    capture_error = io.StringIO()

    # Safe global environment
    safe_globals = {"__builtins__": {
        "print": print,
        "len": len,
    }}  # Restrict built-in functions
    safe_globals.update(allowed_globals)  # Add allowed functions

    error_flag = False  # Track if an error occurred

    try:
        with redirect_stdout(capture_output), redirect_stderr(capture_error):
            exec(action, safe_globals)
    except Exception as e:
        error_flag = True
        capture_error.write(f"Exception captured: {str(e)}\n")

    return capture_output.getvalue() + capture_error.getvalue(), error_flag