# This file is used to create or update a code file in the code base.
# It is used to define the functions that will be used to create or update the code file.


import os

from codagent.tools.read_source_file import read_source_file

CODE_BASE_ROOT = "./src"

def create_or_update_code_file(code_file_path, content):
    raw_content = rf"{content}"

    before = ""
    if os.path.exists(code_file_path): 
        before = read_source_file(code_file_path)
    with open(code_file_path, "w") as f:
        f.write(raw_content)
    after = read_source_file(code_file_path)

    return {
        "before": before,
        "after": after,
    }

DESCRIPTION = {
    "name": "create_or_update_code_file",
    "description": "Create or update the content of a source file with the content provided",
    "parameters": [
        {
            "name": "path",
            "description": "The path to the directory",
            "type": "string",
        },
        {
            "name": "content",
            "description": "The content to write in the file",
            "type": "string",
        }
    ],
    "returns": "A dictionary containing the content before and after the update",
    "callable": create_or_update_code_file,
}