"""You write the logic for handling the state here"""

class Transform:
  """
    Takes a config dict to perform its work.
    The dict must include the following information:
      - event abis of interest
      - arbitrary name and version to identify this state
    Like extract, it runs indefinitely. It checks the database
      every 5 seconds to see if there are any new transactions
      that require transforming.
  """

  def __init__(self):
    ...

  def __call__(self):
    ...
