import numpy as np

from model.model import Model
import flwr as fl
import tensorflow as tf
#from patterns.singleton import singleton
from typing import Optional, Tuple, Dict
from data.data import data
from sklearn.metrics import f1_score, precision_score, recall_score


#@singleton
class Evaluation:
    @staticmethod
    def get_evaluation(model: Model):
        """Return an evaluation function for server-side evaluation."""
        _, _, x_val, y_val = data.load_data()

        # The `evaluate` function will be called after every round
        def evaluate(
                server_round: int,
                parameters: fl.common.NDArrays,
                config: Dict[str, fl.common.Scalar],
        ) -> Optional[Tuple[float, Dict[str, fl.common.Scalar]]]:
            model().set_weights(parameters)  # Update model with the latest parameters
            loss, accuracy = model().evaluate(x_val, y_val)

            predictions = model().predict(x_val)
            predictions = np.argmax(predictions, axis=1).tolist()

            #y_true = y_val.astype(int).tolist()
            precision = precision_score(y_val, predictions, average="weighted")
            recall = recall_score(y_val, predictions, average="weighted")
            f1 = f1_score(y_val, predictions, average="weighted")

            return loss, {"accuracy": accuracy, "precision": precision, "recall": recall, "f1": f1}

        return evaluate

    @staticmethod
    def fit_config(rnd: int):
        """
        Return training configuration dict for each round.
        Keep batch size fixed at 32, perform two rounds of training with one
        local epoch, increase to two local epochs afterwards.
        :param rnd:
        :return:
        """
        config = {
            "batch_size": 32,
            "local_epochs": 1 if rnd < 2 else 100,
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
        val_steps = 5 if rnd < 4 else 10
        return {"val_steps": val_steps}


evaluation = Evaluation()
