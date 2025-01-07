import sys
import traceback

class CustomException(Exception):
    def __init__(self, error_message, error_detail:sys):
        self.error_message = self.error_message_detail(error_message, error_detail)
        super().__init__(self.error_message)

    @staticmethod
    def error_message_detail(error_message, error_detail:sys):
        # Extracting details from the error traceback
        _, _, exc_tb = error_detail.exc_info()
        filename = exc_tb.tb_frame.f_code.co_filename
        line_number = exc_tb.tb_lineno
        function_name = exc_tb.tb_frame.f_code.co_name

        # Constructing the error message
        error_message_detail = f"Error occurred in script: [{filename}], function: [{function_name}], line number: [{line_number}] with message: {error_message}"
        return error_message_detail



