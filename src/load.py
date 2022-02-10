"""Responsible for loading the data into the db"""
from interfaces.iload import ILoad


class Load(ILoad):
    def __init__(self):
        ...

    def __call__(self):
        ...
