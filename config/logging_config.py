# config/logging_config.py

import logging
import sys

# Define a format for log messages
LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

# Define a formatter
formatter = logging.Formatter(LOG_FORMAT)

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)  # Set the default logging level

# Create a handler for console output
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setFormatter(formatter)

# Add the console handler to the logger
logger.addHandler(console_handler)

# You can add more handlers here, e.g., for file logging
# file_handler = logging.FileHandler('app.log')
# file_handler.setFormatter(formatter)
# logger.addHandler(file_handler)

def setup_logging():
    """Sets up centralized logging for the application."""
    # The logger and handlers are already configured above.
    # This function can be used to perform more complex setup if needed,
    # or to reconfigure logging at runtime.
    logging.basicConfig(level=logging.INFO, format=LOG_FORMAT, handlers=[console_handler])
    logger.info("Logging configured successfully.")

