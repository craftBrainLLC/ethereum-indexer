#!/usr/bin/env python
from extract import Extract
from transform import Transform
from load import Load

UPDATE_FREQUENCY = 60  # in seconds


def main():
    extract = Extract(["0x"], UPDATE_FREQUENCY)
    transform = Transform(extract)
    load = Load(transform)

    # * should be running in parallel
    extract()
    transform()
    load()


if __name__ == "__main__":
    main()
