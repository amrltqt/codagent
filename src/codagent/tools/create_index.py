
from codagent.tools.get_directory_structure import get_directory_structure
from codagent.tools.read_source_file import read_source_file

CODE_BASE_ROOT = "./src"

def create_index():
    # Get the directory structure
    directory_structure = get_directory_structure()
    
    # Initialize an empty dictionary to store the index
    index = {}
    
    # Iterate over each file in the directory structure
    for file_path in directory_structure:
        # Read the content of the file
        file_content = read_source_file(file_path)
        
        # Add the file content to the index
        index[file_path] = file_content
    
    # Return the index
    return index

DESCRIPTION = {
    "name": "create_index",
    "description": "Retrieve an index of all files in the code base",
    "parameters": [],
    "returns": "A dictionary containing the content of all files as string in the code base",
    "callable": create_index,
}

if __name__ == "__main__":
    print(create_index())
