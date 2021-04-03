
import logging
import logging.handlers

def get_logger(name, file_name=None):
    LOG_FILENAME = file_name if file_name else name + '.log'
    # Set up a specific logger with our desired output level

    my_logger = logging.getLogger(name)
    # Add the log message handler to the logger

    if not my_logger.handlers:
        handler = logging.handlers.RotatingFileHandler(LOG_FILENAME,
                                                      maxBytes=10000000,
                                                      backupCount=5,
                                                      )
        formatter = logging.Formatter("[%(asctime)s] [%(filename)s:%(lineno)s - %(funcName)5s() - %(processName)s] %(levelname)s - %(message)s")
        handler.setFormatter(formatter)
        my_logger.addHandler(handler)

    return my_logger