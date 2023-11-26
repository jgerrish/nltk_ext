# Count number of characters in a document
from typing import Iterator, List, Optional, Union

from nltk_ext.documents.document import Document
from nltk_ext.pipelines.pipeline_module import PipelineModule


class CharCount(PipelineModule):
    def __init__(self, new_attribute: str = "char_count") -> None:
        self.new_attribute = new_attribute

    def process_text(self, text: str) -> int:
        return len(text)

    def process(
        self,
        documents: Union[List[str], List[Document]],
        attributes: Optional[List[str]] = None,
    ) -> Iterator[Union[int, Document]]:
        for document in documents:
            if type(document) == str:
                yield self.process_text(document)
            elif isinstance(document, Document):
                new_val = self.process_text(str(document))
                document.set(self.new_attribute, new_val)
                yield document
