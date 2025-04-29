from pymongo import MongoClient, database


class MongoDB:
    db_name = "documentos"
    __client: MongoClient

    def __init__(self):
        self.__client = MongoClient("mongodb://localhost:27017/")

    def get_db(self) -> database.Database:
        return self.__client.get_database(self.db_name)

    def get_collection(self, collection_name) -> database.Collection:
        return self.get_db().get_collection(collection_name)


class Extract:
    __collection_name: str = "extracoes"

    def __init__(self, connection: MongoDB):
        self.__collection = connection.get_collection(self.__collection_name)

    def insert(self, value):
        self.__collection.insert_one(value)
