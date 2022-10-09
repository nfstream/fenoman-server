from helpers.argumenter import argumenter
from helpers.authenticator import authenticator
from flask import Response
from typing import Union, Tuple


class Applicator:
    @staticmethod
    def headers(arguments: list, keys: list) -> Tuple[Union[Response, None], bool]:
        """
        During http calls, this class unifies the error codes in case a parameter or key is missing.

        :param arguments: list of arguments that are required in the given call
        :param keys: acutal keys that appears in the call
        :return:
        """
        argumenter_msg, argumenter_state = argumenter.check_arguments(
            arguments=arguments,
            keys=keys
        )
        if not argumenter_state:
            return Response(argumenter_msg, 406), False
        return None, True

    @staticmethod
    def authentication(api_key: str) -> Tuple[Union[Response, None], bool]:
        """
        This function uniformly handles error messages for the existence of the api key.

        :param api_key: api key provided in the http call
        :return:
        """
        authentication_msg, authentication_state = authenticator.check_api_key(api_key)
        if not authentication_state:
            return Response(authentication_msg, 401), False
        return None, True


applicator = Applicator()