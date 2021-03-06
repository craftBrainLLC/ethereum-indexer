from typing import Dict, List, Any
import requests
import logging
import os

from interfaces.iextract import IExtract
from load.main import Load
from utils.address import validate_address
from utils.misc import remove_duplicates
from db import DB

# todo: eventually would want each extractor running in its own process
# for now the solution around that would be to simply run this pipeline
# multiple times

# * notes
# - possible to pull from a different blockchain if `chain_id` is different
# - `block_signed_at=false` pulls all transactions putting most recent ones
# at the top
COVALENT_TRANSACTIONS_URI = (
    lambda address, page_number: f'https://api.covalenthq.com/v1/1/address/{address}/transactions_v2/?quote-currency=USD&format=JSON&block-signed-at-asc=false&no-logs=false&page-number={page_number}&key={os.environ["COVALENT_API_KEY"]}&page-size=100'
)


class Extract(IExtract):
    def __init__(self, address: List[str]):
        """
        Args:
            address (List[str]): list of addresses for which to extract the raw historical
        transaction data.
        """
        # Validate the addresses. https://github.com/ethereum/web3.py/blob/71ef3cd7edc299be64a8767c2a354a56c552555c/tests/core/utilities/test_validation.py#L11
        # Store the address
        self._validate_address(address)

        self._address: List[str] = address
        # block number up to which the extraction has happened
        self._block_height: Dict[str, int] = dict(
            zip(self._address, [0 for _ in self._address])
        )

        self._db_name = "ethereum-indexer"

        self._db = DB()
        self._load = Load()

    def __setattr__(self, key, value):
        # https://towardsdatascience.com/how-to-create-read-only-and-deletion-proof-attributes-in-your-python-classes-b34cd1019c2d

        # re-setting the _address, _db_name, _db, _load is not allowed
        forbid_reset_on = ["_address", "_db_name", "_db", "_load"]
        for k in forbid_reset_on:
            if key == k and hasattr(self, k):
                raise AttributeError(
                    "The value of the address attribute has already been set, and can not be re-set."
                )

        if key == "_block_height":
            self.__dict__[key] = int(value)

        self.__dict__[key] = value

    def _validate_address(self, address: List[str]) -> None:
        """_summary_

        Args:
            address (List[str]): _description_

        Raises:
            InvalidAddress: _description_
            ValueError: _description_
        """

        for a in address:
            validate_address(a)

        # * ensures there are no duplicate addresses
        # * note that if multiple instances of the pipeline
        # are running with duplicate addresses, that **will**
        # cause errors
        without_dupes = remove_duplicates(address)

        if len(without_dupes) != len(address):
            raise ValueError("There can't be duplicates in address", address)

    def _get_block_height_collection_name(self, address: str) -> str:
        return f"{address}-block-height"

    def _determine_block_height(self) -> None:
        """
        Goes through each address and determines its `block_height` value.
        This ensures we do not extract all the data all the time, but only
        the new stuff. This is also helpful in case the binary raises and
        we need to restart it.
        """

        for addr in self._address:
            block_height = self._db.get_any_item(
                self._db_name, self._get_block_height_collection_name(addr)
            )
            # If it is None, then we have already set it to 0 in the
            # __init__. This will signal the extractor to extract
            # the complete history of the address
            if block_height is None:
                continue

            self._block_height[addr] = block_height

    def _update_block_height(self, new_block_height: int, for_address: str) -> None:
        """
        After extracting the transactions update the db with the latest block height.

        Args:
            new_block_height (int): _description_
            for_address (str): _description_
        """

        collection_name = self._get_block_height_collection_name(for_address)
        # _id: 1, because we are only ever storing single block_height value per address
        item = {"_id": 1, "block_height": new_block_height}
        self._db.put_item(item, self._db_name, collection_name)

    # todo: return type here
    def _request_transactions(self, for_address: str, page_number: int) -> Any:
        """
        Response looks like this
            "data": {
                "address": "0x94d8f036a0fbc216bb532d33bdf6564157af0cd7",
                "updated_at": "2022-02-22T12:29:52.068887528Z",
                "next_update_at": "2022-02-22T12:34:52.068887688Z",
                "quote_currency": "USD",
                "chain_id": 1,
                "items": [<transaction>, ...],
                "pagination": {
                    "has_more": true,
                    "page_number": 0,
                    "page_size": 100,
                    "total_count": null
                },
                "error": false,
                "error_message": null,
                "error_code": null
            }

        Args:
            for_address (str): _description_
            page_number (int): _description_

        Returns:
            Any: _description_
        """
        request_uri = COVALENT_TRANSACTIONS_URI(for_address, page_number)

        # todo: check the status code
        response = requests.get(request_uri)

        return response

    def _extract_txn_history_since(self, block_height: int, for_address: str) -> None:
        """
        Makes requests to Covalent, and only extracts transactions after `block_height`

        Args:
            block_height (int): _description_
            for_address (str): _description_
        """

        logging.info(f"[EXTRACTING] {for_address} since block: {block_height}")

        latest_block_height = -1

        # todo: new_block_height
        new_block_height = 1
        self._update_block_height(new_block_height, for_address)

    # Interface Implementation

    def flush(self) -> None:
        return

    def extract(self) -> None:
        """
        Extracts transactions for all self._address
        """

        # Running this ensures we know what transactions to extract in the code
        # will follow. This avoids extracting all the transactions all the time.
        self._determine_block_height()

        # - check if the db has transactions, if it has, then download the new ones
        # if it doesn't have any transactions, download all
        # - we utilise a separate collection to track what raw transactions have
        # been extracted
        for addr in self._address:
            block_height = self._block_height[addr]
            self._extract_txn_history_since(block_height, addr)
