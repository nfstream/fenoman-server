import os

HOST_URI: str = str(os.getenv('FENOMAN_HOST_URI', '0.0.0.0'))
HOST_PORT: int = int(os.getenv('FENOMAN_SERVER_PORT', 8081))
BASE_URI: str = str(os.getenv('FENOMAN_BASE_URI', '/api/v1'))
OCP_APIM_KEY: str = str(os.getenv('FENOMAN_OCP_APIM_KEY', '7e8a84c1-34f7-44e4-91eb-96845d57396f'))
LOGGING_LEVEL: str = str(os.getenv('FENOMAN_LOGGING_LEVEL', 'DEBUG'))
LOGGING_FORMATTER: str = str(os.getenv('FENOMAN_LOGGING_FORMATTER', '%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
