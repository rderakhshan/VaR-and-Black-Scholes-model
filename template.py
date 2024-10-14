import os
from pathlib import Path

list_of_files = [
   ".github/workflows/main.yaml",
#    "src/__init__.py",
#    "src/utils.py",
#    "src/logger.py",
#    "src/exception.py",
#    "src/components/__init__.py",
#    "src/components/data_ingestion.py",
#    "src/components/VaR_calculation.py",
#    "src/components/Pricing.py",
#    "src/pipeline/VaR_pipeline.py",
#    "src/pipeline/pricing_pipeline.py",
#    "requirements.txt",
#    "Experiments/Value at Risk/VaR.ipynb",
#    "Experiments/Pricing/Pricing.ipynb",
#    "Experiments/Data/VaR.xlsx",
#    "Artifacts/Artifacts",
#    "Results/Results",
#    "Assignment.py",
#    "utils.py",
]

for filepath in list_of_files:
    filepath = Path(filepath)
    filedir, filename = os.path.split(filepath)
    if filedir != "":
        os.makedirs(filedir, exist_ok=True)

    if (not os.path.exists(filepath)) or (os.path.getsize(filepath) == 0):
        with open(filepath, "w") as f:
            pass # create an empty file
