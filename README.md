# ethereum-indexer

Personal blockchain indexer to not depend on services like The Graph, which proved to be incredibly unreliable.

Currently, only supports Ethereum mainnet.

## How It Works

**[Raw Txn Data]** All transactions for a given address are downloaded and stored in Python's SQLite db. This process does not terminate when it has downloaded all the data. It runs to RPC poll for any new blocks containing our address.

**[Maintaining State]** Next, according to the rules of how to parse the above, state starts to build up. Once it catched up with the head of the blockchain, it continues to run checking in the db if there were any new raw txn data entries from the above.

**[Serving State]** `graphql` server is spawned up with which you can query all the above state. Each response item will contain the block number, to indicate up to what block number the response state is valid.
