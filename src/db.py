from typing import List, Dict, Any
from pymongo import MongoClient

from interfaces.idb import IDB


class DB(IDB):
    def __init__(self):
        self.client = MongoClient(port=27017)

    def put_item(self, item: Dict, table_name: str, collection_name: str) -> None:
        db = self.client[table_name]
        db[collection_name].replace_one({"_id": item["_id"]}, item, upsert=True)

    def get_item(self, id: str, table_name: str, collection_name: str) -> List[Any]:
        ...
        # db = self.client[table_name]
        # return list(db[collection_name].find({}))
