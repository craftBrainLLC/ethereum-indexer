#!/usr/bin/env python
from extract import Extract
from transform import Transform
from load import Load

SECOND = 1


def main():
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

    # run in the same process
    extract = Extract(extract_txns_for_these, update_frequencies)
    load_extracted = Load(extract)

    # run in a different process, but both in the same one
    transform = Transform()
    load_transformed = Load(transform)

    # * should be running in parallel
    extract()
    load_extracted()

    transform()
    load_transformed()


if __name__ == "__main__":
    main()
