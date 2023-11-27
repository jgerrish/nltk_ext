# Module to return uniq elements given a list of elements
# Stores every item seen in the stream, for large collections,
# use the RedisUniq Redis-backed uniq module
from typing import Set

from nltk_ext.pipelines.pipeline_module import (
    PipelineModule,
    ProcessElementsType,
    ProcessAttributesType,
    ProcessReturnType,
)


class Uniq(PipelineModule):
    def __init__(self) -> None:
        self.items: Set = set()

    def process(
        self,
        elements: ProcessElementsType,
        attributes: ProcessAttributesType = None,
    ) -> ProcessReturnType:
        for s in elements:
            if s not in self.items:
                self.items.add(s)
                yield s
