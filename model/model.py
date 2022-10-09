import tensorflow as tf
from sklearn.preprocessing import LabelEncoder
from configuration.model_configuration import *

from patterns.singleton import singleton
from typing import Any
from data.data import data


@singleton
class Model:
    def __init__(self) -> None:
        """
        The model class is a wrapper class that contains a Keras-based instance. Currently, the solution only supports
        the direct implementation of the model, which is defined in the next block.

        :return: None
        """
        ### Internal model definition block. ###
        '''
        TODO ezt a jövőben tovább kell fejleszteni, hogy akármilyen modelt be lehessen nyomni ne csak igy!
        '''
        self.__model = tf.keras.Sequential()
        self.__model.add(tf.keras.layers.Dense(13, input_dim=13, activation='relu'))
        self.__model.add(tf.keras.layers.Dense(200, activation='relu'))
        self.__model.add(tf.keras.layers.Dense(171, activation='softmax'))
        self.__model.compile("adam", "sparse_categorical_crossentropy", metrics=["accuracy"])
        ### Internal model definition block. ###

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
        self.__save_model()

    def __call__(self) -> Any:
        """
        This __call__ method used to call directly the underlying keras model. This allows the developer to use the
        built-in keras functions if the Model object is called like model().

        :return: Keras Model
        """
        return self.__model

    def __save_model(self) -> None:
        """
        Function used to save the model to a local folder.

        :return: None
        """
        self.__model.save(f'model/temp/{MODEL_NAME}.h5')

    @staticmethod
    def get_health_state() -> bool:
        """
        Returns the status of the class.

        :return: state of health status
        """
        return True


model = Model()
