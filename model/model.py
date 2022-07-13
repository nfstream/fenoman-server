import tensorflow as tf
import flwr as fl
from patterns.singleton import singleton
from typing import Any


@singleton
class Model:
    def __init__(self):
        # laod here the given model, it must be universal
        self.__model = None

    def __call__(self) -> Any:
        return self.__model


model = Model()
