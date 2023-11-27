# A blacklist filter to filter out data
# This module also supports the Pipeline interface
#
# The Filter interface expects Filter classes to provide a method
# filter that takes a single element and returns True if the element
# should be included and False if it should be filtered out
from typing import Any, Iterator, List, Optional
from nltk.corpus import stopwords

from nltk_ext.filters.filter import Filter


class StopwordFilter(Filter):
    def __init__(self, lang: str = "english") -> None:
        self.stopwords = stopwords.words(lang)

    def filter(self, elements: List[Any]) -> Iterator[Any]:
        for elem in elements:
            if elem not in self.stopwords:
                yield elem

    def process(self, elements: Any, data: Optional[Any] = None) -> Iterator[Any]:
        return self.filter(elements)
