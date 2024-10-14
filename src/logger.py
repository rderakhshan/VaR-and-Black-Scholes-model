import os
import logging
from datetime import datetime

# Set the log file name with the current timestamp
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"

# Define the directory where log files will be saved
log_path = os.path.join(os.getcwd(), "logs")

# Create the log directory if it does not already exist
os.makedirs(log_path, exist_ok=True)

# Define the complete file path for the log file
LOG_FILEPATH = os.path.join(log_path, LOG_FILE)

# Configure the logging settings
logging.basicConfig(
    level=logging.INFO,  # Set the logging level to INFO
    filename=LOG_FILEPATH,  # Log output file path
    format="[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s"  # Log message format
)

# Example use case
# if __name__ == "__main__":
#     logging.info("Logging Has started.")
