import logging
import os
from datetime import datetime

# Create the logs directory if it doesn't exist
logs_path = os.path.join(os.getcwd(), "logs")
os.makedirs(logs_path, exist_ok=True)

# Generate a timestamped log file name
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)

# Setting up the logging configuration
logging.basicConfig(
    filename=LOG_FILE_PATH,  # The log file to which logs will be written
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",  # Log format
    level=logging.INFO  # Logging level set to INFO
)

# Console logging configuration
console_handler = logging.StreamHandler()
console_handler.setFormatter(logging.Formatter("[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s"))
console_handler.setLevel(logging.INFO)

# Add the console handler to the root logger
logging.getLogger().addHandler(console_handler)

# Example to use the logger
logging.info("Logger setup complete.")
