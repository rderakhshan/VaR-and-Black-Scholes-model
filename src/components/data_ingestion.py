import os
import sys
import pandas as pd
from dataclasses import dataclass

# Add the project's root directory to sys.path to enable importing from 'src'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.logger import logging
from src.exception import CustomException

logging.info("Data ingestion part is started.")


class EXLLoader:
    """
    A class to load Excel files.

    Attributes:
        directory (str): The path to the directory containing the Excel file.
        filename (str): The name of the Excel file to be loaded.
    """

    def __init__(self, directory: str, filename: str):
        """
        Initializes the EXLLoader with the directory and filename.

        Parameters:
            directory (str): The path to the directory containing the Excel file.
            filename (str): The name of the Excel file to be loaded.
        """
        self.directory = directory
        self.filename = filename

    def load_exl(self) -> pd.DataFrame:
        """
        Loads the specified Excel file and returns the data as a pandas DataFrame.

        Returns:
            pd.DataFrame: The data from the specified sheet of the Excel file.

        Raises:
            FileNotFoundError: If the specified Excel file does not exist in the directory.
        """
        file_path = os.path.join(self.directory, self.filename)
        
        # Check if the file exists
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"{self.filename} not found in {self.directory}")
        
        logging.info("Data ingestion part is done.")

        # Load and return the data from the specified sheet using pandas
        return pd.read_excel(file_path, sheet_name="Q 4", engine="openpyxl")
    
    


# Example usage (commented out for demonstration purposes)
# excel_df = EXLLoader("/Users/vahid/Downloads/Project/Experiments/Data/", "VaR.xlsx")
# df = excel_df.load_exl()
