# HTML to text module for converting HTML documents to text
from bs4 import BeautifulSoup

from nltk_ext.pipelines.pipeline_module import (
    PipelineModule,
    ProcessElementsType,
    ProcessAttributesType,
    ProcessReturnType,
)


class HtmlToTextPipeline(PipelineModule):
    def __init__(self, attribute: str = "soup") -> None:
        self.parser: str = "lxml"
        self.attribute = attribute

        return

    def clean(self) -> None:
        [s.extract() for s in self.soup("script")]

    def process(
        self,
        elements: ProcessElementsType,
        attributes: ProcessAttributesType = None,
    ) -> ProcessReturnType:
        for doc in elements:
            if type(doc) == str:
                self.soup = BeautifulSoup(doc, self.parser)
            else:
                self.soup = BeautifulSoup(str(doc), self.parser)
            self.clean()
            yield self.soup.get_text()  # .encode('ascii', 'ignore')
