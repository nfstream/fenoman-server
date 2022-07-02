import database
import application

class Core:
    def __init__(self):
        application.app.run(port=1234)

    def load_models(self, model):
        return database.modelDB.get_data(model)

core = Core()
