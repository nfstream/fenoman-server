from app import app
from configuration.application_configuration import *
import logging


if __name__ == "__main__":
    from waitress import serve
    logging.info('Starting FeNOMan server.')
    serve(app, host=HOST_URI, port=HOST_PORT)
