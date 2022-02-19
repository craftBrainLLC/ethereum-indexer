"""You specify which transformers to use from the transformers
directory. Each transformer must sit in its separate folder and
must include a main.py file that describes the handlers for the
events. There also must be a config file in that directory.

Name your files such that there is a part that gives your
transformer recognisable slug and a part that versions them.

Only those transformers that are specified by the user will be
used (i.e. not all of the transformers will be used).

Example:

src
 |
 |transformers
 |  |
 |  |rumble-kong-league-0.0.1
 |  | |
 |  | |main.py
 |  | |config.json
 |  | |

Where ``config.json`` looks like

...

And ``main.py`` looks like

...
"""
import time

from interfaces.itransform import ITransform


class Transform(ITransform):
    """
    Takes a config dict to perform its work.
    The dict must include the following information:
      - event abis of interest
    Like extract, it runs indefinitely. It checks the database
      every 5 seconds to see if there are any new transactions
      that require transforming.
    No need to provide any paths, since it will look for
    required filed in `transformers` folder.
    """

    def __init__(self):
        ...

    def __call__(self):
        """
        Before transforming, ensure that configs' addresses are all
        in the database. If they are not, produce soft warning and
        continue working on the ones that are in the database.
        """
        while True:
            print("transforming")
            time.sleep(1)
