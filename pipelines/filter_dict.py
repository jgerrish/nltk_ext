# filter a dictionary down to a select list of keys
# useful for processing large sets of documents in memory
from typing import Any, Iterator, List, Optional


# pipeline module to filter a dictionary by keys
class FilterDict(object):
    def __init__(self, keys: Optional[List[str]] = None) -> None:
        self.keys = keys

    def process(self, documents: List[Any]) -> Iterator[Any]:
        for document in documents:
            if self.keys is not None:
                d = {key: document[key] for key in self.keys}
                yield d
            else:
                yield document
