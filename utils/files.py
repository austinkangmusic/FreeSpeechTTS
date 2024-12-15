def read(file_path: str) -> str:
    """
    Reads the content of a file and returns it as a string.
    
    Supports any text-based file format (e.g., .json, .md, .txt).
    
    Parameters:
        file_path (str): The path to the file to be read.
    
    Returns:
        str: The content of the file as a string.
    
    Raises:
        FileNotFoundError: If the file does not exist.
        ValueError: If the file cannot be read as text.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return file.read()
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {file_path}")
    except Exception as e:
        raise ValueError(f"An error occurred while reading the file: {e}")
