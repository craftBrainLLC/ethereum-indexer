from typing import List
import time
import os

from interfaces.iextract import IExtract
from load.main import Load
from utils.address import validate_address


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

        self._load = Load()

    def _validate_address(self, address: List[str]) -> None:
        """
        @param address: address which to validate. Should be checksum correct.

        Raises if any address is invalid.
        """
        for a in address:
            validate_address(a)
        # todo: ensure there are no duplicates

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
        # * extracts transactions for all self._address

        COVALENT_TRANSACTIONS_URI = (
            lambda address, page_number: f'https://api.covalenthq.com/v1/1/address/{address}/transactions_v2/?quote-currency=USD&format=JSON&block-signed-at-asc=false&no-logs=false&page-number={page_number}&key={os.environ["COVALENT_API_KEY"]}&page-size=100'
        )

        # check if the db has transactions, if it has, then download the new ones
        # if it doesn't have any transactions, download all
        for addr in self._address:
            ...

        return
