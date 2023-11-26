# HTML to text module for converting HTML documents to text
import copy
from boilerpy3.extractors import ArticleExtractor
from typing import Iterator, List, Union

from nltk_ext.documents.document import Document


class BoilerpipeExtractor:
    def __init__(
        self, attribute: str = "body", new_attribute: str = "body_text"
    ) -> None:
        self.attribute = attribute
        self.new_attribute = new_attribute

    def process_text(self, text: str) -> str:
        if text == "":
            return text
        extractor = ArticleExtractor()
        new_val = extractor.get_content(text)
        return new_val

    def process(
        self,
        documents: List[Union[Document, str]],
    ) -> Iterator[Union[str, Document]]:
        for document in documents:
            if type(document) == str:
                s = document
                yield self.process_text(s)
                continue
            elif isinstance(document, Document):
                d = copy.copy(document)
                if self.attribute in d:
                    text = d[self.attribute]
                    new_val = self.process_text(text)
                    d.set(self.new_attribute, new_val)
                    yield d
                    continue
                else:
                    d.set(self.new_attribute, "")
                    yield d
                    continue
