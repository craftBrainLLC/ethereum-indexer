"""Responsible for extracting the raw transaction data for the address"""


class Extract:
    """
    Has the ability to continue from where it left off.

    Has the ability to re-try the same poll over and over again.

    Has the ability to sleep and wait for the connection to come back up.

    Runs in a separate process from transform and load.

    It polls indefinitely with desired frequency the blockchain to obtain
    the latest transactions, to identify and store the ones that are
    concerned with the address.
    """

    def __init__(self, address, update_frequency: int):
        # validate the address. https://github.com/ethereum/web3.py/blob/71ef3cd7edc299be64a8767c2a354a56c552555c/tests/core/utilities/test_validation.py#L11
        # store the address

        ...

    def __call__(self):
        ...
