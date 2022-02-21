"""
We use formal interfaces to enforce **modularity** first and foremost, and then structure
onto all of the code that is to be written.

Think of this as mathematical axioms, with which you then build proofs which you then use
together to build new proofs.
"""
import abc
from typing import List, Any


# todo: some of the items below can raise. Write docs for it


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
    def put_item(self, item: Any, database_name: str, collection_name: str) -> None:
        """
        Load in the data set
        @param item:
        @param database_name:
        @param collection_name:
        """
        raise NotImplementedError

    def put_items(
        self, items: List[Any], database_name: str, collection_name: str
    ) -> None:
        """
        Users are free to override to make use of in-built db batching API.
        @param items:
        @param database_name:
        @param collection_name:
        """
        for item in items:
            self.put_item(item, database_name, collection_name)

    @abc.abstractmethod
    def get_item(self, id: str, database_name: str, collection_name: str) -> Any:
        """
        Load in the data set
        @param id:
        @param database_name:
        @param collection_name:
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_any_item(self, database_name: str, collection_name: str) -> Any:
        """
        Gets any item from a collection.
        This is useful to figure out if collection even exists.
        This is more useful than simply returning number of items in
        the collection, because you can perform some actions on the
        attributes of the returned result, for example.

        @param database_name:
        @param collection_name:
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_all_items(self, database_name: str, collection_name: str) -> List[Any]:
        raise NotImplementedError

    def get_items(
        self, ids: List[str], database_name: str, collection_name: str
    ) -> List[Any]:
        """
        Users are free to override to make use of in-built db batching API.
        @param ids:
        @param database_name:
        @param collection_name:
        """
        out: List[Any] = []
        for id in ids:
            item = self.get_item(id, database_name, collection_name)
            out.append(item)
        return out
