"""Responsible for loading the data into the db"""
import logging
import time

from interfaces.iload import ILoad


class Load(ILoad):
    def __init__(self):
        ...

    def __call__(self):
        logging.debug("loading")
