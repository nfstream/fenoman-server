from model import Model
import flwr as fl
from patterns.singleton import singleton
from typing import Optional, Tuple, Dict


@singleton
class Evaluation:
    @staticmethod
    def get_evaluation(model: Model, data, validation_split: float = 0.1):
        """
        Return an evaluation function for server-side evaluation.
        :param model:
        :param data:
        :param validation_split:
        :return:
        """
        # TODO splitting mechanisms required here!
        (x_train, y_train) = data
        split_size = len(x_train) * (1 - validation_split)
        x_val, y_val = x_train[split_size:], y_train[split_size:]
        score = Model.evaluate(
            weights="",
            model=model,
            x_val=x_val,
            y_val=y_val
        )
        return score

    @staticmethod
    def evaluate(weights: fl.common.Weights, model: Model, x_val: list, y_val: list) -> Optional[
        Tuple[float, Dict[str, fl.common.Scalar]]]:
        """

        :param weights:
        :param model:
        :param x_val:
        :param y_val:
        :return:
        """
        model.set_weights(weights)  # Update model with the latest parameters
        loss, accuracy = model.evaluate(x_val, y_val)
        return loss, {"accuracy": accuracy}

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
            "local_epochs": 1 if rnd < 2 else 2,
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
