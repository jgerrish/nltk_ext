"""
Simple document corpus / collection
"""
import importlib.util
import math
import operator
import pprint
from typing import Any, Callable, Dict, List, Optional, Set, Tuple, Union, TYPE_CHECKING
from typing_extensions import Self

if TYPE_CHECKING:
    from nltk_ext.pipelines.pipeline_module import PipelineModule

from nltk import FreqDist
from nltk.text import TextCollection
from nltk_ext.documents.document import Document
from operator import itemgetter


package_name = "sklearn.utils"
spec = importlib.util.find_spec(package_name)
sklearn_installed = False
if spec is not None:
    sklearn_installed = True
    from sklearn.utils import Bunch


class ScikitLearnNotInstalledException(Exception):
    "An exception that indicates scikit-learn is not installed"
    pass


class Corpus:
    """A Corpus class that holds a collection of documents

    This class holds a collection of documents and provides several
    methods for indexing and computing statistics on the documents.
    """
    def __init__(self, documents: List[Document] = None) -> None:
        """Corpus constructor

        Arguments:
          documents: a list of documents to add to the corpus
        """
        self.docs = {}
        if documents:
            for doc in documents:
                self.docs[doc.doc_id] = doc
            self.nltk_text_collection = TextCollection(
                [x.to_nltk_text() for x in self.docs.values()]
            )
        self.term_index: Dict[str, Set[str]] = {}
        self._vocabulary = None
        self.clear_indexes()
        self.pp = pprint.PrettyPrinter(indent=4)

    # def neighbors(self, document, window_size=9)

    def __len__(self) -> int:
        """Returns the number of documents in the Corpus"""
        return len(self.docs.keys())

    def __contains__(self, a: str) -> bool:
        """Returns the document with the given id in the Corpus"""
        return a in self.docs

    def __getitem__(self, x: str) -> Document:
        """Return the document with Document ID x"""
        return self.docs[x]

    def categories(self) -> List[str]:
        """
        Returns list of categories in this corpus
        For combined corpora, categories are equivalent to document ids
        """
        return list(self.docs.keys())

    def neighbors(
        self,
        document: Document,
        max_distance: float,
    ) -> list[Document]:
        """
        neighbors based on moving window
        distance is the maximum distance from the index element
        that should be included in the results
        """
        sorted_dist_vector = self.generate_neighbor_list(document)
        filtered = filter(lambda x: x[1] <= max_distance, sorted_dist_vector)
        return [self.__getitem__(x[0][0]) for x in filtered]

    def _sort_dict_by_value(self, d: Dict[Any, Any]) -> List[Tuple[Any, Any]]:
        """Sort a dictionary by value

        Arguments:
          d: The dictionary to sort by value

        Returns:
          The dictionary sorted by value
        """
        return sorted(iter(d.items()), key=operator.itemgetter(1))

    def _sorted_dict_index(self, pairs: List[Tuple[Any, Any]]) -> List[Any]:
        """Return the index tuple in a tuple pair list

        Given a list of tuple pairs, return the first item in each
        tuple pair for all items in the list.

        Example: [("a", 1), ("b", 2), ("c", 3)] -> ['a', 'b', 'c']

        Arguments:
          pairs: A list of tuple pairs

        Returns:
          A list of the first element of each tuple pair
        """
        return [i for i, j in pairs]

    def add(self, document: Document) -> None:
        """
        Add a document to this collection
        If there is any current iterator using this collection, it is
        not modified.  You need to re-initialize the iterator if you want
        to include the new items.
        """
        # print "adding " + str(document.doc_id)
        self.docs[document.doc_id] = document
        self.clear_indexes()

    def clear_indexes(self) -> None:
        """Clear the indexes on this Corpus"""
        self.doc_lens: Optional[Dict[str, int]] = None
        self.dist_matrix: Optional[Dict[Tuple[str, str], float]] = None
        self.sorted_by_len: Optional[List[str]] = None
        self.inverse_len_index: Optional[Dict[str, int]] = None
        self.inverse_dist_index = None

    # TODO Add tests for this
    def generate_doc_lens(self) -> None:
        """Generate and store document lengths

        This method finds the length of each document and stores it in
        the doc_lens member variable.
        """
        self.doc_lens = {}
        for document in self.docs.values():
            shn = len(document)
            self.doc_lens[document.doc_id] = shn

    def char_dist(self, doc1: str, doc2: str) -> int:
        "distance function by difference between document lengths"
        if self.doc_lens is None:
            self.generate_doc_lens()
        return abs(self.doc_lens[doc1] - self.doc_lens[doc2])

    def generate_dist_vector(
        self,
        document: Document,
        dist_func: Callable[["Corpus", str, str], float] = char_dist,
    ) -> dict[str, float]:
        """Generate a distance vector for a document

        Generate a distance vector for a given document with a given
        distance function.

        Arguments:
          document: The document to use to build a distance vector
          dist_func: The distance function

        Returns:
          The distance vector
        """
        doc_id = None
        if isinstance(document, Document):
            doc_id = document.doc_id
        elif type(document) == str:
            doc_id = document
        if self.doc_lens is None:
            self.generate_doc_lens()
        v = {}
        for target in self.docs.keys():
            v[target] = dist_func(self, doc_id, target)
        return v

    # TODO Add tests for this
    def generate_dist_matrix(self) -> None:
        """Generate a distance matrix for this corpus"""
        if self.doc_lens is None:
            self.generate_doc_lens()
        if self.dist_matrix is None:
            self.dist_matrix = {}
        # for doc1 in self.docs.keys():
        #     self.dist_matrix[doc1] = generate_dist_vector(doc1)

    def _generate_neighbor_list(self) -> None:
        """Generate a neighbor list for this corpus"""
        if self.doc_lens is None:
            self.generate_doc_lens()
        self.sorted_by_len = self._sorted_dict_index(
            self._sort_dict_by_value(self.doc_lens)
        )
        self.inverse_len_index = {}
        for idx, val in enumerate(self.sorted_by_len):
            self.inverse_len_index[val] = idx

    def generate_neighbor_list(self, document: Document) -> List[Tuple[str, float]]:
        """Generate a neighbor list for document

        Arguments:
          document: The document to generate a neighbor list

        Returns:
          The distance vector
        """
        dist_vector = self.generate_dist_vector(document)
        return self._sort_dict_by_value(dist_vector)

    def next(self) -> Document:
        """Return the next item in the iterator"""
        if self.cursor_position >= len(self.found_docs):
            raise StopIteration
        else:
            self.cursor_position += 1
            doc = self.docs[self.found_docs[self.cursor_position - 1]]
            return doc

    def __iter__(self) -> Self:
        """Get an iterator for this Corpus"""
        self.cursor_position = 0
        self.found_docs: List[str] = list(self.docs.keys())
        return self

    def __next__(self) -> Document:
        """Return the next item in the iterator"""
        if self.cursor_position >= len(self.found_docs):
            raise StopIteration
        else:
            doc = self.found_docs[self.cursor_position]
            self.cursor_position += 1
            return self.docs[doc]

    def to_nltk_text_collection(self) -> Union[None, "Corpus"]:
        """Generate a NLTK TextCollection from this Corpus

        Returns:
          None if a TextCollection couldn't be generated, otherwise it
          returns a TextCollection with the documents.
        """
        if self.nltk_text_collection:
            return self.nltk_text_collection
        else:
            self.nltk_text_collection = TextCollection(
                [x.to_nltk_text() for x in self.docs.values()]
            )
            return self.nltk_text_collection
        return None

    # wtf nltk
    def index(self) -> None:
        """Build a term index for the Corpus

        Builds a term index for this document and stores it in the
        term_index member variable.
        """
        for k in self.docs.keys():
            for word in self.docs[k].words():
                if word in self.term_index:
                    self.term_index[word].add(k)
                else:
                    self.term_index[word] = set()
                    self.term_index[word].add(k)

    def df(self, term: str) -> float:
        """Find the document frequency for a given term

        Finds the number of documents a term occurs in.

        If the term occurs more than once in a document, it is only counted
        once for that document.

        Arguments:
          term: the term to look up

        Returns:
          The number of documents the term occurs in
        """
        if not self.term_index:
            self.index()
        # self.pp.pprint(self.term_index)
        if term in self.term_index:
            return len(self.term_index[term])
        else:
            return 0

    def idf(self, term: str) -> float:
        """Find the inverse document frequency for a given term

        Arguments:
          term: the term to look up

        Returns:
          The inverse document frequency of the term
        """
        df = self.df(term)
        if df == 0.0:
            return 0.0
        else:
            return math.log(float(len(self)) / float(self.df(term)))

    # Use non-augmented tf for now, can experiment later
    def tf(self, doc_id: str, term: str) -> float:
        """Return the term frequency for a word in a given document

        Return the term frequency for a word in a given document

        Arguments:
          doc_id: The document ID of the document to search
          term: The term to lookup

        Returns:
          The term frequency of the term in the given document
        """
        return self.docs[doc_id].tf(term)

    def tf_idf(self, doc_id: str, term: str) -> float:
        """Get the TF-IDF for a term in a given document

        Arguments:
          doc_id: The document ID of the document to search
          term: The term to lookup

        Returns:
          The TF-IDF for the given document and term
        """
        return self.tf(doc_id, term) * float(self.idf(term))

    def vocabulary(self) -> FreqDist:
        """Return the vocabulary of this Corpus

        Returns all the terms in this document and their frequency.

        Returns:
          The vocabulary of this Corpus as a NLTK FreqDist object
        """
        if self._vocabulary is None:
            self._vocabulary = FreqDist()
            for doc in self.docs.values():
                if self._vocabulary is not None:
                    self._vocabulary.update(dict(doc.freq_dist()))
        return self._vocabulary

    def tf_idf_vector(self, doc_id: str) -> list[float]:
        """return the TF-IDF term vector for a document
        the length of the vector is equal to the vocabulary size, not the
        number of terms in the document"""
        v = [0.0] * len(self.vocabulary())
        d = self.docs[doc_id]
        if d:
            fd = d.freq_dist()
            for idx, word in self.vocabulary():
                if word in fd:
                    v[idx] = self.tf_idf(doc_id, word)
        return v

    def ranked_terms(
        self, doc_id: str, n: Union[None, int] = None
    ) -> List[Tuple[str, float]]:
        """
        returns a list of the top terms by TF-IDF in a document
        if n is none, return all terms.  Otherwise return the top n
        terms.
        """
        d = self.docs[doc_id]
        if d:
            v = {}
            fd = d.freq_dist()
            for word in fd.keys():
                v[word] = self.tf_idf(doc_id, word)
        sorted_v = sorted(iter(v.items()), key=operator.itemgetter(1))
        sorted_v.reverse()

        if n is not None:
            return sorted_v[0:n]
        else:
            return sorted_v

    def top_terms(self, n: int = 5) -> List[List[Tuple[str, float]]]:
        """Get all the top terms for all the documents

        Get a list of all the top terms in the Corpus for all documents.
        The terms are not combined.
        A list of lists is returned for every document and every term.

        Arguments:
          n: The limit on the top-n terms to return

        Returns:
          A list of lists for every document and every term in each
          document.
        """
        r: List[List[Tuple[str, float]]] = []
        for document in self.docs.values():
            r.append(self.ranked_terms(document.doc_id, n))
        return r

    def to_scikit_learn_dataset(self) -> Bunch:
        """Return a scikit-learn dataset for this Corpus

        Returns:
          A Bunch representation of the Corpus
        """
        if not sklearn_installed:
            raise ScikitLearnNotInstalledException("scikit-learn not installed")
        dataset: Dict[str, List[str]] = {}
        dataset["data"] = []
        dataset["ids"] = []
        # dataset["filenames"]
        for doc_id in self.docs.keys():
            dataset["ids"].append(doc_id)
            dataset["data"].append(str(self.docs[doc_id]))
            # dataset["data"].append(unicode(self.docs[doc_id]))

        b = Bunch(DESCR=None, ids=dataset["ids"], data=dataset["data"])
        return b

    def keys_sorted_by_attribute(self, attribute: str = "created_time") -> list[str]:
        """
        Return the list of document ids sorted by a document attribute
        """
        d = []
        for doc_id in self.docs.keys():
            if attribute in self.docs[doc_id].document:
                d.append((doc_id, self.docs[doc_id].document[attribute]))
        # sort the list of doc_id, attribute tuples by the attribute
        return [x[0] for x in sorted(d, key=itemgetter(1))]

    # TODO Add tests for this
    def process_pipeline(self, pipeline: "PipelineModule") -> None:
        """Apply a pipeline module to this corpus

        Process this collection of documents with a PipelineModule

        Arguments:
          pipeline: The PipelineModule to run
        """
        for doc in self.docs.values():
            pipeline.process([doc])
