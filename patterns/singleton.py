from typing import Any


def singleton(class_: Any) -> Any:
    """
    This is the singleton pattern, which is a software design pattern that restricts the instantiation of a class to
    one single instance. This is useful when exactly one object is needed to coordinate actions across the system.
    :param class_: any class type
    :return: none
    """
    __instances = {}

    def get_instance(*args: Any, **kwargs: Any) -> Any:
        """
        This function checks if there are any instances registered in the dictionary if not it will return a new
        instances of a class.
        :rtype Any
        :param args: non-keyword arguments
        :param kwargs: keyword arguments
        :return: Any class instances
        """
        if class_ not in __instances:
            __instances[class_] = class_(*args, **kwargs)
        return __instances[class_]

    return get_instance
