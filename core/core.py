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
from typing import cast
from pathlib import Path


class SaveModelStrategy(fl.server.strategy.FedAvg):
    def aggregate_fit(self, rnd: int, results, failures, ):
        weights = super().aggregate_fit(rnd, results, failures)
        if weights is not None:
            # Save weights
            print(f"Saving round {rnd} weights to nosql database.")

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
        # TODO

        :param fraction_fit:
        :param fraction_eval:
        :param min_fit_clients:
        :param min_eval_clients:
        :param min_available_clients:
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
            print("Previous model parameter state loaded in.")
            bytes_io = BytesIO(records[0]['weights'])
            ndarry_deserialized = np.load(bytes_io, allow_pickle=True)
            initial_parameters = fl.common.ndarrays_to_parameters(cast(fl.common.NDArray, ndarry_deserialized))
        else:
            print("Previous model paramter is not found, new created.")
            # TODO ekkor kell csak a model train!
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

    def start_server(self, secure: bool = SECURE_MODE):
        server_configuration = {
            'strategy': self.__strategy,
            'server_address': f'{FLOWER_SERVER_ADDRESS}:{FLOWER_SERVER_PORT}',
            'config': fl.server.ServerConfig(num_rounds=self.__num_rounds),
        }
        if secure:
            server_configuration['certificates'] = (
                Path("configuration/certificates/ca.crt").read_bytes(),
                Path("configuration/certificates/server.pem").read_bytes(),
                Path("configuration/certificates/server.key").read_bytes()
             )
        fl.server.start_server(**server_configuration)
