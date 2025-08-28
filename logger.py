import logging
import sys

def configure_application_logging(log_level, log_file, logging_format):
    """
    Configures the root logger for the entire application.
    """
    # Get the root logger
    # This is crucial: logging.getLogger() with no arguments returns the root logger.
    logger = logging.getLogger() 

    # Set the global logging level. Messages below this level will be ignored.
    logger.setLevel(log_level)

    # Clear existing handlers to prevent duplicate output if this function is called multiple times.
    # This is a good practice for robust reconfiguration.
    if logger.handlers:
        for handler in list(logger.handlers): # Iterate over a copy in case handlers are removed during iteration
            logger.removeHandler(handler)
            handler.close() # Important to close file handlers to release resources

    # Create a formatter with your desired format
    formatter = logging.Formatter(logging_format)

    # Create and configure the FileHandler
    file_handler = logging.FileHandler(log_file)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Create and configure the StreamHandler (for console output)
    # Using sys.stdout is fine, sys.stderr is also common for warnings/errors.
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    logger.info("Logger configured successfully.")
