# Simple document class
import json
import nltk

from nltk.text import Text
from nltk_ext.filters.filter import Filter
from nltk_ext.indexes.index import Index
from nltk_ext.indexes.unigram_index import UnigramIndex
from typing import Any, Dict, Iterator, List, Optional, Union, TYPE_CHECKING

if TYPE_CHECKING:
    from nltk_ext.corpus.corpus import Corpus


class Document:
    """
    Generic Document class
    Every document should have the following fields:
    doc_id: a unique document id
    text: an attribute defined by BodyAttribute that contains the main
          document text
    """

    BodyAttribute = "body"

    # def __init__(self, **data):
    #     """
    #     factory constructor that creates attributes for each dictionary key
    #     passed in
    #     """
    #     self.__dict__.update(data)

    def __init__(
        self,
        data: Union[str, Dict[str, str]],
        word_filters: List[Filter] = [],
    ) -> None:
        self.nltk_text = None
        self.body_attribute = Document.BodyAttribute
        self._index: Optional["Index"] = None
        if type(data) == str:  # or (type(data) == unicode):
            self.document = {}
            self.document[Document.BodyAttribute] = data
        else:
            self.__dict__.update((t, i) for (i, t) in enumerate(data))
            keys: List[str] = list(data.keys())  # type: ignore[union-attr]
            self.__dict__.update(zip(keys, [data[key] for key in keys]))  # type: ignore[index]
            self.document = data.copy()  # type: ignore[union-attr]
        if "id" in self.document:
            self.set_doc_id(self.document["id"])
        self.word_filters = word_filters

    def __len__(self) -> int:
        "length of the document in characters"
        if self.body_attribute in self.document:
            return len(self.document[self.body_attribute])
        else:
            return 0

    def num_words(self) -> int:
        "length of the document in words"
        return sum(1 for _ in self.words())

    def __str__(self) -> str:
        if self.body_attribute in self.document:
            return self.document[self.body_attribute]
        else:
            return ""

    def __getitem__(self, k: str) -> str:
        return self.document[k]

    def __contains__(self, k: str) -> bool:
        return k in self.document

    def as_json(self) -> str:
        return json.dumps(
            self.document, sort_keys=True, indent=4, separators=(",", ": ")
        )

    def set_doc_id(self, doc_id: str) -> None:
        self.doc_id = doc_id

    def set_collection(self, collection: "Corpus") -> None:
        self.collection = collection

    def set(self, attribute: str, value: Any) -> None:
        "set an attribute on the document"
        self.document[attribute] = value

    def neighbors(self) -> list["Document"]:
        return self.collection.neighbors(self, 1.0)

    def lowercase_words(self, words: List[str]) -> Iterator[str]:
        for word in words:
            yield word.lower()

    def words(
        self,
        use_unicode: bool = True,
        filtered: bool = True,
        lowercase: bool = True,
    ) -> List[str]:
        all_words = []
        # text = unicode(self).encode('ascii', 'ignore')
        # text = str(self).encode('ascii', 'ignore')
        text = str(self)
        # print(type(self))
        # if type(self) == 'java.lang.String':
        # text = self.decode(chardet.detect(self)['encoding'])
        # else:
        #    text = str(self)

        for sentence in nltk.tokenize.sent_tokenize(text):
            words = nltk.tokenize.word_tokenize(sentence)
            if lowercase:
                words = self.lowercase_words(words)
            if filtered:
                for f in self.word_filters:
                    words = f.filter(words)
            all_words += words
        return all_words

    def to_ngrams(self, n: int = 5) -> Iterator[str]:
        """
        This returns an iterator for ngrams.
        Creating a list from it consumes the generator.
        """
        self.ngrams = nltk.ngrams(self.words(), n)
        return self.ngrams

    def to_nltk_text(self) -> Optional[Text]:
        if self.nltk_text:
            return self.nltk_text
        elif self.body_attribute in self.document:
            self.nltk_text = Text(self.words())
            return self.nltk_text
        return None

    def index(self, index_class: type[Index] = UnigramIndex) -> None:
        """
        index the document, building a word frequency table and other indexes
        stopwords are currently indexed
        """
        self._index = index_class()
        if self._index is not None:
            self._index.index(self)

    # returns the term frequency of a term
    def tf(self, term: str) -> float:
        if self._index is not None:
            return self._index.tf(term)
        else:
            self.index()
            if self._index is not None:
                return self._index.tf(term)
            else:
                raise Exception("TODO Fix this shit")

    def freq_dist(self) -> Dict[str, int]:
        if self._index:
            return self._index.freq_dist()
        else:
            self.index()
            return self._index.freq_dist()

    def update_text(self, text: str) -> None:
        if self.body_attribute in self.document:
            self.document[self.body_attribute] = text
        self.nltk_text = None
        if self._index:
            self._index.reset()
