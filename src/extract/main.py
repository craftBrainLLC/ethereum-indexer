from typing import List
import time
import os

from interfaces.iextract import IExtract
from load.main import Load
from utils.address import validate_address


class Extract(IExtract):
    def __init__(self, address: List[str], update_frequency: List[int]):
        """
        @param address: list of addresses for which to extract the raw historical
        transaction data.
        @param update_frequency: list of update frequencies for each of the
        addresses supplied.
        """
        # Validate the addresses. https://github.com/ethereum/web3.py/blob/71ef3cd7edc299be64a8767c2a354a56c552555c/tests/core/utilities/test_validation.py#L11
        # Store the address
        self._validate_address(address)
        self._validate_update_frequency(update_frequency)

        self._address: List[str] = address
        self._update_frequency: List[int] = update_frequency

        self._load = Load()

    def _validate_address(self, address: List[str]) -> None:
        """
        @param address:

        Raises if any address is invalid.
        """
        for a in address:
            validate_address(a)

        # todo: ensure there are no duplicates

    def _validate_update_frequency(self, update_frequency: List[int]) -> None:
        """
        @param update_frequency:

        Raises if any update frequency is invalid.
        """
        for frequency in update_frequency:
            if frequency < 0:
                raise ValueError("Update frequency must be in seconds and be positive.")

        # ? anything else

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

        COVALENT_TRANSACTIONS_URI = (
            lambda address, page_number: f'https://api.covalenthq.com/v1/1/address/{address}/transactions_v2/?quote-currency=USD&format=JSON&block-signed-at-asc=false&no-logs=false&page-number={page_number}&key={os.environ["COVALENT_API_KEY"]}&page-size=100'
        )

        time.sleep(1)
        return
