# HTML Cleaner module for cleaning HTML documents before conversion
# TODO: Clean up pipeline interface, separate word/document processing
import copy
from typing import Any, Iterator, List

from nltk_ext.documents.html_document import HTMLDocument


class CreateDocument(object):
    def __init__(
        self,
        document_class: Any = HTMLDocument,
        attribute: str = "body",
    ) -> None:
        self.document_class = document_class
        self.attribute = attribute

    def process(self, documents: List[Any]) -> Iterator[Any]:
        for document in documents:
            if type(document) == str:
                d = {self.attribute: document}
            else:
                d = copy.copy(document)
            doc = self.document_class(d)
            yield doc
