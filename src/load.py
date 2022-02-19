"""Responsible for loading the data into the db"""
import time

from interfaces.iload import ILoad


class Load(ILoad):
    def __init__(self):
        ...

    def __call__(self):
        while True:
            print("loading")
            time.sleep(1)
