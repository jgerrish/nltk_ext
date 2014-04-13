# add_to_corpus is a pipeline module that adds documents to a corpus
from nltk_ext.documents.document import Document
from nltk_ext.corpus.corpus import Corpus
from nltk_ext.pipelines.pipeline_module import enumModuleType, enumModuleProcessingType, PipelineModule

class AddToCorpus(PipelineModule):
    def __init__(self, output=None, corpus=None):
        self.output = output
        self.corpus = Corpus() if (corpus == None) else corpus
        self.module_type = enumModuleType(enumModuleType.Document)
        self.module_processing_type = \
            enumModuleProcessingType(enumModuleProcessingType.PostProcess)

    def process(self, data):
        for document in data:
            print data
            self.corpus.add(data)

    def post_process(self):
        return self.corpus

    def as_json(self):
        json.dumps(self.corpus, sort_keys=True, indent=4, separators=(',', ': '))

    def write(self):
        if self.output != None:
            f = open(self.output, 'w')
            f.write(self.as_json())
            f.close()
