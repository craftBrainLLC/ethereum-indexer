"""We use formal interfaces to enforce **modularity** first and foremost, and then structure
onto all of the code that is to be written.
"""
import logging
import time
import abc

INTERNET_CONNECTION_CHECK_FREQUENCY = 5  # in seconds


class IExtract(metaclass=abc.ABCMeta):
    """
    [function] determine if there is Internet connection.

    [function] sleep and wait for the connection to come back up.

    [Properties]
    Runs in a separate process from transform and load.

    It polls indefinitely with desired frequency the blockchain to obtain
    the latest transactions, to identify and store the ones that are
    concerned with the address.
    """

    @classmethod
    def __subclasshook__(cls, subclass):
        return (
            hasattr(subclass, "is_connected_to_internet")
            and callable(subclass.is_connected_to_internet)
            and hasattr(subclass, "extract")
            and callable(subclass.extract)
            and hasattr(subclass, "flush")
            and callable(subclass.flush)
            or NotImplemented
        )

    @abc.abstractmethod
    def is_connected_to_internet(self) -> bool:
        """Determines if connected to Internet"""
        raise NotImplementedError

    @abc.abstractmethod
    def extract(self) -> None:
        """Extracts the new data since the last extraction. If this
        is the first extraction, then extracts everything up to now."""
        raise NotImplementedError

    @abc.abstractmethod
    def flush(self) -> None:
        """Flushes the extracted in memory data into the db or other
        means of storage"""
        raise NotImplementedError

    def __call__(self):
        def repeat(is_ok: bool):
            if not is_ok:
                is_connected = self.is_connected_to_internet()
                while not is_connected:
                    logging.warning("no internet connection. waiting.")
                    time.sleep(INTERNET_CONNECTION_CHECK_FREQUENCY)
                    is_connected = self.is_connected_to_internet()
                # todo: log other potential errors
                # * explicitly is_ok True
                is_ok = True
                return is_ok
            else:
                # * is OK
                return is_ok

        while True:
            logging.debug("extracting")

            ok = self.extract()

            while not ok:
                ok = repeat(ok)

            self.flush()
