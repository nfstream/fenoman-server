import flwr as fl
from patterns.singleton import singleton
import pathlib
from model.model import model
from model.evaluation import evaluation


@singleton
class Core:
    def __init__(self, fraction_fit: float = 0.3, fraction_eval: float = 0.2, min_fit_clients: int = 3,
                 min_eval_clients: int = 2, min_available_clients=10, num_rounds: int = 32) -> None:
        """
        # TODO

        :param fraction_fit:
        :param fraction_eval:
        :param min_fit_clients:
        :param min_eval_clients:
        :param min_available_clients:
        """
        self.__strategy = fl.server.strategy.FedAvg(
            fraction_fit=fraction_fit,
            fraction_eval=fraction_eval,
            min_fit_clients=min_fit_clients,
            min_eval_clients=min_eval_clients,
            min_available_clients=min_available_clients,
            eval_fn=evaluation.get_evaluation(model),
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
