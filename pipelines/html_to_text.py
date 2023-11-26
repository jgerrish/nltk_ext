# HTML to text module for converting HTML documents to text
from bs4 import BeautifulSoup
from typing import Iterator, List, Optional, Union

from nltk_ext.documents.document import Document
from nltk_ext.pipelines.pipeline_module import PipelineModule


class HtmlToTextPipeline(PipelineModule):
    def __init__(self, attribute: str = "soup") -> None:
        self.parser: str = "lxml"
        self.attribute = attribute

        return

    def clean(self) -> None:
        [s.extract() for s in self.soup("script")]

    def process(
        self,
        data: Union[List[str], List[Document]],
        attributes: Optional[List[str]] = None,
    ) -> Iterator[Union[str, Document]]:
        for doc in data:
            if type(doc) == str:
                self.soup = BeautifulSoup(doc, self.parser)
            else:
                self.soup = BeautifulSoup(str(doc), self.parser)
            self.clean()
            yield self.soup.get_text()  # .encode('ascii', 'ignore')
