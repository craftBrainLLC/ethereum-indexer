"""We use formal interfaces to enforce **modularity** first and foremost, and then structure
onto all of the code that is to be written.
"""
import abc
from typing import Dict, List


class IDB(metaclass=abc.ABCMeta):
    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, "put_item")
            and callable(subclass.put_item)
            and hasattr(subclass, "put_items")
            and callable(subclass.put_items)
            and hasattr(subclass, "get_item")
            and callable(subclass.get_item)
            and hasattr(subclass, "get_items")
            and callable(subclass.get_items)
            or NotImplemented
        )

    @abc.abstractmethod
    def put_item(self, item: Dict, database_name: str, collection_name: str):
        """Load in the data set"""
        raise NotImplementedError

    @abc.abstractmethod
    def put_items(self, items: List[Dict], database_name: str, collection_name: str):
        """Extract text from the data set"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_item(self, id: str, database_name: str, collection_name: str):
        """Load in the data set"""
        raise NotImplementedError

    @abc.abstractmethod
    def get_items(self, ids: List[str], database_name: str, collection_name: str):
        """Load in the data set"""
        raise NotImplementedError
