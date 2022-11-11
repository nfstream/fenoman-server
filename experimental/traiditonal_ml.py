import tensorflow as tf
import flwr as fl
from typing import Any
from data.data import data
from keras import backend as K


def recall_m(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    possible_positives = K.sum(K.round(K.clip(y_true, 0, 1)))
    recall = true_positives / (possible_positives + K.epsilon())
    return recall


def precision_m(y_true, y_pred):
    true_positives = K.sum(K.round(K.clip(y_true * y_pred, 0, 1)))
    predicted_positives = K.sum(K.round(K.clip(y_pred, 0, 1)))
    precision = true_positives / (predicted_positives + K.epsilon())
    return precision


def f1_m(y_true, y_pred):
    precision = precision_m(y_true, y_pred)
    recall = recall_m(y_true, y_pred)
    return 2*((precision*recall)/(precision+recall+K.epsilon()))


def main():
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.Dense(13, input_dim=13, activation='relu'))
    model.add(tf.keras.layers.Dense(200, activation='relu'))
    model.add(tf.keras.layers.Dense(171, activation='softmax'))

    model.compile("adam", "sparse_categorical_crossentropy", metrics=["accuracy",f1_m,precision_m, recall_m])

    x_train, y_train, x_val, y_val = data.load_data()

    history = model.fit(
                x_train,
                y_train,
                batch_size=64,
                epochs=2,
                # We pass some validation for
                # monitoring validation loss and metrics
                # at the end of each epoch
                validation_data=(x_val, y_val),
            )

    print(f'loss: {history.history["loss"]}')
    print(f'accuracy: {history.history["accuracy"]}')
    print(history.history)

    #with open("traditional_ml_output.txt", "w") as f:
    #    f.write(f'loss: {history.history["loss"]}\n')
    #    f.write(f'accuracy: {history.history["accuracy"]}')


if __name__ == '__main__':
    main()
