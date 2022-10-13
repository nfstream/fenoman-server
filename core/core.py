import flwr as fl
from patterns.singleton import singleton
from model.model import model
from model.evaluation import evaluation
from configuration.flower_configuration import *
from database.nosql_database import nosql_database
import time
import numpy as np
from io import BytesIO
from configuration.model_configuration import *
from typing import cast, Any
from pathlib import Path


class SaveModelStrategy(fl.server.strategy.FedAvg):
    def aggregate_fit(self, rnd: int, results, failures,) -> Any:
        """
        This custom strategy saves out the model into the mongo database in each round.

        :param rnd: The current round of federated learning.
        :param results: Successful updates from the previously selected and configured clients. Each pair of
        (ClientProxy, FitRes constitutes a successful update from one of the previously selected clients. Not that not
        all previously selected clients are necessarily included in this list: a client might drop out and not submit a
        result. For each client that did not submit an update, there should be an Exception in failures.
        :param failures: Exceptions that occurred while the server was waiting for client updates.
        :return: The aggregated evaluation result. Aggregation typically uses some variant of a weighted average.
        """
        weights = super().aggregate_fit(rnd, results, failures)
        if weights is not None:
            # Save weights
            timestamp = time.strftime('%b-%d-%Y_%H%M', time.localtime())
            ndarray = fl.common.parameters_to_ndarrays(weights[0])

            bytes_io = BytesIO()
            np.save(bytes_io, ndarray, allow_pickle=True)

            nosql_database.insert_element(
                search_data_dict={
                    "timestamp": timestamp
                },
                insert_data_dict={
                    "model_name": MODEL_NAME,
                    "timestamp": timestamp,
                    "weights": bytes_io.getvalue()
                }
            )
        return weights


@singleton
class Core:
    def __init__(self,
                 fraction_fit: float = FRACTION_FIT,
                 fraction_eval: float = FRACTION_EVAL,
                 min_fit_clients: int = MIN_FIT_CLIENTS,
                 min_eval_clients: int = MIN_EVAL_CLIENTS,
                 min_available_clients: int = MIN_AVAILABLE_CLIENTS,
                 num_rounds: int = NUM_ROUNDS) -> None:
        """
        The Core class is an internal instance of the FeNOMan system. This is where the server and configurations
        implemented by Flower are started.

        :param fraction_fit: Fraction of clients used during training. In case min_fit_clients is larger than
        fraction_fit * available_clients, min_fit_clients will still be sampled. Defaults to 1.0.
        :param fraction_eval: Fraction of clients used during validation. In case min_evaluate_clients is larger than
        fraction_evaluate * available_clients, min_evaluate_clients will still be sampled. Defaults to 1.0.
        :param min_fit_clients: Minimum number of clients used during training. Defaults to 2.
        :param min_eval_clients: Minimum number of clients used during validation. Defaults to 2.
        :param min_available_clients: Minimum number of total clients in the system. Defaults to 2.
        """
        self.__fraction_fit = fraction_fit
        self.__fraction_eval = fraction_eval
        self.__min_fit_clients = min_fit_clients
        self.__min_eval_clients = min_eval_clients
        self.__min_available_clients = min_available_clients
        self.__num_rounds = num_rounds

        # We must load in the last model that was used in a given model_name configuration scenario
        initial_parameters = None
        records, state = nosql_database.last_n_element(
            search_field={
                'model_name': MODEL_NAME
            },
            key='timestamp',
            limit=1)

        if state:
            bytes_io = BytesIO(records[0]['weights'])
            ndarry_deserialized = np.load(bytes_io, allow_pickle=True)
            initial_parameters = fl.common.ndarrays_to_parameters(cast(fl.common.NDArray, ndarry_deserialized))
        else:
            initial_parameters = fl.common.ndarrays_to_parameters(model().get_weights())

        self.__strategy = SaveModelStrategy(
            fraction_fit=fraction_fit,
            fraction_evaluate=fraction_eval,
            min_fit_clients=min_fit_clients,
            min_evaluate_clients=min_eval_clients,
            min_available_clients=min_available_clients,
            evaluate_fn=evaluation.get_evaluation(model),
            on_fit_config_fn=evaluation.fit_config,
            on_evaluate_config_fn=evaluation.evaluate_config,
            initial_parameters=initial_parameters,
        )

    def start_server(self,
                     flower_server_address: str = FLOWER_SERVER_ADDRESS,
                     flower_server_port: str = FLOWER_SERVER_PORT,
                     secure: bool = SECURE_MODE) -> None:
        """
        This method starts the Flower server inside the Fenoman server, where Fenoman clients can connect using the
        flower directory.

        :param flower_server_address: The IPv4 or IPv6 address of the server.
        :param flower_server_port: Servers port where to listen to the Flower clients.
        :param secure: This enables the secure SSL connection between client and server.
        :return: None
        """
        self.__flower_server_address = flower_server_address
        self.__flower_server_port = flower_server_port
        self.__secure = secure

        server_configuration = {
            'strategy': self.__strategy,
            'server_address': f'{self.__flower_server_address}:{self.__flower_server_port}',
            'config': fl.server.ServerConfig(num_rounds=self.__num_rounds),
        }
        if self.__secure:
            server_configuration['certificates'] = (
                Path("configuration/certificates/ca.crt").read_bytes(),
                Path("configuration/certificates/server.pem").read_bytes(),
                Path("configuration/certificates/server.key").read_bytes()
             )
        fl.server.start_server(**server_configuration)

    @staticmethod
    def get_health_state() -> bool:
        """
        Returns the status of the class.

        :return: state of health status
        """
        for component in [model, evaluation, nosql_database]:
            if not component.get_health_state():
                return False
        return True
