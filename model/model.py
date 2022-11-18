from configuration.model_configuration import *
from sklearn.preprocessing import LabelEncoder
from typing import Any
from data.data import data
from database.nosql_database import nosql_database
import pickle


class Model:
    def __init__(self, model_name: str) -> None:
        """
        The model class is a wrapper class that contains a Keras-based instance. Currently, the solution only supports
        the direct implementation of the model, which is defined in the next block.

        :return: None
        """
        self.__model_name = model_name

        # Checking if model exists in database
        records, state = nosql_database.last_n_element(
            search_field={
                'model_name': self.__model_name
            },
            key='timestamp',
            limit=1)

        if state:
            print("loading model in Model class from mongodb")
            self.__model = pickle.loads(records[0]['model'])
        else:
            module = __import__(f'temp.{self.__model_name}')
            external_model_class = getattr(module, 'ExternalModel')
            self.__model = external_model_class.get_model()

            x_train, y_train, x_val, y_val = data.load_data()

            lb = LabelEncoder()

            y_val = lb.fit_transform(y_val)
            y_train = lb.fit_transform(y_train)
            self.__history = self.__model.fit(
                x_train,
                y_train,
                batch_size=MODEL_BATCH_SIZE,
                epochs=MODE_EPOCHS,
                # We pass some validation for
                # monitoring validation loss and metrics
                # at the end of each epoch
                validation_data=(x_val, y_val),
            )

        self.save_model()

    def get_model_name(self) -> str:
        return self.__model_name

    def __call__(self) -> Any:
        """
        This __call__ method used to call directly the underlying keras model. This allows the developer to use the
        built-in keras functions if the Model object is called like model().

        :return: Keras Model
        """
        return self.__model

    def save_model(self) -> None:
        """
        Function used to save the model to a local folder.

        :return: None
        """
        self.__model.save(
            f'model/temp/{MODEL_NAME}.h5',
            overwrite=True
        )

    @staticmethod
    def get_health_state() -> bool:
        """
        Returns the status of the class.

        :return: state of health status
        """
        return True


models = {}
for model_name in MODEL_NAME:
    models[model_name] = Model(model_name=model_name)
