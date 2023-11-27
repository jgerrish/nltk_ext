# TODO Fix this up
# TODO Have the other filters subclass this

# A blacklist filter to filter out data
# This module also supports the Pipeline interface
#
# The Filter interface expects Filter classes to provide a method
# filter that takes a single element and returns True if the element
# should be included and False if it should be filtered out
from typing import Any, List, Iterator

from nltk_ext.pipelines.pipeline_module import (
    PipelineModule,
    ProcessElementsType,
    ProcessAttributesType,
    ProcessReturnType,
)


class Filter(PipelineModule):
    def __init__(self) -> None:
        pass

    # def filter(
    #     self,
    #     elements: ProcessElementsType,
    #     attributes: ProcessAttributesType = None,
    # ) -> ProcessReturnType:
    def filter(self, elements: List[Any]) -> Iterator[Any]:
        for elem in elements:
            yield elem

    def process(
        self,
        elements: ProcessElementsType,
        attributes: ProcessAttributesType = None,
    ) -> ProcessReturnType:
        return self.filter(elements)
