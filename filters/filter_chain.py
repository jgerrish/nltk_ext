from typing import Any, List

from nltk_ext.filters.filter import Filter


class FilterChain:
    def __init__(self, filters: List[Filter] = []) -> None:
        self.filters = filters

    def add(self, f: Filter) -> None:
        self.filters.append(f)

    def check(self, data: List[Any]) -> bool:
        for f in self.filters:
            if not f.filter(data):
                return False
        return True
