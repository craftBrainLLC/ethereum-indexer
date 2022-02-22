from typing import List


def remove_duplicates(lst: List[str]):
    return list(dict.fromkeys(lst))
