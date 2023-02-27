import os
from .model_configuration import MODEL_NAME

FRACTION_FIT: float = float(os.getenv('FLOWER_FRACTION_FIT', 0.3))
FRACTION_EVAL: float = float(os.getenv('FLOWER_FRACTION_EVAL', 0.2))
MIN_FIT_CLIENTS: int = int(os.getenv('FLOWER_MIN_FIT_CLIENTS', 1))
MIN_EVAL_CLIENTS: int = int(os.getenv('FLOWER_MIN_EVAL_CLIENTS', 1))
MIN_AVAILABLE_CLIENTS: int = int(os.getenv('FLOWER_MIN_AVAILABLE_CLIENTS', 1))
NUM_ROUNDS: int = int(os.getenv('FLOWER_MIN_ROUNDS', 1))
SERVER_JOB_TIMER_MINUTES: int = int(os.getenv('FLOWER_SERVER_JOB_TIMER_MINUTES', 1))
SECURE_MODE: bool = bool(os.getenv('FLOWER_SECURE_MODE', False))
FLOWER_SERVER_ADDRESS: str = str(os.getenv('FLOWER_SERVER_ADDRESS', '0.0.0.0'))

flower_port_range_start: int = int(os.getenv('FLOWER_PORT_RANGE_START', 8090))
flower_port_range_end: int = int(os.getenv('FLOWER_PORT_RANGE_END', 8094))
FLOWER_SERVER_PORT: list = [i for i in range(flower_port_range_start, len(MODEL_NAME)+1,) if i <= flower_port_range_end]
