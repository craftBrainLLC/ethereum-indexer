"""We use formal interfaces to enforce **modularity** first and foremost, and then structure
onto all of the code that is to be written.
"""
import abc


class ILoad(metaclass=abc.ABCMeta):
    ...
