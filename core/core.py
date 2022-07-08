import flwr as fl
from patterns.singleton import singleton


@singleton
class Core:
    def __init__(self, num_rounds: int, num_clients: int, fraction_fit: float) -> None:
        """

        :param num_rounds:
        :param num_clients:
        :param fraction_fit:
        """
        # TODO strategy must came from model.model!
        self.__strategy = fl.FedAvg(min_available_clients=num_clients,
                                    fraction_fit=fraction_fit)
        fl.server.start_server(
            strategy=self.__strategy,
            server_address="[::]:8080",
            config={
                "num_rounds": num_rounds
            },

        )
