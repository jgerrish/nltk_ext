# Count number of characters in a document
from nltk_ext.documents.document import Document
from nltk_ext.pipelines.pipeline_module import (
    PipelineModule,
    ProcessElementsType,
    ProcessAttributesType,
    ProcessReturnType,
)


class CharCount(PipelineModule):
    def __init__(self, new_attribute: str = "char_count") -> None:
        self.new_attribute = new_attribute

    def process_text(self, text: str) -> int:
        return len(text)

    def process(
        self,
        elements: ProcessElementsType,
        attributes: ProcessAttributesType = None,
    ) -> ProcessReturnType:
        for document in elements:
            if type(document) == str:
                yield self.process_text(document)
            elif isinstance(document, Document):
                new_val = self.process_text(str(document))
                document.set(self.new_attribute, new_val)
                yield document
