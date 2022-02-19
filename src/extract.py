"""Responsible for extracting the raw transaction data for the address"""
from typing import List

from interfaces.iextract import IExtract

# TODO: how to document python code inside of the docs. Extract class's python
# is not rendered properly in VSCode


class Extract(IExtract):
    """
    The job of extractor is to extract all the historical raw transaction
    data pertaining to an address and check for any new transactions
    concerning the said addresses every update_frequency.

    The said transactions are stored in memory until loader takes them
    and writes to the db. Upon successful write, they are removed from memory.

    To avoid having cross-process communication between loader and extract,
    we introduce an interface that supports writing to db. Extract adheres
    to this interface, and so load supports such interfaces. Therefore,
    we simply require each implementation of the writing to db interface
    to have its own instance of a loader. For example,

        ```python
        EVERY_10_SECONDS = 10
        EVERY_20_SECONDS = 20

        extract = Extract(['0x', '0x'], [EVERY_10_SECONDS, EVERY_20_SECONDS])
        load = Load(extract)

        transform = Transform(...)
        load = Load(transform)
        ```

    """

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

        self._address: List[str] = self._strandardise_address(address)
        self._update_frequency: List[int] = update_frequency

    def _validate_address(self, address: List[str]):
        """
        Raises if any address is invalid.
        """
        ...

    def _validate_update_frequency(update_frequency: List[int]):
        """
        Raises if any update frequency is invalid.
        """
        ...

    def _strandardise_address(self, address: List[str]) -> List[str]:
        """
        Standardises the address as per ...
        """
        ...

    def __call__(self):
        ...
