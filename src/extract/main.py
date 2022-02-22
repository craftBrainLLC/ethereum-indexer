from typing import List, TypeVar
import os

from interfaces.iextract import IExtract
from load.main import Load
from utils.address import validate_address
from db import DB

Timestamp = TypeVar("Timestamp", int)


class Extract(IExtract):
    def __init__(self, address: List[str]):
        """
        @param address: list of addresses for which to extract the raw historical
        transaction data.
        @param update_frequency: list of update frequencies for each of the
        addresses supplied.
        """
        # Validate the addresses. https://github.com/ethereum/web3.py/blob/71ef3cd7edc299be64a8767c2a354a56c552555c/tests/core/utilities/test_validation.py#L11
        # Store the address
        self._validate_address(address)

        self._address: List[str] = address
        # gives timestamp up to which the extraction of the address is valid
        # if this is 1645534244, then our data is only relevant up to
        # 2/22/2022 12:51 UTC. It is a list because each address will have
        # its unique value
        self._valid_up_to: List[Timestamp] = [0 for _ in self._address]

        self._db_name = "ethereum-indexer"

        self._db = DB()
        self._load = Load()

    def _validate_address(self, address: List[str]) -> None:
        """
        @param address: address which to validate. Should be checksum correct.

        Raises if any address is invalid.
        """
        for a in address:
            validate_address(a)
        # todo: ensure there are no duplicates

    def _get_valid_up_to_collection_name(self, address: str) -> str:
        return f"{address}-valid-up-to"

    def _update_valid_up_to(self) -> None:
        """
        Goes through each address and determines its `valid_up_to` value.
        This ensures we do not extract all the data all the time, but only
        the new stuff. This is also helpful in case the binary raises and
        we need to restart it.
        """
        for addr in self._address:
            # ! what happens if the collection does not exist?
            valid_up_to = self._db.get_any_item(
                self._db_name, self._get_valid_up_to_collection_name(addr)
            )
            # ! needs parsing into timestamp
            self._valid_up_to = valid_up_to

    # re-setting _address is not allowed
    # https://towardsdatascience.com/how-to-create-read-only-and-deletion-proof-attributes-in-your-python-classes-b34cd1019c2d
    def __setattr__(self, key, value):
        if key == "_address" and hasattr(self, "_address"):
            raise AttributeError(
                "The value of the address attribute has already been set, and can not be re-set."
            )
        # * might even do type casting for some keys like in the example link
        self.__dict__[key] = value

    # Interface Implementation

    def flush(self) -> None:
        return

    def extract(self) -> None:
        """
        Extracts transactions for all self._address
        """

        # * notes
        # - possible to pull from a different blockchain if `chain_id` is different
        # - `block_signed_at=false` pulls all transactions putting most recent ones
        # at the top
        COVALENT_TRANSACTIONS_URI = (
            lambda address, page_number: f'https://api.covalenthq.com/v1/1/address/{address}/transactions_v2/?quote-currency=USD&format=JSON&block-signed-at-asc=false&no-logs=false&page-number={page_number}&key={os.environ["COVALENT_API_KEY"]}&page-size=100'
        )

        # - check if the db has transactions, if it has, then download the new ones
        # if it doesn't have any transactions, download all
        # - we utilise a separate collection to track what raw transactions have
        # been extracted
        for addr in self._address:
            ...

        return
