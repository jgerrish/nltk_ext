# A blacklist filter to filter out data
#
# The Filter interface expects Filter classes to provide a method
# filter that takes a single element and returns True if the element
# should be included and False if it should be filtered out
from typing import Iterator, List, Optional

from nltk_ext.filters.filter import Filter


class BlacklistFilter(Filter):
    def __init__(
        self,
        blacklist: Optional[List[str]] = None,
        blacklist_fn: str = "blacklist.txt",
    ) -> None:
        bl = []
        if (blacklist_fn is not None) and (blacklist is None):
            with open(blacklist, "r") as f:
                bl = f.read().split("\n")
                # convert list to a set
        elif blacklist is not None:
            bl = blacklist
        self.blacklist = set(bl)

    def filter(self, elements: List[str]) -> Iterator[str]:
        for elem in elements:
            if elem not in self.blacklist:
                yield elem
