import pandas
from nfstream import NFStreamer
from configuration.nfstream_configuration import *


class TimerPlugin(object):
    def __init__(self, **kwargs):
        """
        NFPlugin Parameters:
        kwargs : user defined named arguments that will be stored as Plugin attributes
        """
        for key, value in kwargs.items():
            setattr(self, key, value)

    def on_init(self, packet, flow):
        """
        on_init(self, packet, flow): Method called at flow creation.
        You must initiate your udps values if you plan to compute ones.
        Example: -------------------------------------------------------
                 flow.udps.magic_message = "NO"
                 if packet.raw_size == 40:
                    flow.udps.packet_40_count = 1
                 else:
                    flow.udps.packet_40_count = 0
        ----------------------------------------------------------------
        """

    def on_update(self, packet, flow):
        """
        on_update(self, packet, flow): Method called to update each flow
                                       with its belonging packet.
        Example: -------------------------------------------------------
                 if packet.raw_size == 40:
                    flow.udps.packet_40_count += 1
        ----------------------------------------------------------------
        """

    def on_expire(self, flow):
        """
        on_expire(self, flow):      Method called at flow expiration.
        Example: -------------------------------------------------------
                 if flow.udps.packet_40_count >= 10:
                    flow.udps.magic_message = "YES"
        ----------------------------------------------------------------
        """
        pass

    def cleanup(self):
        """
        cleanup(self):               Method called for plugin cleanup.
        Example: -------------------------------------------------------
                 del self.large_dict_passed_as_plugin_attribute
        ----------------------------------------------------------------
        """


class Capturer:
    def __init__(self,
                 source: str = SOURCE,
                 statistical_analysis: bool = STATISTICAL_ANALYSIS,
                 splt_analysis: int = SPLT_ANALYSIS) -> None:
        """
        This class is responsible for monitoring the network traffic with NFStreamer in case the user has not specified
        which CSV to run the training from or it does not exist.

        :param source: Packet capture source. Pcap file path, List of pcap files path (considered as a single file) or
        network interface name.
        :param statistical_analysis: 	Enable/Disable post-mortem flow statistical analysis.
        :param splt_analysis: 	Specify the sequence of first packets length for early statistical analysis. When set to
        0, splt_analysis is disabled.
        :return: None
        """
        self.__source = source
        self.__statistical_analysis = statistical_analysis
        self.__splt_analysis = splt_analysis

        self.__nsftreamer = NFStreamer(
            source=self.__source,
            statistical_analysis=self.__statistical_analysis,
            splt_analysis=self.__splt_analysis,
            udps=TimerPlugin()
        )

    def generate_export(self,
                        columns_to_anonymize: list = COLUMNS_TO_ANONYMIZE) -> pandas.DataFrame:
        """
        This function can be used to produce the pandas dataframe with the monitored content.

        :param columns_to_anonymize :List of columns names to anonymize. Anonymization is based on a random secret key
        generation at each start of NFStreamer. The generated key is used to anonymize configured values using blake2b
        algorithm.
        :return: Pandas DateFrame containing the generated data
        """
        self.__columns_to_anonymize = columns_to_anonymize
        self.__generated_dataframe = self.__nsftreamer.to_pandas(
            columns_to_anonymize=self.__columns_to_anonymize
        )
        return self.__generated_dataframe
