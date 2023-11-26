# The Index module builds an index of terms to documents
from typing import Any, Dict, List

from nltk_ext.documents.document import Document
from nltk_ext.pipelines.pipeline_module import (
    enumModuleType,
    enumModuleProcessingType,
)

IndexType = Dict[str, List[str]]


class Index:
    def __init__(self) -> None:
        self.module_type = enumModuleType.Document
        self.module_processing_type = enumModuleProcessingType.PostProcess
        self.index: IndexType = {}

    def process(
        self,
        source: str,
        data: Document,
        attribute: str = "body_text",
    ) -> None:
        if attribute in data.document:
            words = data.words()
            for word in words:
                if word not in self.index:
                    self.index[word] = [source]
                else:
                    self.index[word].append(source)

    # method that gets run after all data has been processed
    def post_process(self) -> IndexType:
        return self.index


class IndexAttributes:
    def __init__(self) -> None:
        self.module_type = enumModuleType.Document
        self.module_processing_type = enumModuleProcessingType.PostProcess
        self.index: Dict[Any, Any] = {}

    def process(
        self,
        source: str,
        data: Document,
        attribute: str = "categories",
    ) -> None:
        if attribute in data.document:
            d = data.document[attribute]
            for v1 in d:
                if v1 not in self.index:
                    self.index[v1] = [source]
                else:
                    self.index[v1].append(source)

    # method that gets run after all data has been processed
    def post_process(self) -> Dict[Any, Any]:
        return self.index
