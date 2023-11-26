# HTML Cleaner module for cleaning HTML documents before conversion
# TODO: Clean up pipeline interface, separate word/document processing
import copy
import pprint
import re

from nltk_ext.documents.document import Document
from nltk_ext.pipelines.pipeline_module import (
    PipelineModule,
    ProcessElementsType,
    ProcessAttributesType,
    ProcessReturnType,
)


class HtmlCleaner(PipelineModule):
    def __init__(self, attribute: str = "body") -> None:
        self.attribute = attribute
        self.regexp = re.compile(r"<[bB][rR]\s*\/?\s*>")
        self.pp = pprint.PrettyPrinter(indent=4)

    def process(
        self,
        elements: ProcessElementsType,
        attributes: ProcessAttributesType = None,
    ) -> ProcessReturnType:
        for document in elements:
            if type(document) == str:
                s = document
                if s != "":
                    s = self.regexp.sub("\n", s)
                yield s
            else:
                if isinstance(document, Document):
                    d = copy.copy(document)
                if isinstance(d, Document) and (self.attribute in d):
                    new_val = self.regexp.sub("\n", d[self.attribute])
                    d.set(self.attribute, new_val)
                yield d
