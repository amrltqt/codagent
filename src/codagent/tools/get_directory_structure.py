
import os
import fnmatch


CODE_BASE_ROOT = "./src"


def load_gitignore_patterns(code_base_root):
    """
    Reads the .gitignore file and returns a list of ignored patterns.
    
    :param code_base_root: Root directory where .gitignore is located
    :return: List of patterns to ignore
    """
    gitignore_path = os.path.join(code_base_root, ".gitignore")
    ignore_patterns = []

    if os.path.isfile(gitignore_path):
        with open(gitignore_path, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):  # Ignore comments and empty lines
                    if line.endswith("/"):  
                        # Convert directory ignores to pattern matching all their content
                        ignore_patterns.append(line.rstrip("/") + "/*")
                    ignore_patterns.append(line)

    return ignore_patterns

def is_ignored(path, ignore_patterns, code_base_root):
    """
    Checks if a given path should be ignored based on the .gitignore patterns.

    :param path: File or directory path to check
    :param ignore_patterns: List of patterns from .gitignore
    :param code_base_root: Root directory
    :return: True if the path should be ignored, False otherwise
    """
    relative_path = os.path.relpath(path, code_base_root)
    
    # Normalize path to use '/' instead of '\'
    relative_path = relative_path.replace(os.sep, "/")

    for pattern in ignore_patterns:
        # Handle directory patterns correctly
        if fnmatch.fnmatch(relative_path, pattern) or fnmatch.fnmatch(os.path.basename(path), pattern):
            return True

    return False

def get_directory_structure():
    """
    Prints the full path of each file in the given source directory,
    filtering out files and directories ignored in .gitignore.
    """

    all_files = []
    ignore_patterns = load_gitignore_patterns("./")
    for root, dirs, files in os.walk(CODE_BASE_ROOT):
        # Filter out ignored directories
        dirs[:] = [d for d in dirs if not is_ignored(os.path.join(root, d), ignore_patterns, CODE_BASE_ROOT)]

        # Print each file with full path, filtering out ignored files
      # Print each file with full path, filtering out ignored files
        for file in sorted(files):
            full_path = os.path.join(root, file).replace(os.sep, "/")
            if not is_ignored(full_path, ignore_patterns, CODE_BASE_ROOT):
                all_files.append(full_path)
    return all_files

DESCRIPTION = {
    "name": "get_directory_structure",
    "description": "Read the directory structure of the code base",
    "parameters": [],
    "returns": "List of full paths of files as strings",
    "callable": get_directory_structure,
}

if __name__ == "__main__":
    print(get_directory_structure())
