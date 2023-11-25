from abc import abstractmethod
from enum import Enum
from typing import Any, Callable, Iterator, List, Optional, TYPE_CHECKING, Union

if TYPE_CHECKING:
    from nltk_ext.documents.document import Document


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


class PipelineModule:
    """
    Abstract base class for pipeline modules
    Concrete classes must implement a process method

    The process method is called for each document, sentence or word
    depending on the module type.
    """

    def __init__(self) -> None:
        self.before_process_callbacks: List[
            Callable[[Union[List[str], List["Document"]], List[str]], Any]
        ] = []
        self.after_process_callbacks: List[
            Callable[[Union[List[str], List["Document"]], List[str]], Any]
        ] = []

    @abstractmethod
    def process(
        self,
        elements: Union[List[str], List["Document"]],
        attributes: Optional[List[str]] = None,
    ) -> Iterator[Union[str, "Document"]]:
        for cb in self.before_process_callbacks:
            cb(elements, attributes)

        # res = self._process(elements, attributes)
        res = ""

        for cb in self.after_process_callbacks:
            cb(elements, attributes)

        yield res

    def add_before_process_callback(
        self,
        cb: Callable[[Union[List[str], List["Document"]], List[str]], Any],
    ) -> None:
        self.before_process_callbacks.append(cb)

    def add_after_process_callback(
        self,
        cb: Callable[[Union[List[str], List["Document"]], List[str]], Any],
    ) -> None:
        self.after_process_callbacks.append(cb)

    def process_all(
        self,
        data: Union[List[str], List["Document"]],
        attributes: Optional[List[str]],
    ) -> None:
        for d in self.process(data, attributes):
            continue
