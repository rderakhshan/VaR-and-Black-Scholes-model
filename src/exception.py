import os
import sys

# Add the project's root directory to sys.path to enable importing from 'src'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from src.logger import logging

def error_message_detail(error, error_detail: sys) -> str:
    """
    Generates a detailed error message including the file name, line number, and error message.

    Args:
        error (Exception): The exception object that was raised.
        error_detail (sys): The system module to access exception details.

    Returns:
        str: A formatted string containing the detailed error message with the script name, line number, and error message.
    """
    # Get the traceback information
    _, _, exc_tb = error_detail.exc_info()

    # Extract file name and line number from traceback
    file_name = exc_tb.tb_frame.f_code.co_filename
    line_number = exc_tb.tb_lineno

    # Construct a formatted error message
    error_message = "Error occurred in python script name [{0}] line number [{1}] error message[{2}]".format(
        file_name, line_number, str(error)
    )

    return error_message

class CustomException(Exception):
    """
    Custom exception class that extends the built-in Exception class to provide more detailed error messages.

    Attributes:
        error_message (str): Detailed error message generated for the exception.
    """

    def __init__(self, error_message: Exception, error_detail: sys):
        """
        Initializes the CustomException class with an error message and error details.

        Args:
            error_message (Exception): The original exception object.
            error_detail (sys): The system module to access exception details for generating the error message.
        """
        # Initialize the base Exception class with the error message
        super().__init__(error_message)

        # Generate a detailed error message
        self.error_message = error_message_detail(error_message, error_detail=error_detail)

    def __str__(self) -> str:
        """
        Returns the detailed error message when the exception is converted to a string.

        Returns:
            str: The detailed error message.
        """
        return self.error_message

# # Example use case
# if __name__ == "__main__":
#     try:
#         a = 1 / 0  # This will raise a ZeroDivisionError
#     except Exception as e:
#         logging.info("Divided by zero!")  # Log the error information
#         raise CustomException(e, sys)  # Raise the CustomException with error details
