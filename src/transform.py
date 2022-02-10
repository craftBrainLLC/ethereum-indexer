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


class Transform:
    """
    Takes a config dict to perform its work.
    The dict must include the following information:
      - event abis of interest
    Like extract, it runs indefinitely. It checks the database
      every 5 seconds to see if there are any new transactions
      that require transforming.
    """

    def __init__(self):
        ...

    def __call__(self):
        ...
