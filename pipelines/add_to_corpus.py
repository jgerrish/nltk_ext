# add_to_corpus is a pipeline module that adds documents to a corpus
import json
from nltk_ext.corpus.corpus import Corpus
from nltk_ext.pipelines.pipeline_module import (
    enumModuleType,
    enumModuleProcessingType,
    PipelineModule,
)


class AddToCorpus(PipelineModule):
    def __init__(self, output=None, corpus=None):
        self.output = output
        self.corpus = Corpus() if (corpus is None) else corpus
        self.module_type = enumModuleType.Document
        self.module_processing_type = enumModuleProcessingType.PostProcess

    def process(self, data):
        for document in data:
            self.corpus.add(document)

    def post_process(self):
        return self.corpus

    def as_json(self):
        json.dumps(
            self.corpus,
            sort_keys=True,
            indent=4,
            separators=(",", ": "),
        )

    def write(self):
        if self.output is not None:
            f = open(self.output, "w")
            f.write(self.as_json())
            f.close()
