from nltk import FreqDist
from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from nltk_ext.documents.document import Document


class Index:
    """
    The Index class stores an index for a document.
    """

    def __init__(self) -> None:
        self._freq_dist: Optional[FreqDist] = None
        self._document: Optional["Document"] = None

    def index(self, document: Optional["Document"] = None) -> None:
        if document is not None:
            self._document = document
        if self._document:
            if self._freq_dist is None:
                self._freq_dist = FreqDist()
                # TODO Test this and verify
                for term in self._document.words():
                    # for term in self.terms():
                    self._freq_dist[term] += 1  # type: ignore[attr-defined, index]

    def reset(self) -> None:
        "Reset the index"
        self._freq_dist = None

    def freq_dist(self) -> FreqDist:
        if self._freq_dist is None:
            self.index()
        return self._freq_dist

    # return the number of times a term appears in this document
    def freq(self, term: str) -> int:
        if not self._freq_dist:
            self.index()
        return self._freq_dist[term]  # type: ignore[index]

    def tf(self, term: str) -> float:
        if not self._freq_dist:
            self.index()
        return float(self._freq_dist[term]) / float(self._freq_dist.N())  # type: ignore[attr-defined, index]
