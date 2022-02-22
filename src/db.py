from typing import List, Dict, Any
from pymongo import MongoClient

from interfaces.idb import IDB


class DB(IDB):
    def __init__(self):
        self.client = MongoClient(port=27017)

    def put_item(self, item: Dict, table_name: str, collection_name: str) -> None:
        db = self.client[table_name]
        db[collection_name].replace_one({"_id": item["_id"]}, item, upsert=True)

    def get_item(self, id: str, table_name: str, collection_name: str) -> Any:
        db = self.client[table_name]
        return db[collection_name].find({"_id": id})

    def get_all_items(self, table_name: str, collection_name: str) -> List[Any]:
        db = self.client[table_name]
        return list(db[collection_name]).find({})

    def get_any_item(self, table_name: str, collection_name: str) -> Any:
        """
        MongoDB will return an empty list is collection does not exist
        """
        all_items = self.get_all_items(table_name, collection_name)
        if len(all_items) == 0:
            return None
        else:
            return all_items[0]
