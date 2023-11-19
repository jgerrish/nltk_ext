# A blacklist filter to filter out data
# This module also supports the Pipeline interface
#
# The Filter interface expects Filter classes to provide a method
# filter that takes a single element and returns True if the element
# should be included and False if it should be filtered out
from nltk.corpus import stopwords
from nltk_ext.pipelines.pipeline_module import PipelineModule


class StopwordFilter(PipelineModule):
    def __init__(self, lang="english"):
        self.stopwords = stopwords.words(lang)

    def filter(self, elements):
        for elem in elements:
            if elem not in self.stopwords:
                yield elem

    def process(self, elements, data=None):
        return self.filter(elements)
