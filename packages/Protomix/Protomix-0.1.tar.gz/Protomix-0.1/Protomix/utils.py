import os
import glob

def get_paths(root_directory: str, filename: str) -> list:
    """
    Retrieve all paths matching the specified filename within the root_directory and its subdirectories.

    Parameters:
    - root_directory (str): The starting directory from which the search begins.
    - filename (str): The name of the file to search for.

    Returns:
    - list: A list of full paths to the files matching the specified filename. If no files are found, returns an empty list.

    Note:
    This function performs a recursive search, so it will also look in all subdirectories of the root_directory.
    """
    
    # Assertive checks for input parameters
    assert isinstance(root_directory, str), "Expected 'root_directory' to be a string."
    assert isinstance(filename, str), "Expected 'filename' to be a string."
    assert root_directory, "'root_directory' should not be an empty string."
    assert filename, "'filename' should not be an empty string."
    assert os.path.isdir(root_directory), f"'{root_directory}' is not a valid directory."
    
    # Construct the search pattern using os.path.join to ensure platform-independent behavior.
    # '**' allows for recursive search in all subdirectories, and the filename is what we're looking for.
    search_pattern = os.path.join(root_directory, '**', filename)
    
    # Use glob with recursive=True to find all matching paths.
    paths = glob.glob(search_pattern, recursive=True)
    
    return paths
