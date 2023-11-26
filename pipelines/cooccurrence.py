# The co-occurrence pipeline module builds a co-occurrence graph
# of values, indicating which ones occur together
from typing import Any, Iterator, List, Union

from nltk_ext.documents.document import Document
from nltk_ext.graph import Graph
from nltk_ext.pipelines.pipeline_module import (
    enumModuleType,
    enumModuleProcessingType,
)


class CooccurrencePipeline:
    def __init__(self, output: str = None) -> None:
        self.output = output
        self.cooccur_graph = Graph()
        self.module_type = enumModuleType.Document
        self.module_processing_type = enumModuleProcessingType.PostProcess

    def process(
        self,
        source: Any,
        data: Union[List[str], List[Document]],
        # data: Union[Document, str],
        attribute: str = "categories",
        # self,
        # source: Any,
        # data: Union[List[str], List[Document]],
        # attributes: Optional[List[str]] = None,
    ) -> Iterator[Union[str, Document]]:
        for doc in data:
            if isinstance(doc, Document):
                document = doc
            elif type(doc) == str:
                document = Document(doc)
            if attribute in document:
                attr = document[attribute]
                for v1 in attr:
                    for v2 in attr:
                        self.cooccur_graph.inc_edge(v1, v2)
            yield document

    # method that gets run after all data has been processed
    # TODO: look into optimizing this, seems inefficient, written in derp-mode
    def post_process(self) -> Graph:
        return self.cooccur_graph

    def write(self) -> None:
        if self.output is not None:
            f = open(self.output, "w")
            f.write(self.cooccur_graph.as_edgelist())
            f.close()
