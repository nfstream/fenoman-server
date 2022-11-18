from flask import Flask, Response, send_file, request
import timeloop
from datetime import timedelta
from configuration.flower_configuration import SERVER_JOB_TIMER_MINUTES, FLOWER_SERVER_PORT
from configuration.application_configuration import *
from configuration.model_configuration import *
from helpers.applicator import applicator
from model.model import models
import subprocess
import logging


app = Flask(__name__)
tl = timeloop.Timeloop()
core = None


def flower_server_scheduling() -> None:
    @tl.job(interval=timedelta(minutes=SERVER_JOB_TIMER_MINUTES))
    def __start_fl_server(model_name: str, flower_server_port: str) -> None:
        """
        This is an automatic function which is important to incrementally start the flower server and do the teaching. You
        can control the increment based on the timer. It is important to note that synchronous startup of the teaching
        server cannot run two at the same time, so the system schedules this automatically. In case of a backlog, the next
        one will start automatically after the termination of a flower server.

        :return: None
        """
        subprocess.call(f'python3 ./core/core.py --model_name {model_name} --port {flower_server_port}', shell=True)

    for model_name, flower_server_port in zip(MODEL_NAME, FLOWER_SERVER_PORT):
        __start_fl_server(
            model_name=model_name,
            flower_server_port=flower_server_port
        )
        tl.start(block=False)


flower_server_scheduling()


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
    logging.debug('APP: Client requesting available models.')
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

    response_data = {
        'models': MODEL_NAME,
        'ports': FLOWER_SERVER_PORT
    }
    logging.debug('APP: Returning available models.')
    return Response(response_data, 200)


@app.route(f'{BASE_URI}/get_model/<model_name>', methods=["GET"])
def get_latest_model(model_name: str) -> Response:
    """
    The latest version of the named model can be downloaded from the server using this endpoint.

    :param model_name: model name that must be downloaded
    :return: Response object with model data
    """
    logging.debug('APP: Client requesting model.')
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

    if model_name in models.keys():
        models[model_name].save_model()
        logging.debug('APP: Returning model to the client.')
        return send_file(path_or_file=f"model/temp/{models[model_name].get_model_name()}.h5")
    else:
        logging.debug('APP: Given model name is not available on the server.')
        return Response('Given model name is not available on the server.', 404)
