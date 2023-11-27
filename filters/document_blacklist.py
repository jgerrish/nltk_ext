# A Document blacklist filter to filter out documents
#
# Filters out documents based on a regular expression blacklist
# if the given attribute matches one of the regular expressions, the
# document is rejected
# attribute and one of the blacklist parameters are required arguments
import re
from typing import Any, Iterator, List, Optional, Union

from nltk_ext.documents.document import Document
from nltk_ext.filters.filter import Filter


class DocumentBlacklist(Filter):
    def __init__(
        self,
        attribute: Optional[str] = None,
        blacklist: Optional[List[str]] = None,
        blacklist_fn: str = "blacklist.txt",
    ) -> None:
        bl = []
        if (blacklist_fn is not None) and (blacklist is None):
            with open(blacklist_fn, "r") as f:
                bl = f.read().split("\n")
                # convert list to a set
        elif blacklist is not None:
            bl = blacklist
        self.blacklist = set(bl)
        self.attribute = attribute
        self.init_regexes(bl)

    def init_regexes(self, blacklist: List[str]) -> None:
        """
        Right now, use a simple list of regexes and check in sequence
        Use more efficient methods later
        """
        self.regex_blacklist = []
        for bl in blacklist:
            if bl != "":
                self.regex_blacklist.append(re.compile(bl))

    def filter(
        self, documents: Union[List[str], List[Document]]
    ) -> Iterator[Union[Document, str]]:
        for document in documents:
            match = False
            if isinstance(document, Document) and (self.attribute in document):
                for bl in self.regex_blacklist:
                    if bl.match(document[self.attribute]) is not None:
                        match = True
            if not match:
                yield document

    def process(self, documents: Any, data: Any = None) -> Iterator[Any]:
        return self.filter(documents)
