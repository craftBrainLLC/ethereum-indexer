from typing import List
import time

from interfaces.iextract import IExtract
from load.main import Load


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

        self._address: List[str] = self._strandardise_address(address)
        self._update_frequency: List[int] = update_frequency

        self._load = Load()

    def _validate_address(self, address: List[str]) -> None:
        """
        @param address:

        Raises if any address is invalid.
        """
        ...

    def _validate_update_frequency(self, update_frequency: List[int]) -> None:
        """
        @param update_frequency:

        Raises if any update frequency is invalid.
        """
        ...

    def _strandardise_address(self, address: List[str]) -> List[str]:
        """
        @param address:

        Standardises the address as per ...
        """
        ...

    # Interface Implementation

    def flush(self) -> None:
        return

    def extract(self) -> None:
        time.sleep(1)
        return
