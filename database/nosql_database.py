import pymongo
from pymongo.results import UpdateResult
from configuration.nosql_database_configuration import *
from typing import Tuple, Union
from patterns.singleton import singleton
import logging


@singleton
class NoSqlDataBase:
    def __init__(self,
                 hostname: str = DATABASE_HOST,
                 port: int = DATABASE_PORT,
                 database: str = DATABASE,
                 collection: str = COLLECTION) -> None:
        """
        Initialization function, creates the database if it does not exist, and the collection.

        :rtype None
        :param hostname: host uri of the database localhost or 0.0.0.0 if the database is on the same host as the server
        :param port: database port
        :param database: database name
        :param collection: collection name
        :return: None
        """
        self.__client = pymongo.MongoClient(host=hostname, port=port)
        self.__database_name = database
        self.__collection_name = collection

        if database in self.__client.list_database_names():
            self.__database = self.__client.get_database(database)
        else:
            self.__database = self.__client[database]

        if collection in self.__database.list_collection_names():
            self.__collection = self.__database.get_collection(collection)
        else:
            self.__collection = self.__database[collection]

    def insert_element(self, search_data_dict: dict, insert_data_dict: dict) -> Tuple[str, bool]:
        """
        Inserts the passed dictionary elements into the given database.

        :param insert_data_dict: data to be inserted into the database
        :param search_data_dict: field values to look for used to check if the element already exists
        :return: state
        """
        if search_data_dict == {'special_case': 'insert_anyway'}:
            exists = False
        else:
            _, exists = self.get_element(search_data_dict)

        if exists:
            logging.debug('NOSQLDATABASE: Cannot insert element. Element already exists in the database!')
            res, success = 'Element already exists in the DataBase!', False
        else:
            logging.debug('NOSQLDATABASE: Inserint element into database.')
            res, success = self.__collection.insert_one(insert_data_dict), True
        return str(res), success

    def get_element(self, search_fields: dict) -> Tuple[Union[list, str], bool]:
        """
        Dictionary should be passed as a search fieldset, then these will be searched and returned to the given
        collection.

        :param search_fields: field values to look for
        :return: records found
        """
        resp_data = []
        if self.__collection.count_documents(search_fields) > 0:
            for element in self.__collection.find(search_fields):
                resp_data.append(element)
            logging.debug('NOSQLDATABASE: Returning elements from database.')
            return resp_data, True
        else:
            logging.debug('NOSQLDATABASE: Element does not exists in the DataBase!')
            return 'Element does not exists in the DataBase!', False

    def delete_element(self, search_fields: dict) -> NotImplemented:
            #Tuple[Union[int, str], bool]:
        """
        Delete items passed in the Dictionary from the database.

        :param search_fields: search value of records to be deleted
        :return: number of records deleted
        """
        logging.warning('NOSQLDATABASE: Delete element is not implemented!')
        return NotImplemented
        #resp = self.__collection.delete_many(search_fields)
        #if resp.deleted_count > 0:
        #    return resp.deleted_count, True
        #else:
        #    return 'Element does not exists in the DataBase!', False

    def drop_collection(self) -> NotImplemented:
        """
        Deletes the collection with all its contents.

        :return: NotImplemented
        """
        logging.warning('NOSQLDATABASE: Drop collection is not implemented!')
        return NotImplemented
        #self.__collection.drop()

    def update_element(self, search_fields: dict, update_data: dict) -> NotImplemented:
        """
        Currently not supported due to the Mongodb version update. The procedure does not use the update of existing
        records so this procedure cannot be used.

        :param search_fields: search value of records to be updated
        :param update_data: the new data to overwrite the current data stored in the database
        :return: NotImplemented
        """
        logging.warning('NOSQLDATABASE: Update Element is not implemented!')
        return NotImplemented
        #resp = self.__collection.update_many(search_fields, {"$set": update_data})
        #return resp

    def last_n_element(self, search_field: dict, key: str, limit: int) -> Tuple[Union[list, str], bool]:
        """
        This function returns the latest element based on the key value. Use the search_field to filter to a given
        part of the collection.

        :param search_field: field value to look for
        :param key: field to make the sort
        :param limit: count of elements should be returned
        :return: latest record
        """
        resp_data = []
        for element in self.__collection.find(search_field).sort([(key, -1)]).limit(limit):
            resp_data.append(element)

        if len(resp_data) > 0:
            logging.debug('NOSQLDATABASE: Returning the last n element.')
            return resp_data, True
        else:
            logging.debug('NOSQLDATABASE: No element in the DataBase with the given search_field.')
            return 'No element in the DataBase with the given search_field', False

    def get_health_state(self) -> bool:
        """
        Returns the status of the class.

        :return: state of health status
        """
        logging.debug('NOSQLDATABASE: Returning health state.')
        try:
            self.__client.server_info()
            return True

        # pymongo.errors.ServerSelectionTimeoutError
        except Exception as exp:
            return False


logging.debug('NOSQLDATABASE: Creating an instance of nosqldatabase class.')
nosql_database = NoSqlDataBase()
logging.debug('NOSQLDATABASE: Created instance of nosqldatabase class.')
