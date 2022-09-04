import flwr as fl
from patterns.singleton import singleton
from model.model import model
from model.evaluation import evaluation
from configuration.flower_configuration import *
from database.nosql_database import nosql_database
import time
import pickle
import ast
from bson.binary import Binary
from configuration.model_configuration import *


class SaveModelStrategy(fl.server.strategy.FedAvg):
    def aggregate_fit(self, rnd: int, results, failures, ):
        weights = super().aggregate_fit(rnd, results, failures)
        if weights is not None:
            # Save weights
            print(f"Saving round {rnd} weights to nosql database.")

            timestamp = time.strftime('%b-%d-%Y_%H%M', time.localtime())
            nosql_database.insert_element(
                search_data_dict={
                    "timestamp": timestamp
                },
                insert_data_dict={
                    "model_name": MODEL_NAME,
                    "timestamp": timestamp,
                    "weights": Binary(pickle.dumps(weights))
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
L
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

        records, state = nosql_database.last_element({
            'model_name': MODEL_NAME
        }, 'timestamp')
        if state:
            
            pickle.loads(records[0]['weights'])
            # TODO bináris a data itt!




        self.__strategy = SaveModelStrategy(
            fraction_fit=fraction_fit,
            fraction_evaluate=fraction_eval,
            min_fit_clients=min_fit_clients,
            min_evaluate_clients=min_eval_clients,
            min_available_clients=min_available_clients,
            evaluate_fn=evaluation.get_evaluation(model),
            on_fit_config_fn=evaluation.fit_config,
            on_evaluate_config_fn=evaluation.evaluate_config, # TODO itt az initial paraméter ide kell majd beadni a dolgoakt
            initial_parameters=fl.common.ndarrays_to_parameters(model().get_weights()),
        )

    def start_server(self):
        fl.server.start_server(
            strategy=self.__strategy,
            server_address="0.0.0.0:8080",
            config=fl.server.ServerConfig(num_rounds=self.__num_rounds),
            # certificates=(
            #    pathlib.Path("configuration/certificates/ca.crt").read_bytes(),
            #    pathlib.Path("configuration/certificates/server.pem").read_bytes(),
            #    pathlib.Path("configuration/certificates/server.key").read_bytes()
            # ),
        )
