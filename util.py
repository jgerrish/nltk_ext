from collections import deque
from itertools import islice
from typing import Any, Iterator, Set


class Util:
    @staticmethod
    def jaccard(s1: Set, s2: Set) -> float:
        """Static method for Jaccard distance"""
        union = len(s1.union(s2))
        inter = len(s1.intersection(s2))
        if union == 0:
            return 0.0
        else:
            return float(inter) / float(union)


def consume(iterator: Iterator[Any], n: int = None) -> None:
    """Advance the iterator n-steps ahead.  If n i None, consume entirely."""
    # Copied directly from the Python itertools documentation
    # Use functions that consume iterators at C speed.
    if n is None:
        # feed the entire iterator into a zero-length deque
        deque(iterator, maxlen=0)
    else:
        next(islice(iterator, n, n), None)
