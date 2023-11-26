from typing import Dict, Iterator, Optional
from typing_extensions import Self

from nltk_ext.documents.document import Document


class FileReader:
    def __init__(self, source: str) -> None:
        self.data: Optional[str] = None
        if source:
            self.source = source
            self.read()

    # TODO: Make this use the context manager API
    def read(self, source: str = None) -> Optional[str]:
        # override constructor source if specified
        if source:
            self.source = source
        self.data = None
        with open(self.source, "r") as f:
            self.data = f.read().replace("\n", " ")
        return self.data

    # get the next document in the source
    # currently the FileReader only reads a single document
    def next(self) -> Dict[str, str]:
        if self.cursor_position > 0:
            raise StopIteration
        else:
            self.cursor_position += 1
            return {"id": self.source, "body": self.data}

    def process(self, data: str) -> Iterator[Document]:
        doc = Document({"id": self.source, "body": self.data})
        for doc in [doc]:
            yield doc

    def __iter__(self) -> Self:
        self.cursor_position = 0
        return self
