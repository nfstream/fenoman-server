from sklearn.preprocessing import LabelEncoder
from typing import Any
from model.model import Model
import flwr as fl
from patterns.singleton import singleton
from typing import Optional, Tuple, Dict
from data.data import data
from configuration.evaluation_configuration import *
import numpy as np
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.metrics import confusion_matrix, f1_score, precision_score, recall_score
import matplotlib.pyplot as plt
from configuration.model_configuration import *
import time
import logging


@singleton
class Evaluation:
    @staticmethod
    def get_evaluation(model: Model) -> Any:
        """
        Return an evaluation function for server-side evaluation.

        :param model: input Model class that defined by FeNOMan Server
        :return: evaluation function
        """
        logging.debug('EVALUATION: Calling get evaluate method.')
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

            predictions = model().predict(x_val)
            predictions = np.argmax(predictions, axis=1).tolist()

            precision = precision_score(y_val, predictions, average="weighted")
            recall = recall_score(y_val, predictions, average="weighted")
            f1 = f1_score(y_val, predictions, average="weighted")

            return loss, {"accuracy": accuracy, "precision": precision, "recall": recall, "f1": f1}

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
        logging.debug('EVALUATION: Calling fit config method.')
        config = {
            "batch_size": EVALUATION_BATCH_SIZE,
            "local_epochs": EVALUATION_LOCAL_EPOCHS_MINIMUM if
            rnd < EVALUATION_FIT_CONFIG_ROUND_THRESHOLD else EVALUATION_LOCAL_EPOCHS_MAXIMUM,
        }
        return config

    @staticmethod
    def evaluate_config(rnd: int) -> dict:
        """
        Return evaluation configuration dict for each round.
        Perform five local evaluation steps on each client (i.e., use five
        batches) during rounds one to three, then increase to ten local
        evaluation steps.

        :param rnd: evaluation step counter
        :return: dictionary of validation steps
        """
        logging.debug('EVALUATION: Calling evaluate config method.')
        val_steps = EVALUATION_VALIDATION_STEP_MINIMUM if \
            rnd < EVALUATION_VALIDATION_STEP_ROUND_THRESHOLD else EVALUATION_VALIDATION_STEP_MAXIMUM
        return {"val_steps": val_steps}

    @staticmethod
    def generate_confusion_matrix(model: Model, labels: list = CONFUSION_MATRIX_LABELS) -> None:
        """
        This static function generates the configuration matrix for the model specified in the parameter for the
        specified matrix columns and then saves them under the "model/temp/{MODEL_NAME}..." folder.

        :param model: Model object
        :param labels: labels that should be used in the matrix
        :return: None
        """
        logging.debug('EVALUATION: Generating confusion matrix.')
        x_train, y_train, x_val, y_val = data.load_data()
        predictions = model().predict(x_val)
        predictions = np.argmax(predictions, axis=1).tolist()

        y_true = y_val.astype(int).tolist()
        matrix = confusion_matrix(y_true, predictions, normalize="true")

        disp = ConfusionMatrixDisplay(confusion_matrix=matrix, display_labels=labels)
        disp.plot(cmap=plt.cm.Blues)

        timestamp = time.strftime('%b-%d-%Y_%H%M', time.localtime())

        logging.debug('EVALUATION: Saving confusion matrix into temp folder.')
        plt.savefig(f'model/temp/{MODEL_NAME}_confusion_matrix_{timestamp}.png')

    @staticmethod
    def get_health_state() -> bool:
        """
        Returns the status of the class.

        :return: state of health status
        """
        logging.debug('EVALUATION: Returning health state.')
        return True


logging.debug('EVALUATION: Creating an instance of evaluation class.')
evaluation = Evaluation()
logging.debug('EVALUATION: Created instance of evaluation class.')
