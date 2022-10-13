from flask import Flask, Response, send_file, request
from core.core import Core
import timeloop
from datetime import timedelta
from configuration.flower_configuration import SERVER_JOB_TIMER_MINUTES
import logging
from configuration.application_configuration import *
from configuration.model_configuration import *
from helpers.applicator import applicator


app = Flask(__name__)
core = Core()
tl = timeloop.Timeloop()


@tl.job(interval=timedelta(minutes=SERVER_JOB_TIMER_MINUTES))
def start_fl_server():
    logging.info("Starting Flower server.")
    core.start_server()


tl.start(block=False)


@app.route(f'{BASE_URI}/healthz', methods=["GET"])
def default_route() -> Response:
    if core.get_health_state():
        return Response("OK", status=200)
    else:
        return Response("Internal error.", status=500)


@app.route(f'{BASE_URI}/get_available_models', methods=["GET"])
def get_available_models() -> Response:
    header_resp, header_state = applicator.headers(
        ['Ocp-Apim-Key'],
        [*[str(x) for x in request.headers.keys()], *request.values.keys()]
    )
    if not header_state:
        return header_resp

    auth_resp, auth_state = applicator.authentication(
        request.headers['Ocp-Apim-Key']
    )
    if not auth_state:
        return auth_resp

    return Response(MODEL_NAME, 200)


@app.route(f'{BASE_URI}/get_model/<model_name>', methods=["GET"])
def get_latest_model(model_name: str) -> Response:
    header_resp, header_state = applicator.headers(
        ['Ocp-Apim-Key'],
        [*[str(x) for x in request.headers.keys()], *request.values.keys()]
    )
    if not header_state:
        return header_resp

    auth_resp, auth_state = applicator.authentication(
        request.headers['Ocp-Apim-Key']
    )
    if not auth_state:
        return auth_resp

    if model_name == MODEL_NAME:
        return send_file(path_or_file=f"model/temp/{MODEL_NAME}.h5")
