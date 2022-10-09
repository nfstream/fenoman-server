from sklearn.preprocessing import LabelEncoder
from typing import Any
from model.model import Model
import flwr as fl
from patterns.singleton import singleton
from typing import Optional, Tuple, Dict
from data.data import data
from configuration.evaluation_config import *


@singleton
class Evaluation:
    @staticmethod
    def get_evaluation(model: Model) -> Any:
        """
        Return an evaluation function for server-side evaluation.

        :param model: input Model class that defined by FeNOMan Server
        :return: evaluation function
        """
        _, _, x_val, y_val = data.load_data()

        lb = LabelEncoder()

        y_val = lb.fit_transform(y_val)

        def evaluate(
                server_round: int,
                parameters: fl.common.NDArrays,
                config: Dict[str, fl.common.Scalar],
        ) -> Optional[Tuple[float, Dict[str, fl.common.Scalar]]]:
            """
            The `evaluate` function will be called after every round

            :param server_round: count of server evaluation round
            :param parameters: model paramters as ndarrays
            :param config: model configuration
            :return: loss and accuracy as a dict
            """
            model().set_weights(parameters)  # Update model with the latest parameters
            loss, accuracy = model().evaluate(x_val, y_val)
            return loss, {"accuracy": accuracy}

        return evaluate

    @staticmethod
    def fit_config(rnd: int) -> dict:
        """
        Return training configuration dict for each round.
        Keep batch size fixed at 32, perform two rounds of training with one
        local epoch, increase to two local epochs afterwards.

        :param rnd: fit round counter
        :return: dictionary of configuration settings
        """
        config = {
            "batch_size": EVALUATION_BATCH_SIZE,
            "local_epochs": EVALUATION_LOCAL_EPOCHS_MINIMUM if
            rnd < EVALUATION_FIT_CONFIG_ROUND_THRESHOLD else EVALUATION_LOCAL_EPOCHS_MAXIMUM,
        }
        return config

    @staticmethod
    def evaluate_config(rnd: int):
        """
        Return evaluation configuration dict for each round.
        Perform five local evaluation steps on each client (i.e., use five
        batches) during rounds one to three, then increase to ten local
        evaluation steps.

        :param rnd:
        :return:
        """
        val_steps = EVALUATION_VALIDATION_STEP_MINIMUM if \
            rnd < EVALUATION_VALIDATION_STEP_ROUND_THRESHOLD else EVALUATION_VALIDATION_STEP_MAXIMUM
        return {"val_steps": val_steps}

    @staticmethod
    def get_health_state() -> bool:
        """
        Returns the status of the class.

        :return: state of health status
        """
        return True


evaluation = Evaluation()
