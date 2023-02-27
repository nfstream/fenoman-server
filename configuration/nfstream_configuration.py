import os

SOURCE: str = str(os.getenv('NFSTREAM_SOURCE', 'eth0'))
STATISTICAL_ANALYSIS: bool = bool(os.getenv('NFSTREAM_STATISTICAL_ANALYSIS', True))
SPLT_ANALYSIS: int = int(os.getenv('NFSTREAM_SPLT_ANALYSIS', 10))
COLUMNS_TO_ANONYMIZE: list = list(os.getenv('NFSTREAM_COLUMNS_TO_ANONYMIZE', []))
MAX_NFLOWS: int = int(os.getenv('NFSTREAM_MAX_NFLOWS', 1000))
