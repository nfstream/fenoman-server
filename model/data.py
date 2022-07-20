from typing import Any
from patterns.singleton import singleton


@singleton
class Data:
    # TODO DATA CLASS for evaluation
    def __init__(self) -> None:
        self.__data = None

    def __call__(self, *args, **kwargs) -> Any:
        return self.__data


data = Data()
