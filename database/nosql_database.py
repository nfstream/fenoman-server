import pymongo
from pymongo.results import UpdateResult
from configuration.nosql_database_configuration import *
from typing import Tuple, Union
from patterns.singleton import singleton


@singleton
class NoSqlDataBase:
    def __init__(self, hostname: str = DATABASE_HOST, port: int = DATABASE_PORT,
                 database: str = DATABASE, collection: str = COLLECTION) -> None:
        """
        Initialization function, creates the database if it does not exist, and the collection.
        :rtype None
        :param database: database name
        :param collection: collection name
        """
        self.__client = pymongo.MongoClient(host=hostname, port=port)
        self.__database_name = database
        self.__collection_name = collection

        if database in self.__client.list_database_names():
            self.__database = self.__client.get_database(database)
        else:
            self.__database = self.__client[database]

        if collection in self.__database.collection_names():
            self.__collection = self.__database.get_collection(collection)
        else:
            self.__collection = self.__database[collection]

    def insert_element(self, search_data_dict: dict, insert_data_dict: dict) -> Tuple[str, bool]:
        """
        Inserts the passed dictionary elements into the given database.
        :param insert_data_dict:
        :param search_data_dict:
        :return: state
        """
        if search_data_dict == {'special_case': 'insert_anyway'}:
            exists = False
        else:
            _, exists = self.get_element(search_data_dict)

        if exists:
            res, success = 'Element already exists in the DataBase!', False
        else:
            res, success = self.__collection.insert(insert_data_dict), True
        return str(res), success

    def get_element(self, search_fields: dict) -> Tuple[Union[list, str], bool]:
        """
        Dicitonary should be passed as a search fieldset, then these will be searched and returned in the given
        collection.
        :param search_fields: field values to look for
        :return: records found
        """
        resp_data = []
        if self.__collection.find(search_fields).count() > 0:
            for element in self.__collection.find(search_fields):
                resp_data.append(element)
            return resp_data, True
        else:
            return 'Element does not exists in the DataBase!', False

    def delete_element(self, search_fields: dict) -> Tuple[Union[int, str], bool]:
        """
        Delete items passed in the Dictionary from the database.
        :param search_fields: search value of records to be deleted
        :return: number of records deleted
        """
        resp = self.__collection.delete_many(search_fields)
        if resp.deleted_count > 0:
            return resp.deleted_count, True
        else:
            return 'Element does not exists in the DataBase!', False

    def drop_collection(self) -> None:
        """
        Deletes the collection with all its contents.
        :return: none
        """
        self.__collection.drop()

    def update_element(self, search_fields: dict, update_data: dict) -> UpdateResult:
        """
        # TODO
        :param search_fields:
        :param update_data:
        :return:
        """
        resp = self.__collection.update_many(search_fields, {"$set": update_data})
        return resp


nosql_database = NoSqlDataBase()
