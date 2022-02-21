#!/usr/bin/env python
from multiprocessing import Process
import logging

from extract.main import Extract
from transform.main import Transform

SECOND = 1


def main():
    logging.basicConfig(
        level=logging.DEBUG, format="%(relativeCreated)6d %(process)d %(message)s"
    )

    # extraction details. Multiplying by second for readability of code
    # rkl is the main rumble kong league collection
    # azrael is renft's v1 collateral solution
    # sylvester is renft's v1 collateral free solution
    # renft is a leading p2p nft rentals protocol
    extract_txns_for_these = [
        "0xEf0182dc0574cd5874494a120750FD222FdB909a",  # rkl
        "0x94D8f036a0fbC216Bb532D33bDF6564157Af0cD7",  # azrael
        "0xa8D3F65b6E2922fED1430b77aC2b557e1fa8DA4a",  # sylvester
    ]
    update_frequencies = [30 * SECOND, 60 * SECOND, 120 * SECOND]

    # goal: avoid cross process communication
    #
    # solution 1: Make extract and load asynchronous. Not ideal because
    # that introduces a notch of complexity
    #
    # solution 2: Thread the tasks. They would share the context, so it
    # will be easy to share the resources (extracted data; or transformed
    # data). Does not add to complexity as much as other options.
    #
    # solution 3: ignore separation of concerns and have load be part
    # of the interfaces that are required to be persisted. Even though,
    # this is not ideal. I like this solution the best. This is the
    # solution I will go with.

    def extract_and_load():
        extract = Extract(extract_txns_for_these, update_frequencies)
        extract()

    def transform_and_load():
        transform = Transform()
        transform()

    # todo: graceful keyboard interrupt
    p1 = Process(target=extract_and_load)
    p2 = Process(target=transform_and_load)
    p1.start()
    p2.start()
    p1.join()
    p2.join()


if __name__ == "__main__":
    main()
