"""We use formal interfaces to enforce **modularity** first and foremost, and then structure
onto all of the code that is to be written.
"""
import abc


class IExtract(metaclass=abc.ABCMeta):
    """
    [function] continue from where it left off.

    [function] re-try the same poll over and over again.

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
            hasattr(subclass, "continue_where_left_off")
            and callable(subclass.continue_where_left_off)
            and hasattr(subclass, "retry_poll")
            and callable(subclass.retry_poll)
            and hasattr(subclass, "is_connected_to_internet")
            and callable(subclass.is_connected_to_internet)
            and hasattr(subclass, "wait_for_internet_connection")
            and callable(subclass.wait_for_internet_connection)
            or NotImplemented
        )

    @abc.abstractmethod
    def continue_where_left_off(self):
        """After downloading all the raw transaction data, this function
        gets called to continue from the last point it left off"""
        raise NotImplementedError

    @abc.abstractmethod
    def retry_poll(self):
        """Retries the poll untill it succeeds"""
        raise NotImplementedError

    @abc.abstractmethod
    def is_connected_to_internet(self):
        """Determines if connected to Internet"""
        raise NotImplementedError

    @abc.abstractmethod
    def wait_for_internet_connection(self):
        """Waits for Internet connection to go back up"""
        raise NotImplementedError
