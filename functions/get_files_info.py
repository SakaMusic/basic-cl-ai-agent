import os
from google.genai import types

def get_files_info(working_directory, directory="."):
    try:
        working_dir_abs = os.path.abspath(working_directory) #absolute path
        target_dir = os.path.normpath(os.path.join(working_dir_abs, directory)) #relative path
        valid_target_dir = os.path.commonpath([working_dir_abs, target_dir]) == working_dir_abs #check to see if relative path in absolute path
        
        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
        
        if not os.path.isdir(target_dir):
            return f'Error: "{directory}" is not a directory'
        
        dir_items_list = []
        for item in os.listdir(target_dir):
            item_path = os.path.join(target_dir, item)
            is_dir = os.path.isdir(item_path)
            file_size = os.path.getsize(item_path)
            item_string = f"- {item}: file_size={file_size} bytes, is_dir={is_dir}"
            dir_items_list.append(item_string)
        
        return "\n".join(dir_items_list)
    except Exception as e:
        return f"Error: {e}"
    
schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Lists content of a file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="path to the file"
            )
        },
        required=["file_path"]
    )
)

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Write to a file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="path to the file"
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="contents of file"
            )
        },
        required=["file_path", "content"]
    )
)

schema_run_python_file = types.FunctionDeclaration(
    name="run_python_file",
    description="Run a python file",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="path to the file"
            ),
            "args": types.Schema(
                type=types.Type.ARRAY,
                items=types.Schema(
                    type=types.Type.STRING,
                ),
                description="Array of arguments"
            )
        },
        required=["file_path"]
    )
)