import tensorflow as tf


def get_model() -> tf.keras.Sequential:
    model = tf.keras.Sequential()
    model.add(tf.keras.layers.Dense(13, input_dim=13, activation='relu'))
    model.add(tf.keras.layers.Dense(200, activation='relu'))
    model.add(tf.keras.layers.Dense(500, activation='softmax'))
    model.compile("adam", "sparse_categorical_crossentropy", metrics=["accuracy"])

    return model
