# A random filter that drops a random number of documents based on
# simple uniform probability distribution
from typing import Any, Callable, Iterator, List, Optional

from nltk_ext.filters.filter import Filter
import random


class RandomFilter(Filter):
    # Initialize the RandomFilter with a drop probability,
    # probability is the drop probability
    def __init__(
        self,
        probability: float = 0.8,
        randgen: Optional[Callable[[], float]] = None,
    ) -> None:
        self.probability = probability
        self.randgen = randgen
        if self.randgen is None:
            self.randgen = random.random

    def filter(self, elements: List[Any]) -> Iterator[Any]:
        for elem in elements:
            if self.randgen is not None:
                rnd = self.randgen()
                if rnd >= self.probability:
                    yield elem
            else:
                raise Exception("No random number generator")

    def process(self, docs: Any, data: Any = None) -> Iterator[Any]:
        return self.filter(docs)

    # def filter(self, elem):
    #    if self.randgen:
    #        rnd = self.randgen()
    #    else:
    #        rnd = self.r.random()
    #    return rnd >= self.probability
