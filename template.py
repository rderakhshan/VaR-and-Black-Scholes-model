import os
from pathlib import Path

# List of file paths to be checked or created
list_of_files = [
    ".github/workflows/main.yaml",
    "src/__init__.py",
    "src/utils.py",
    "src/logger.py",
    "src/exception.py",
    "src/components/__init__.py",
    "src/components/data_ingestion.py",
    "src/components/VaR_calculation.py",
    "src/components/Pricing.py",
    "src/pipeline/VaR_pipeline.py",
    "src/pipeline/pricing_pipeline.py",
    "requirements.txt",
    "Experiments/Value at Risk/VaR.ipynb",
    "Experiments/Pricing/Pricing.ipynb",
    "Experiments/Data/VaR.xlsx",
    "Artifacts/Artifacts",
    "Results/Results",
    "Assignment.py",
    "utils.py",
]

for filepath in list_of_files:
    """
    This loop iterates over the list of file paths, checks if the specified directories exist,
    and creates them if necessary. It then creates an empty file for each specified path if
    the file does not exist or is empty.

    Input:
        - list_of_files: A list of strings, each representing the relative path to a file or directory.

    Process:
        - For each file path:
            1. Convert the path string to a Path object for compatibility with different operating systems.
            2. Split the file path into the directory and file name.
            3. If the directory portion is not empty, create the directory (including any intermediate directories).
            4. If the file does not exist or is empty, create an empty file at that location.

    Output:
        - This script does not return any values, but it ensures that all specified files
          and their parent directories exist on the filesystem.
    """
    # Convert the string path to a Path object
    filepath = Path(filepath)
    
    # Split the file path into directory and filename
    filedir, filename = os.path.split(filepath)
    
    # If the directory part is not empty, create the directory
    if filedir != "":
        # Create the directory if it doesn't exist, including any intermediate directories
        os.makedirs(filedir, exist_ok=True)
    
    # If the file does not exist or its size is zero, create an empty file
    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass  # Create an empty file
