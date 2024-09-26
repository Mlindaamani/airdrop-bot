import logging


class Logger:
    """
    This class is used to log the messages to the file.
    The class has the following methods:
    1. log_info: This method is used to log the info messages.
    2. log_debug: This method is used to log the debug messages.
    3. log_warning: This method is used to log the warning messages.
    4. log_error: This method is used to log the error messages.
    5. __init__: This method is used to initialize the logger

    """

    def __init__(self, name, level=logging.INFO):

        self.logger = logging.getLogger(name)

        self.logger.setLevel(level)

        formatter = logging.Formatter(
            "%(asctime)s - %(levelname)s - %(message)s")

        file_handler = logging.FileHandler(filename=name)

        file_handler.setFormatter(formatter)

        self.logger.addHandler(file_handler)

    def log_info(self, message=None):
        self.logger.info(message)

    def log_debug(self, message=None):
        self.logger.debug(message)

    def log_warning(self, message=None):
        self.logger.warning(message)

    def log_error(self, message=None):
        self.logger.error(message)
