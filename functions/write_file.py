import os

def write_file(working_directory, file_path, content):
    try:
        working_dir_abs = os.path.abspath(working_directory) #absolute working dir path
        abs_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path)) #joined file path and directory path

        if os.path.commonpath([working_dir_abs, abs_file_path]) != working_dir_abs:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
        
        if os.path.isdir(abs_file_path):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        
        os.makedirs(os.path.dirname(abs_file_path), exist_ok=True) #Make any directories that don't already exist

        with open(abs_file_path, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
    except Exception as e:
        return f"Error: {e}"