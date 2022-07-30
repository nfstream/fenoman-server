from flask import Flask
from core.core import Core
import timeloop
from datetime import timedelta
from configuration.flower_configuration import SERVER_JOB_TIMER_MINUTES


app = Flask(__name__)
core = Core()
tl = timeloop.Timeloop()


@tl.job(interval=timedelta(minutes=SERVER_JOB_TIMER_MINUTES))
def start_fl_server():
    print("Starting Flower server.")
    core.start_server()


@app.route('/', methods=["GET", "POST"])
def default_route() -> str: 
    return "200"


# TODO
def get_avilable_models():
    # lista az elérhető modellekről
    pass


def get_latest_model(name: str):
    # a legújabb model leküldése a kliens számára
    pass


tl.start(block=False)
if __name__ == '__main__':
    app.run()
