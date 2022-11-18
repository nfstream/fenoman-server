from typing import Tuple
import logging


class Argumenter:
    @staticmethod
    def check_arguments(arguments: list, keys: list) -> Tuple[str, bool]:
        """
        This class checks whether the given function has received all the arguments in the list, in case any of them are
        missing it produces the output string.

        :param arguments: predefined http header list
        :param keys: list of keys received in http request
        :return: Output message and a status integer
        """
        logging.debug('ARGUMENTER: Checking arguments.')
        missing_arguments = []
        for argument in arguments:
            if argument not in keys:
                missing_arguments.append(argument)

        if len(missing_arguments) > 0:
            return f'Missing call parameters, the following fields are missing: {",".join(missing_arguments)}', False
        else:
            return 'OK', True


logging.debug('ARGUMENTER: Creating an instance of argumenter class.')
argumenter = Argumenter()
logging.debug('ARGUMENTER: Created instance of argumenter class.')
