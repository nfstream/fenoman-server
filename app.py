from flask import Flask, Response, send_file, request
from core.core import Core
import timeloop
from datetime import timedelta
from configuration.flower_configuration import SERVER_JOB_TIMER_MINUTES
import logging
from configuration.application_configuration import *
from configuration.model_configuration import *
from helpers.applicator import applicator
from model.model import model


app = Flask(__name__)
tl = timeloop.Timeloop()
core = None


@tl.job(interval=timedelta(minutes=SERVER_JOB_TIMER_MINUTES))
def start_fl_server() -> None:
    """
    This is an automatic function which is important to incrementally start the flower server and do the teaching. You
    can control the increment based on the timer. It is important to note that synchronous startup of the teaching
    server cannot run two at the same time, so the system schedules this automatically. In case of a backlog, the next
    one will start automatically after the termination of a flower server.

    :return: None
    """
    global core

    core = Core()
    logging.info("Starting Flower server.")
    core.start_server()

    del core


tl.start(block=False)


@app.route(f'{BASE_URI}/healthz', methods=["GET"])
def default_route() -> Response:
    """
    This is an endpoint to support docker containerization health status.

    :return: Response object of the success state
    """
    if core is None:
        return Response("Init in progress", status=100)

    if core.get_health_state():
        return Response("OK", status=200)
    else:
        return Response("Internal error.", status=500)


@app.route(f'{BASE_URI}/get_available_models', methods=["GET"])
def get_available_models() -> Response:
    """
    The databases available on the server can be queried using this procedure.

    :return: Response object with data.
    """
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
    """
    The latest version of the named model can be downloaded from the server using this endpoint.

    :param model_name: model name that must be downloaded
    :return: Response object with model data
    """
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
        model.save_model()
        return send_file(path_or_file=f"model/temp/{MODEL_NAME}.h5")
    else:
        return Response('Given model name is not available on the server.', 404)
