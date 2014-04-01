# The Index module builds an index of terms to documents
from nltk_ext.graph import Graph
from nltk_ext.pipelines.pipeline_module import enumModuleType, enumModuleProcessingType, PipelineModule

class Index(PipelineModule):
    def __init__(self):
        self.module_type = enumModuleType(enumModuleType.Document)
        self.module_processing_type = \
            enumModuleProcessingType(enumModuleProcessingType.PostProcess)
        self.index = {}

    def process(self, source, data, attribute="body_text"):
        if attribute in data.document:
            words = data.words()
            for word in words:
                if word not in self.index:
                    self.index[word] = [source]
                else:
                    self.index[word].append(source)

    # method that gets run after all data has been processed
    def post_process(self):
        return self.index

class IndexAttributes(PipelineModule):
    def __init__(self):
        self.module_type = enumModuleType(enumModuleType.Document)
        self.module_processing_type = \
            enumModuleProcessingType(enumModuleProcessingType.PostProcess)
        self.index = {}

    def process(self, source, data, attribute="categories"):
        if attribute in data.document:
            d = data.document[attribute]
            for v1 in d:
                if v1 not in self.index:
                    self.index[v1] = [source]
                else:
                    self.index[v1].append(source)

    # method that gets run after all data has been processed
    def post_process(self):
        return self.index
