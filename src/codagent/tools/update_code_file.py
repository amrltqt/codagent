
from codagent.tools.read_source_file import read_source_file

CODE_BASE_ROOT = "./src"

def update_code_file(code_file_path, content):
    raw_content = rf"{content}"

    before = read_source_file(code_file_path)
    with open(code_file_path, "w") as f:
        f.write(raw_content)
    after = read_source_file(code_file_path)

    return {
        "before": before,
        "after": after,
    }

DESCRIPTION = {
    "name": "update_code_file",
    "description": "Update the content of a source file with the content provided",
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
    "callable": update_code_file,
}