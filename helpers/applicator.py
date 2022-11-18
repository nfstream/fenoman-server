from helpers.argumenter import argumenter
from helpers.authenticator import authenticator
from flask import Response
from typing import Union, Tuple
import logging


class Applicator:
    @staticmethod
    def headers(arguments: list, keys: list) -> Tuple[Union[Response, None], bool]:
        """
        During http calls, this class unifies the error codes in case a parameter or key is missing.

        :param arguments: list of arguments that are required in the given call
        :param keys: actual keys that appears in the call
        :return: tuple of success as a bool and a Response object
        """
        logging.debug('APPLICATOR: Checking headers.')
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
        :return: tuple of success as a bool and a Response object
        """
        logging.debug('APPLICATOR: Checking authentication.')
        authentication_msg, authentication_state = authenticator.check_api_key(api_key)
        if not authentication_state:
            return Response(authentication_msg, 401), False
        return None, True


logging.debug('APPLICATOR: Creating an instance of applicator class.')
applicator = Applicator()
logging.debug('APPLICATOR: Created instance of applicator class.')
