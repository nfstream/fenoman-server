from app import app
from configuration.application_configuration import *
import logging


if __name__ == "__main__":
    logging.getLogger().setLevel(logging.DEBUG)

    from waitress import serve
    logging.info('WSGI: Starting FeNOMan server.')
    serve(app, host=HOST_URI, port=HOST_PORT)
