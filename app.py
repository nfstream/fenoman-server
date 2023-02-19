import json
import socket
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


@tl.job(interval=timedelta(minutes=SERVER_JOB_TIMER_MINUTES))
def flower_server_scheduling() -> None:
    """
    This is an automatic function which is important to incrementally start the flower server and do the teaching. You
    can control the increment based on the timer. It is important to note that synchronous startup of the teaching
    server cannot run two at the same time, so the system schedules this automatically. In case of a backlog, the next
    one will start automatically after the termination of a flower server.

    :return: None
    """
    for model_name, flower_server_port in zip(MODEL_NAME, FLOWER_SERVER_PORT):
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock_state = sock.connect_ex(('127.0.0.1', int(flower_server_port)))
        init_process_state = False
        # If socket is open then skip the init
        if sock_state != 0:
            init_process_state = True
        sock.close()

        if init_process_state:
            subprocess.Popen(f'python ./core/core.py --model_name {model_name} --port {flower_server_port}',
                             shell=True,
                             start_new_session=True)


@app.route(f'{BASE_URI}/healthz', methods=["GET"])
def default_route() -> Response:
    """
    This is an endpoint to support docker containerization health status.

    :return: Response object of the success state
    """
    return Response("OK", status=200)


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
    return Response(json.dumps(response_data), 200)


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


tl.start(block=False)
