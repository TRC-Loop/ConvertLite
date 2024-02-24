import os

def get_file_name_without_extension(file_path):
    # Extract the base name of the file (e.g., 'image.png' from '/path/to/image.png')
    base_name = os.path.basename(file_path)
    # Split the base name into the file name and extension and return just the name
    file_name_without_extension, _ = os.path.splitext(base_name)
    return file_name_without_extension

def get_full_file_name(file_path):
    # Extract the base name of the file, which includes the extension
    full_file_name = os.path.basename(file_path)
    return full_file_name

def get_file_type(file_path):
    # Extract the extension from the file path
    _, file_extension = os.path.splitext(file_path)
    # Remove the dot and convert to lowercase
    file_type = file_extension[1:].lower()
    return file_type