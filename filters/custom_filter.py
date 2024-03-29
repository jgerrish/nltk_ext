from typing import Callable, Union

# Filter documents using a custom filter function
from nltk_ext.documents.document import Document
from nltk_ext.filters.filter import Filter
from nltk_ext.pipelines.pipeline_module import (
    ProcessElementsType,
    ProcessAttributesType,
    ProcessReturnType,
)


class CustomFilter(Filter):
    """
    Filter documents using a custom function supplied to this class.
    The filter function accepts a single parameter, the element to
    test.  It should return true if the element should be passed along the
    pipeline, and false if it should be ignored.
    """

    def __init__(self, custom_func: Callable[[Union[str, Document]], bool]) -> None:
        self.custom_func = custom_func

    def filter(
        self,
        elements: ProcessElementsType,
        attributes: ProcessAttributesType = None,
    ) -> ProcessReturnType:
        for elem in elements:
            if self.custom_func(elem):
                yield elem

    def process(
        self,
        elements: ProcessElementsType,
        attributes: ProcessAttributesType = None,
    ) -> ProcessReturnType:
        return self.filter(elements)
