

def read_source_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()
    

DESCRIPTION = {
    "name": "read_source_file",
    "description": "Read the content of a source file with the precise file path. Get the precise file path with 'get_directory_structure' tool",
    "parameters": [
        {
            "name": "file_path",
            "description": "The path of the file to read"
        }
    ],
    "returns": "The content of the file as a string",
    "callable": read_source_file,
}