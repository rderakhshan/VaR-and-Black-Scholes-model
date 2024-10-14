import os
import subprocess

def run_python_file(directory, filename):
    """
    Runs a Python file located in the specified directory.

    Parameters:
        directory (str): The path to the directory containing the Python file.
        filename (str): The name of the Python file to run.

    Returns:
        None
    """
    # Construct the full path to the Python file
    file_path = os.path.join(directory, filename)
    
    # Check if the file exists
    if not os.path.isfile(file_path):
        print(f"File '{file_path}' does not exist.")
        return  # Exit the function if the file does not exist

    # Run the Python file
    try:
        # Use subprocess to run the Python file and check for errors
        subprocess.run(['python', file_path], check=True)
        print(f"Executed '{filename}' successfully.")
    except subprocess.CalledProcessError as e:
        # Handle errors that occur during execution of the subprocess
        print(f"Failed to execute '{filename}'. Error: {e}")
    except Exception as e:
        # Handle any other unexpected exceptions
        print(f"An unexpected error occurred: {e}")

# Set the directory containing the Python files
directory = './src/components/'  # Replace with the path to your directory

# List of Python files to run
files_list = ["data_ingestion.py", "data_transformation.py", "VaR_calculation.py"]

# Iterate through the list of files and run each one
for pyfile in files_list:
    run_python_file(directory, pyfile)
