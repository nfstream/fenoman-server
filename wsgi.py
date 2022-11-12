from app import app
from configuration.application_configuration import *


if __name__ == "__main__":
    from waitress import serve
    serve(app, host=HOST_URI, port=HOST_PORT)
