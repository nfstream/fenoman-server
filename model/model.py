import tensorflow as tf
import flwr as fl
from patterns.singleton import singleton


@singleton
class Model:
    def __init__(self):
        # laod here the given model, it must be universal
        self.__model = None
        self.__strategy = fl.server.strategy.FedAvh(

        )

    def __call__(self) -> tf.model:
        return self.__model
