# Run custom code in the pipeline
from typing import Any, Callable, Iterator, List


class Custom(object):
    def __init__(self, custom_func: Callable[[Any], Any]) -> None:
        self.custom_func = custom_func

    def process(self, documents: List[Any]) -> Iterator[Any]:
        for document in documents:
            yield self.custom_func(document)
