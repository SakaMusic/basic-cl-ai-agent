import os
import subprocess

def run_python_file(working_directory, file_path, args=None):
    try:
        working_dir_abs = os.path.abspath(working_directory) #absolute working dir path
        abs_file_path = os.path.normpath(os.path.join(working_dir_abs, file_path)) #joined file path and directory path

        if os.path.commonpath([working_dir_abs, abs_file_path]) != working_dir_abs:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(abs_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        
        if not abs_file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'
        
        command = ["python", abs_file_path]
        if args: command.extend(args)

        completed_command = subprocess.run(args=command,
                                        capture_output=True,
                                        text=True,
                                        timeout=30,
                                        cwd=working_dir_abs
                                        )
        
        output = []
        
        if completed_command.returncode != 0:
            output.append(f"Process exited with code {completed_command.returncode}")
        if len(completed_command.stdout) == 0 and len(completed_command.stderr) == 0:
            output.append(f"No output produced")
        if completed_command.stdout:
            output.append(f"STDOUT:\n{completed_command.stdout}")
        if completed_command.stderr:
            output.append(f"STDERR:\n{completed_command.stderr}")

        return "\n".join(output)
    
    except Exception as e:
        return f"Error: executing Python file: {e}"
        