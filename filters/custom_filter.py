# Filter documents using a custom filter function
from nltk_ext.pipelines.pipeline_module import enumModuleType, enumModuleProcessingType, PipelineModule

class CustomFilter(PipelineModule):
    """
    Filter documents using a custom function supplied to this class.
    The filter function accepts a single parameter, the element to
    test.  It should return true if the element should be passed along the
    pipeline, and false if it should be ignored.
    """
    def __init__(self, custom_func):
        self.custom_func = custom_func

    def filter(self, elements):
        for elem in elements:
            if self.custom_func(elem):
                yield elem

    def process(self, elements, data=None):
        return self.filter(elements)
