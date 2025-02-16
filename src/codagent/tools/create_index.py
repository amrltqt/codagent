# This file is used to create an index of all files in the code base.
# It is used to define the functions that will be used to create the index.


from pymilvus import MilvusClient
import numpy as np

from codagent.tools.get_directory_structure import get_directory_structure
from codagent.tools.read_source_file import read_source_file

CODE_BASE_ROOT = "./src"

client = MilvusClient("./milvus_db.db")
client.create_collection(
    collection_name="code_index",
    dimension=1024
)


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
    "description": "Retrieve an index of all files in the code base as a dictionary",
    "parameters": [],
    "returns": "A dictionary containing the content of all files as string in the code base.",
    "callable": create_index,
}

if __name__ == "__main__":
    print(create_index())
