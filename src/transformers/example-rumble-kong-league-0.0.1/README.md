# Example

`config.json` may include more than one address, because, perhaps you need to build state from more than one source. Or, you may simply want to build a single indexer for all your contracts. This list of strings goes into the `address` key in the `config.json`. Note, that extractor also takes a list of strings for `address`. You need to supply **all** the addresses across all of your indexers in there. Extractor is responsible for extracting raw transactions from the Ethereum blockchain for all of these addresses and saving them into the db whose collection name is precisely the `address`.

