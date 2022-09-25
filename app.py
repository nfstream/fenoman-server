from json import dumps

from flask import Flask, Response, send_file, make_response
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


@app.route(f'{BASE_URI}/get_avilable_models', methods=["GET"])
def get_avilable_models():
    # lista az elérhető modellekről
    models = []
    models.append("classification")
    return make_response(dumps(models))


@app.route(f'{BASE_URI}/get_model/<model_name>', methods=["GET"])
def get_latest_model(model_name: str):
    if model_name == "classification":
        return send_file(path_or_file="model/temp/classification.h5")
    # a legújabb model leküldése a kliens számára
    pass


tl.start(block=False)
if __name__ == '__main__':
    app.run()
