import os
import subprocess

def run_python_file(directory, filename):
    # Construct the full path to the Python file
    file_path = os.path.join(directory, filename)
    
    # Check if the file exists
    if not os.path.isfile(file_path):
        print(f"File '{file_path}' does not exist.")
        return

    # Run the Python file
    try:
        subprocess.run(['python', file_path], check=True)
        print(f"Executed '{filename}' successfully.")
    except subprocess.CalledProcessError as e:
        print(f"Failed to execute '{filename}'. Error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

directory = '/Users/vahid/Downloads/Project/src/components/'  # Replace with the path to your directory
files_list = ["data_ingestion.py", "data_transformation.py", "VaR_calculation.py"]

for pyfile in files_list:
    run_python_file(directory, pyfile)
