from eth_utils import is_checksum_address

from exceptions import InvalidAddress

# taken from: https://github.com/ethereum/web3.py/blob/71ef3cd7edc299be64a8767c2a354a56c552555c/web3/_utils/validation.py#L163
def validate_address(value: str) -> None:
    """
    Helper function for validating an address
    """
    # if is_bytes(value):
    #     if not is_binary_address(value):
    #         raise InvalidAddress("Address must be 20 bytes when input type is bytes", value)
    #     return

    # if not isinstance(value, str):
    #     raise TypeError(f'Address {value} must be provided as a string')

    # if not is_hex_address(value):
    #     raise InvalidAddress("Address must be 20 bytes, as a hex string with a 0x prefix", value)

    if not is_checksum_address(value):
        if value == value.lower():
            raise InvalidAddress(
                "Indexer only accepts checksum addresses. ",
                "The software that gave you this non-checksum address should be considered unsafe, ",
                "please file it as a bug on their platform. ",
                value,
            )
        else:
            raise InvalidAddress(
                "Address has an invalid EIP-55 checksum. ",
                "After looking up the address from the original source, try again.",
                value,
            )
