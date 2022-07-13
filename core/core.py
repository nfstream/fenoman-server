import flwr as fl
from patterns.singleton import singleton
import pathlib
from model.model import model
from model.evaluation import evaluation


@singleton
class Core:
    def __init__(self, num_rounds: int, num_clients: int, fraction_fit: float) -> None:
        """

        :param num_rounds:
        :param num_clients:
        :param fraction_fit:
        """
        self.__strategy = fl.server.strategy.FedAvg(
            fraction_fit=0.3,
            fraction_eval=0.2,
            min_fit_clients=3,
            min_eval_clients=2,
            min_available_clients=10,
            eval_fn=evaluation.get_eval_fn(model),
            on_fit_config_fn=evaluation.fit_config,
            on_evaluate_config_fn=evaluation.evaluate_config,
            initial_parameters=fl.common.weights_to_parameters(model.get_weights()),
        )

        fl.server.start_server(
            strategy=self.__strategy,
            server_address="[::]:8080",
            config={
                "num_rounds": num_rounds
            },
            certificates=(
                pathlib.Path("configuration/certificates/ca.crt").read_bytes(),
                pathlib.Path("configuration/certificates/server.pem").read_bytes(),
                pathlib.Path("configuration/certificates/server.key").read_bytes()
            ),
        )
