import os
import sys
import pandas as pd
from dataclasses import dataclass

# Add the project's root directory to sys.path to enable importing from 'src'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.logger import logging
from src.exception import CustomException

class EXLLoader:
    def __init__(self, directory, filename):
        self.directory = directory
        self.filename = filename

    def load_exl(self):
        file_path = os.path.join(self.directory, self.filename)
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"{self.filename} not found in {self.directory}")
        return pd.read_excel(file_path, sheet_name = "Q 4", engine = "openpyxl")
    
# excel_df = EXLLoader("/Users/vahid/Downloads/Project/Experiments/Data/", "VaR.xlsx")
# df     = excel_df.load_exl()

