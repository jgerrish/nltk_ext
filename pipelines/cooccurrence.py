# The co-occurrence pipeline module builds a co-occurrence graph
# of values, indicating which ones occur together
from nltk_ext.graph import Graph
from nltk_ext.pipelines.pipeline_module import (
    enumModuleType,
    enumModuleProcessingType,
    PipelineModule,
)


class CooccurrencePipeline(PipelineModule):
    def __init__(self, output=None):
        self.output = output
        self.cooccur_graph = Graph()
        self.module_type = enumModuleType(enumModuleType.Document)
        self.module_processing_type = enumModuleProcessingType(
            enumModuleProcessingType.PostProcess
        )

    def process(self, source, data, attribute="categories"):
        if attribute in data.document:
            d = data.document[attribute]
            for v1 in d:
                for v2 in d:
                    self.cooccur_graph.inc_edge(v1, v2)

    # method that gets run after all data has been processed
    # TODO: look into optimizing this, seems inefficient, written in derp-mode
    def post_process(self):
        return self.cooccur_graph

    def write(self):
        if self.output is not None:
            f = open(self.output, "w")
            f.write(self.cooccur_graph.as_edgelist())
            f.close()
