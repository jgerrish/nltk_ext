import pprint
from typing import Any, Callable, Iterator, List, Optional


class StdoutWriter(object):
    """
    Pipeline module to print out items
    """

    def __init__(self, formatter: Callable[[Any], Any] = None) -> None:
        if formatter:
            self.formatter = formatter
        else:
            self.pp = pprint.PrettyPrinter(indent=4)
            self.formatter = self.pp_formatter

    def pp_formatter(self, data: str) -> str:
        return self.pp.pformat(data)

    def process(self, source: List[Any], data: Optional[Any] = None) -> Iterator[Any]:
        for s in source:
            print("data")
            print(str(s))  # self.formatter(s)
            yield self.formatter(s)
