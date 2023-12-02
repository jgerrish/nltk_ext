"""
Simple document class
"""
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

    def __init__(
        self,
        data: Union[str, Dict[Any, Any]],
        word_filters: Optional[List[Filter]] = None,
    ) -> None:
        """Create a new document

        Args:
        data: A dictionary containg the fields and data for the
          document.  Or a string with the document contents.
        word_filters: A list of filters that get run when processing this document.

        Returns:
          None.
        """
        self.nltk_text = None
        self.body_attribute = Document.BodyAttribute
        self._index: Optional["Index"] = None
        if type(data) == str:  # or (type(data) == unicode):
            self.document = {}
            self.document[Document.BodyAttribute] = data
        elif type(data) == dict:
            self.__dict__.update((t, i) for (i, t) in enumerate(data))
            keys: List[str] = list(data.keys())
            self.__dict__.update(zip(keys, [data[key] for key in keys]))
            self.document = data.copy()
        if "id" in self.document:
            self.set_doc_id(self.document["id"])
        if word_filters is not None:
            self.word_filters = word_filters
        else:
            self.word_filters = []

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
        """
        Return the document as a string

        Returns:
          The body of the document as a string.
        """
        if self.body_attribute in self.document:
            return self.document[self.body_attribute]
        else:
            return ""

    # TODO Add more tests around int vs str keys and make sure API is
    # clean
    def __getitem__(self, k: Any) -> str:
        """Get an attribute of the document.

        Args:
          k: The document attribute key

        Returns:
          The value of the attribute
        """
        return self.document[k]

    def __contains__(self, k: Any) -> bool:
        """Returns true if an attribute is set on the document.

        Args:
          k: The attribute key

        Returns:

        True if the document contains the attribute, false if
        it doesn't.
        """
        return k in self.document

    def as_json(self) -> str:
        "Returns this document as a JSON string"
        return json.dumps(
            self.document, sort_keys=True, indent=4, separators=(",", ": ")
        )

    def set_doc_id(self, doc_id: str) -> None:
        """Set the document ID for this document.

        Args:
          doc_id: The document ID to set.
        """
        self.doc_id = doc_id

    def set_collection(self, collection: "Corpus") -> None:
        """Set the primary collection this document belongs in.

        Args:
          collection: The primary Corpus this document belongs to.
        """
        self.collection = collection

    def set(self, attribute: str, value: Any) -> None:
        """Set an attribute on the document

        Args:
          attribute: The attribute key to set.
          value: The value of the attribute.
        """
        self.document[attribute] = value

    def neighbors(self) -> list["Document"]:
        """Get the neighbors of this document.

        Returns:
          The neighbors of this document.
        """
        return self.collection.neighbors(self, 1.0)

    def lowercase_words(self, words: List[str]) -> Iterator[str]:
        """Get an iterator for words in this document as lowercase.

        Returns:
          An iterator with the words as lowercase.
        """
        for word in words:
            yield word.lower()

    def words(
        self,
        use_unicode: bool = True,
        filtered: bool = True,
        lowercase: bool = True,
    ) -> List[str]:
        """Get the words in this document
        Args:
          use_unicode: Whether to return Unicode characters.
          filtered: Whether to run the document word filters the words.
          lowercase: Whether to lowercase the words before returning them.

        Returns:
          The words as a list.
        """
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
            if filtered and (self.word_filters is not None):
                for f in self.word_filters:
                    words = f.filter(words)
            all_words += words
        return all_words

    def to_ngrams(self, n: int = 5) -> Iterator[str]:
        """Get an iterator for ngrams.

        Creating a list from it consumes the generator.

        Args:
        n: The n for the n-gram parameter (Number of characters
          in the n-gram).

        Returns:
          The ngrams as a iterator.
        """
        self.ngrams = nltk.ngrams(self.words(), n)
        return self.ngrams

    def to_nltk_text(self) -> Optional[Text]:
        """Return the Document as an NLTK Text object.

        Returns:
          The Document as an NLTK Text object if it contains
          text.  Otherwise it returns None.
        """
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
        """Returns the term frequency for a term in the document.

        The term frequency is the percentage of the document the term
        contributes to.  So for example, in a five word document, "The
        cat bopped the dog", the term "the" has a TF of 40% or
        0.4. The term "cat" has a TF of 20% or 0.2.

        Args:
          term: The term to get the term frequency for.

        Returns:
          The term frequency for the term.

        """
        if self._index is not None:
            return self._index.tf(term)
        else:
            self.index()
            if self._index is not None:
                return self._index.tf(term)
            else:
                raise Exception("TODO Fix this shit")

    def freq_dist(self) -> Dict[str, int]:
        """Get the frequency distribution for this document

        The frequency distribution is a class that is essentially a
        dictionary with each document term as a key and the number of
        occurences as the value.

        Returns:
          Returns the frequency distribution for this document.
        """
        if self._index:
            return self._index.freq_dist()
        else:
            self.index()
            return self._index.freq_dist()

    def update_text(self, text: str) -> None:
        """Update the text for this document

        Args:
          text: The text to set for this document.
        """
        if self.body_attribute in self.document:
            self.document[self.body_attribute] = text
        self.nltk_text = None
        if self._index:
            self._index.reset()
