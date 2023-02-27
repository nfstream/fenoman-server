import sys
from app import app
from configuration.application_configuration import *
import logging
from configuration.application_configuration import LOGGING_LEVEL, LOGGING_FORMATTER


if __name__ == "__main__":
    logger_root = logging.getLogger()
    logger_root.setLevel(getattr(logging, LOGGING_LEVEL))
    logger_handler = logging.StreamHandler(sys.stdout)
    logger_handler.setLevel(getattr(logging, LOGGING_LEVEL))
    logger_formatter = logging.Formatter(LOGGING_FORMATTER)
    logger_handler.setFormatter(logger_formatter)
    logger_root.addHandler(logger_handler)

    from waitress import serve
    logging.info('WSGI: Starting FeNOMan server.')
    serve(app, host=HOST_URI, port=HOST_PORT)
