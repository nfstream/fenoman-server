from flask import Flask
import database as db

app = Flask(__name__)


@app.route("/")
def test():
    return "<p> This is a test message </p>"

@app.route("/get/model/<version>")
def get_model(version):
    #This will be a security issue when we will use a real database
    return db.modelDB.get_data(version)
