from abc import abstractmethod
from enum import Enum
from typing import Any, Callable, Iterator, List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from nltk_ext.documents.document import Document

from nltk_ext.util import consume


class enumModuleType(Enum):
    """
    This enumeration specifies the pipeline module type.
    """

    Document = 0
    Sentence = 1
    Word = 2


class enumModuleProcessingType(Enum):
    """
    This enumeration type indicates at what point in the processing
    pipeline the module has data ready.

    Right now there are two options: after each iteration of
    process(), or at the end of processing via post_process()
    """

    Process = 0
    PostProcess = 1


# TODO Add more checks around this.
# TODO make sure aligned with the CustomFilter init (e.g. union of lists of
# list of unions) and other callback users.
CallbackType = Callable[[Union[List[str], List["Document"]], List[str]], Any]

# The function signature for the process method
# Defining these here is easier for maintenance, but
# it makes understanding what they do in each individual subclass more
# difficult.
ProcessElementsType = Union[List[str], List["Document"]]
ProcessAttributesType = Optional[List[str]]
ProcessReturnType = Iterator[Union[Any, "Document"]]

ProcessIteratorElementsType = Union[Iterator[str], Iterator["Document"]]
ProcessIteratorAttributesType = Optional[Iterator[str]]
ProcessIteratorReturnType = Iterator[Union[Any, "Document"]]


class PipelineModule:
    """
    Abstract base class for pipeline modules
    Concrete classes must implement a process method

    The process method is called for each document, sentence or word
    depending on the module type.
    """

    def __init__(self) -> None:
        self.before_process_callbacks: List[CallbackType] = []
        self.after_process_callbacks: List[CallbackType] = []

    @abstractmethod
    def process(
        self,
        elements: ProcessElementsType,
        attributes: ProcessAttributesType = None,
    ) -> ProcessReturnType:
        for cb in self.before_process_callbacks:
            cb(elements, attributes)

        # res = self._process(elements, attributes)
        res = ""

        for cb in self.after_process_callbacks:
            cb(elements, attributes)

        yield res

    @abstractmethod
    def process_iterator(
        self,
        elements: ProcessIteratorElementsType,
        attributes: ProcessIteratorAttributesType = None,
    ) -> ProcessIteratorReturnType:
        # TODO Fix up these list calls, they shouldn't be necessary
        for cb in self.before_process_callbacks:
            cb(elements, attributes)  # type: ignore[arg-type]

        # res = self._process(elements, attributes)
        res = ""

        for cb in self.after_process_callbacks:
            cb(elements, attributes)  # type: ignore[arg-type]

        yield res

    def consume_process(
        self,
        elements: Union[List[str], List["Document"]],
        attributes: Optional[List[str]] = None,
    ) -> None:
        """
        Consume every element in the process pipeline.
        Returns no results.
        """
        consume(self.process(elements, attributes))

    def add_before_process_callback(self, cb: CallbackType) -> None:
        self.before_process_callbacks.append(cb)

    def add_after_process_callback(self, cb: CallbackType) -> None:
        self.after_process_callbacks.append(cb)

    def process_all(
        self,
        data: Union[List[str], List["Document"]],
        attributes: Optional[List[str]],
    ) -> None:
        for d in self.process(data, attributes):
            continue
