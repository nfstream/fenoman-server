from json import dumps
from flask import Flask, Response, send_file, make_response, request
from core.core import Core
import timeloop
from datetime import timedelta
from configuration.flower_configuration import SERVER_JOB_TIMER_MINUTES
import logging
from configuration.application_configuration import *
from helpers.argumenter import argumenter
from helpers.authenticator import authenticator


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
    argumenter_msg, argumenter_state = argumenter.check_arguments(
        arguments=['Ocp-Apim-Key'],
        keys=[*[str(x) for x in request.headers.keys()], *request.values.keys()]
    )
    if not argumenter_state:
        return Response(argumenter_msg, 406)

    authentication_msg, authentication_state = authenticator.check_api_key(request.headers['Ocp-Apim-Key'])
    if not authentication_state:
        return Response(authentication_msg, 401)

    # TODO nem jó igy a beégetett név azonos kell legyen a modell_configból!
    # lista az elérhető modellekről
    models = []
    models.append("classification")
    return make_response(dumps(models))


@app.route(f'{BASE_URI}/get_model/<model_name>', methods=["GET"])
def get_latest_model(model_name: str) -> Response:
    argumenter_msg, argumenter_state = argumenter.check_arguments(
        arguments=['Ocp-Apim-Key', 'model_name'],
        keys=[*[str(x) for x in request.headers.keys()], *request.values.keys()]
    )
    if not argumenter_state:
        return Response(argumenter_msg, 406)

    authentication_msg, authentication_state = authenticator.check_api_key(request.headers['Ocp-Apim-Key'])
    if not authentication_state:
        return Response(authentication_msg, 401)

    # TODO ez hogy kerül ez a model ide ? meg ez a staticus beégetett model név geci szar
    if model_name == "classification":
        return send_file(path_or_file="model/temp/classification.h5")
    # a legújabb model leküldése a kliens számára
    pass
