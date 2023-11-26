# add_to_corpus is a pipeline module that adds documents to a corpus
import json

from nltk_ext.corpus.corpus import Corpus
from nltk_ext.documents.document import Document
from nltk_ext.pipelines.pipeline_module import (
    enumModuleType,
    enumModuleProcessingType,
    PipelineModule,
    ProcessElementsType,
    ProcessAttributesType,
    ProcessReturnType,
)


class AddToCorpus(PipelineModule):
    def __init__(self, output: str = None, corpus: Corpus = None) -> None:
        self.output = output
        self.corpus = Corpus() if (corpus is None) else corpus
        self.module_type = enumModuleType.Document
        self.module_processing_type = enumModuleProcessingType.PostProcess

    def process(
        self,
        elements: ProcessElementsType,
        attributes: ProcessAttributesType = None,
    ) -> ProcessReturnType:
        for document in elements:
            if type(document) == str:
                self.corpus.add(Document(document))
                # TODO Think about design
                # ModuleType is document, so maybe this should return
                # a Document.
                yield document
            elif isinstance(document, Document):
                self.corpus.add(document)
                yield document
            else:
                print(type(document))

    def post_process(self) -> Corpus:
        return self.corpus

    def as_json(self) -> str:
        return json.dumps(
            self.corpus,
            sort_keys=True,
            indent=4,
            separators=(",", ": "),
        )

    def write(self) -> None:
        if self.output is not None:
            f = open(self.output, "w")
            f.write(self.as_json())
            f.close()
