from typing import Any, List

from nltk_ext.pipelines.pipeline_module import (
    PipelineModule,
    ProcessElementsType,
    ProcessAttributesType,
    ProcessReturnType,
)


class Recorder(PipelineModule):
    """
    Recorder pipeline module that records the current state of the
    pipeline data at a stage in the pipeline.
    Useful for testing pipeline processing and pulling out intermediate
    data.
    """

    def __init__(self, data: List[Any] = []) -> None:
        self.data = data

    def get_data(self) -> Any:
        "Return the recorded data"
        return self.data

    def clear_data(self) -> None:
        "Clear the recorded data"
        self.data = []

    def process(
        self,
        elements: ProcessElementsType,
        attributes: ProcessAttributesType = None,
    ) -> ProcessReturnType:
        for s in elements:
            self.data.append(s)
            yield s
