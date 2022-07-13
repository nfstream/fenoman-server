from flask import Flask
from core.core import Core


app = Flask(__name__)
core = Core()


@app.route('/', methods=["GET", "POST"])
def default_route() -> str: 
    return "200"


if __name__ == '__main__':
    app.run()
