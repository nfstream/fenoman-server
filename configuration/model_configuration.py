import os

MODEL_NAME: list = list(os.getenv('MODEL_NAME', ['LSTM']))
MODEL_BATCH_SIZE: int = int(os.getenv('MODEL_BATCH_SIZE', 64))
MODEl_EPOCHS: int = int(os.getenv('MODEL_EPOCHS', 1))
