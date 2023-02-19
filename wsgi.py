import sys
from app import app
from configuration.application_configuration import *
import logging


if __name__ == "__main__":
    # TODO argparse logg level setter in environment variable
    logger_root = logging.getLogger()
    logger_root.setLevel(logging.DEBUG)
    logger_handler = logging.StreamHandler(sys.stdout)
    logger_handler.setLevel(logging.DEBUG)
    logger_formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logger_handler.setFormatter(logger_formatter)
    logger_root.addHandler(logger_handler)

    from waitress import serve
    logging.info('WSGI: Starting FeNOMan server.')
    serve(app, host=HOST_URI, port=HOST_PORT)
