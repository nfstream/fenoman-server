import pandas
from nfstream import NFStreamer
from configuration.nfstream_configuration import *
import logging


class Capturer:
    def __init__(self,
                 source: str = SOURCE,
                 statistical_analysis: bool = STATISTICAL_ANALYSIS,
                 splt_analysis: int = SPLT_ANALYSIS,
                 max_nflows: int = MAX_NFLOWS) -> None:
        """
        This class is responsible for monitoring the network traffic with NFStreamer in case the user has not specified
        which CSV to run the training from or it does not exist.

        :param source: Packet capture source. Pcap file path, List of pcap files path (considered as a single file) or
        network interface name.
        :param statistical_analysis: 	Enable/Disable post-mortem flow statistical analysis.
        :param splt_analysis: 	Specify the sequence of first packets length for early statistical analysis. When set to
        0, splt_analysis is disabled.
        :param max_nflows: Specify the number of maximum flows to capture before returning. Unset when equal to 0.
        :return: None
        """
        self.__source = source
        self.__statistical_analysis = statistical_analysis
        self.__splt_analysis = splt_analysis
        self.__max_nflows = max_nflows

        logging.debug('CAPTURER: Starting network monitoring.')
        logging.info(f'CAPTURER: Capturing {self.__max_nflows} flows.')
        self.__nsftreamer = NFStreamer(
            source=self.__source,
            statistical_analysis=self.__statistical_analysis,
            splt_analysis=self.__splt_analysis,
            max_nflows=self.__max_nflows
        )
        logging.info('CAPTURER: Finished capturing!')

    def generate_export(self,
                        columns_to_anonymize: list = COLUMNS_TO_ANONYMIZE) -> pandas.DataFrame:
        """
        This function can be used to produce the pandas dataframe with the monitored content.

        :param columns_to_anonymize :List of columns names to anonymize. Anonymization is based on a random secret key
        generation at each start of NFStreamer. The generated key is used to anonymize configured values using blake2b
        algorithm.
        :return: Pandas DateFrame containing the generated data
        """
        logging.debug('CAPTURER: Generating pandas dataframe export.')
        self.__columns_to_anonymize = columns_to_anonymize
        self.__generated_dataframe = self.__nsftreamer.to_pandas(
            columns_to_anonymize=self.__columns_to_anonymize
        )
        return self.__generated_dataframe
