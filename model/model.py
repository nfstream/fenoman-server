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


        :return: None
        """

        # TODO majd ezt meg kell csinálni, hogy ha most lett compilolva akkor 1x tanítani kell, ha már meglévőt szeretnénk
        #   haszánlni akkor az nem szükséges az adatbázisból majd ezt is le kell tölteni!
        self.__model = tf.keras.Sequential()
        self.__model.add(tf.keras.layers.Dense(13, input_dim=13, activation='relu'))
        self.__model.add(tf.keras.layers.Dense(200, activation='relu'))
        self.__model.add(tf.keras.layers.Dense(171, activation='softmax'))
        self.__model.compile("adam", "sparse_categorical_crossentropy", metrics=["accuracy"])
        # TODO ezt hogy lehet univerzálissá tenni?



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

    def __call__(self) -> Any:
        """
        This __call__ method used to call directly the underlaying keras model. This allows the developer to use the
        built-in keras functions if the Model object is called like model().

        :return: Keras Model
        """
        return self.__model

    def save_model(self) -> None:
        """


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
