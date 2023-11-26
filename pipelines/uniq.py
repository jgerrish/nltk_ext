# Module to return uniq elements given a list of elements
# Stores every item seen in the stream, for large collections,
# use the RedisUniq Redis-backed uniq module
from typing import Any, Iterator, List, Set


class Uniq(object):
    def __init__(self) -> None:
        self.items: Set = set()

    def process(self, data: List[Any]) -> Iterator[Any]:
        for s in data:
            if s not in self.items:
                self.items.add(s)
                yield s
