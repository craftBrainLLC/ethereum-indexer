"""Responsible for extracting the raw transaction data for the address"""
from typing import List

from interfaces.iextract import IExtract


class Extract(IExtract):
    def __init__(self, address: List[str], update_frequency: int):
        # validate the address. https://github.com/ethereum/web3.py/blob/71ef3cd7edc299be64a8767c2a354a56c552555c/tests/core/utilities/test_validation.py#L11
        # store the address

        ...

    def __call__(self):
        ...
