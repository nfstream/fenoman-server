from flask import Flask, Response
from core.core import Core
import timeloop
from datetime import timedelta
from configuration.flower_configuration import SERVER_JOB_TIMER_MINUTES
import logging
from configuration.application_configuration import *


app = Flask(__name__)
core = Core()
tl = timeloop.Timeloop()


@tl.job(interval=timedelta(minutes=SERVER_JOB_TIMER_MINUTES))
def start_fl_server():
    logging.info("Starting Flower server.")
    core.start_server()


@app.route(f'{BASE_URI}/health', methods=["GET", "POST"])
def default_route() -> Response:
    return Response("OK", status=200)


# TODO
def get_avilable_models():
    # lista az elérhető modellekről
    pass


@app.route(f'{BASE_URI}/get_model/<model_name>', methods=["GET"])
def get_latest_model(model_name: str):
    # a legújabb model leküldése a kliens számára
    pass


tl.start(block=False)
if __name__ == '__main__':
    app.run()
