import logging

def get_logger(logger_name: str, file_name: str = "default.log", log_level: int = logging.DEBUG) -> logging.Logger:
    """
    Creates and returns a logger.

    Args:
        logger_name (str): Name of the logger.
        file_name (str): File where logs will be written. Defaults to 'default.log'.
        log_level (int): Logging level. Defaults to logging.DEBUG.

    Returns:
        logging.Logger: Configured logger instance.
    """
    # Create or retrieve the logger
    logger = logging.getLogger(logger_name)
    logger.setLevel(log_level)

    # Check if the logger already has handlers to avoid duplicate logs
    if not logger.handlers:
        # Create file handler to write logs to a file
        file_handler = logging.FileHandler(file_name)
        file_handler.setLevel(log_level)

        # Create formatter for the log messages
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(formatter)

        # Add the file handler to the logger
        logger.addHandler(file_handler)

    return logger