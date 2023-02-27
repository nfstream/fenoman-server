import os

DATABASE_CONNECTION_STRING: str = str(os.getenv('DATABASE_CONNECTION_STRING', ''))
DATABASE: str = str(os.getenv('DATABASE_NAME', 'fenoman'))
COLLECTION: str = str(os.getenv('DATABASE_COLLECTION', 'model'))
