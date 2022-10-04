import tensorflow as tf
import flwr as fl
# from patterns.singleton import singleton
from typing import Any
from data.data import data
import numpy as np
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.metrics import classification_report, confusion_matrix, f1_score, precision_score, recall_score
import matplotlib.pyplot as plt
from configuration.data_configuration import TEST_DATAFRAME


#@singleton
class Model:
    def __init__(self) -> None:
        # TODO majd ezt meg kell csinálni, hogy ha most lett compilolva akkor 1x tanítani kell, ha már meglévőt szeretnénk
        #   haszánlni akkor az nem szükséges az adatbázisból majd ezt is le kell tölteni!
        self.__model = tf.keras.Sequential()
        self.__model.add(tf.keras.layers.Dense(13, input_dim=13, activation='relu'))
        self.__model.add(tf.keras.layers.Dense(200, activation='relu'))
        self.__model.add(tf.keras.layers.Dense(171, activation='softmax'))

        self.__model.compile("adam", "sparse_categorical_crossentropy", metrics=["accuracy"])

        x_train, y_train, x_val, y_val = data.load_data()
        #print(len(x_train), len(y_train), len(x_val), len(y_val))

        self.__history = self.__model.fit(
            x_train,
            y_train,
            batch_size=64,
            epochs=1,
            # We pass some validation for
            # monitoring validation loss and metrics
            # at the end of each epoch
            validation_data=(x_val, y_val),
        )

        predictions = self.__model.predict(x_val)
        predictions = np.argmax(predictions, axis=1).tolist()

        #y_true = np.argmax(y_val, axis=1).tolist()
        y_true = y_val.astype(int).tolist()

        matrix = confusion_matrix(y_true, predictions, normalize="true")

        print('Confusion Matrix')
        print(matrix)
        print(classification_report(y_val, predictions))

        print("precision: " + str(precision_score(y_val, predictions, average="weighted")))
        print("recall: " + str(recall_score(y_val, predictions, average="weighted")))
        print("f1: " + str(f1_score(y_val, predictions, average="weighted")))

        labels = ["BitTorrent", "NTP", "NetBIOS.SMBv", "RDP", "SSH"]
        disp = ConfusionMatrixDisplay(confusion_matrix=matrix, display_labels=labels)
        disp.plot(cmap=plt.cm.Blues)
        plt.show()

    def __call__(self) -> Any:
        return self.__model

    def save_model(self) -> None:
        self.__model.save('/model/temp/')


model = Model()
