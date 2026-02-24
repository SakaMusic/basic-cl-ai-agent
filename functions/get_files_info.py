import os

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