from configuration.application_configuration import OCP_APIM_KEY
from typing import Tuple
import logging


class Authenticator:
    @staticmethod
    def check_api_key(api_key: str) -> Tuple[str, bool]:
        """
        This is a simple authentication class that just compares the input api key with the one in the configuration.

        :param api_key: input api key which must be compared to the actual one
        :return: str state response, bool of the success
        """
        logging.debug('AUTHENTICATOR: Checking API key.')
        if api_key == OCP_APIM_KEY:
            return 'OK', True
        else:
            return 'Wrong API key.', False


logging.debug('AUTHENTICATOR: Creating an instance of authenticator class.')
authenticator = Authenticator()
logging.debug('AUTHENTICATOR: Created instance of authenticator class.')
