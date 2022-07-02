
class Database:
    def __init__(self, uri, collection, client, secret):
        print("DB init")
        self.uri = uri
        self.collection = collection
        self.client = client
        self.secret = secret

    def get_data(self, name):
        #Download from DB
        data = name

        return data

    def insert_data(self, data_name, description):
        #Upload to DB
        success = False

        if success:
            return True

        return False

modelDB = Database("","","","")
clientDB = Database("","","","")
