# Simple document corpus / collection
import importlib.util
import math, operator, pprint
import nltk.corpus

package_name = 'sklearn.utils'
spec = importlib.util.find_spec(package_name)
sklearn_installed = False
if spec is not None:
    sklearn_installed = True
    from sklearn.utils import Bunch
from nltk import FreqDist
from nltk.text import TextCollection
from nltk_ext.documents.document import Document
from operator import itemgetter, attrgetter

class ScikitLearnNotInstalledException(Exception):
    "An exception that indicates scikit-learn is not installed"
    pass


class Corpus:
    def __init__(self, documents=None):
        """
        Corpus constructor
        documents is a list of documents
        """
        self.docs = {}
        if documents:
            for doc in documents:
                self.docs[doc.doc_id] = doc
            self.nltk_text_collection = TextCollection([x.to_nltk_text() for x in self.docs.values()])
        self.term_index = {}
        self._vocabulary = None
        self.clear_indexes()
        self.pp = pprint.PrettyPrinter(indent=4)

    #def neighbors(self, document, window_size=9)

    def __len__(self):
        return len(self.docs.keys())

    def __contains__(self, a):
        return a in self.docs

    def __getitem__(self, x):
        """Return the document with Document ID x"""
        return self.docs[x]

    def categories(self):
        """
        Returns list of categories in this corpus
        For combined corpora, categories are equivalent to document ids
        """
        return self.docs.keys()

    def _old_neighbors(self, document, window_size=9):
        """
        neighbors based on moving window
        window_size is the diameter from the index element
        that should be included in the results
        """
        if not self.sorted_by_len:
            self.generate_neighbor_list()

        if document.doc_id not in self.inverse_len_index:
            return []

        index = self.inverse_len_index[document.doc_id]

        l = len(self.sorted_by_len)
        r = window_size / 2
        start = max(0, index - r)
        end = min(l, (index + 1) + r)
        n = self.sorted_by_len[start:index] + self.sorted_by_len[(index+1):end]
        return [self.__getitem__(x) for x in n]

    def neighbors(self, document, max_distance):
        """
        neighbors based on moving window
        distance is the maximum distance from the index element
        that should be included in the results
        """
        sorted_dist_vector = self.generate_neighbor_list(document)
        filtered = filter(lambda x: x[1] <= max_distance, sorted_dist_vector)
        return [self.__getitem__(x[0][0]) for x in filtered]

    def _sort_dict_by_value(self, d):
        return sorted(iter(d.items()), key=operator.itemgetter(1))

    def _sorted_dict_index(self, pairs):
        return [i for i, j in pairs]

    def add(self, document):
        """
        Add a document to this collection
        If there is any current iterator using this collection, it is
        not modified.  You need to re-initialize the iterator if you want
        to include the new items.
        """
        #print "adding " + str(document.doc_id)
        self.docs[document.doc_id] = document
        self.clear_indexes()

    def clear_indexes(self):
        self.doc_lens = None
        self.dist_matrix = None
        self.sorted_by_len = None
        self.inverse_len_index = None
        self.inverse_dist_index = None

    def generate_doc_lens(self):
        self.doc_lens = {}
        for document in self.docs.values():
            doc_id = document.doc_id
            shn = len(document)
            self.doc_lens[document.doc_id] = shn

    def char_dist(self, doc1, doc2):
        "distance function by difference between document lengths"
        return abs(self.doc_lens[doc1] - self.doc_lens[doc2])

    def generate_dist_vector(self, document, dist_func=char_dist):
        if (isinstance(document, Document)):
            doc_id = document.doc_id
        elif type(document) == str:
            doc_id = document
        if self.doc_lens == None:
            self.generate_doc_lens()
        v = {}
        for target in self.docs.keys():
            v[target] = dist_func(self, doc_id, target)
        return v

    def generate_dist_matrix(self):
        if self.doc_lens == None:
            self.generate_doc_lens()
        if self.dist_matrix == None:
            self.dist_matrix = {}
        for doc1 in self.docs.keys():
            self.dist_matrix[doc1] = generate_dist_vector(doc1)

    def _generate_neighbor_list(self):
        if self.doc_lens == None:
            self.generate_doc_lens()
        self.sorted_by_len = self._sorted_dict_index(self._sort_dict_by_value(self.doc_lens))
        self.inverse_len_index = {}
        for idx, val in enumerate(self.sorted_by_len):
            self.inverse_len_index[val] = idx

    def generate_neighbor_list(self, document):
        dist_vector = self.generate_dist_vector(document)
        return self._sort_dict_by_value(dist_vector)

    def next(self):
        if self.cursor_position >= len(self.found_docs):
            raise StopIteration
        else:
            self.cursor_position += 1
            doc = self.docs[self.found_docs[self.cursor_position - 1]]
            return doc

    def __iter__(self):
        self.cursor_position = 0
        self.found_docs = self.docs.keys()
        return self

    def to_nltk_text_collection(self):
        if self.nltk_text_collection:
            return self.nltk_text_collection
        else:
            self.nltk_text_collection = TextCollection([x.to_nltk_text() for x in self.docs.values()])
            return self.nltk_text_collection
        return None

    # wtf nltk
    def index(self):
        for k in self.docs.keys():
            for word in self.docs[k].words():
                if word in self.term_index:
                    self.term_index[word].add(k)
                else:
                    self.term_index[word] = set()
                    self.term_index[word].add(k)

    def df(self, term):
        if not self.term_index:
            self.index()
        #self.pp.pprint(self.term_index)
        if term in self.term_index:
            return len(self.term_index[term])
        else:
            return 0

    def idf(self, term):
        df = self.df(term)
        if df == 0.0:
            return 0.0
        else:
            return math.log(float(len(self)) / float(self.df(term)))

    # Use non-augmented tf for now, can experiment later
    def tf(self, doc_id, term):
        return self.docs[doc_id].tf(term)

    def tf_idf(self, doc_id, term):
        return self.tf(doc_id, term) * float(self.idf(term))

    def vocabulary(self):
        if self._vocabulary == None:
            self._vocabulary = FreqDist()
            for doc in self.docs.values():
                self._vocabulary.update(dict(doc.freq_dist()))
        return self._vocabulary

    def tf_idf_vector(self, doc_id):
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

    def ranked_terms(self, doc_id, n=None):
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

        if n != None:
            return sorted_v[0:n]
        else:
            return sorted_v

    def top_terms(self, n=5):
        r = []
        for document in self.docs.values():
            r.append(self.ranked_terms(document.doc_id, n))
        return r

    def to_scikit_learn_dataset(self):
        if not sklearn_installed:
            raise ScikitLearnNotInstalledException("scikit-learn not installed")
        dataset = {}
        dataset["data"] = []
        dataset["ids"] = []
        #dataset["filenames"]
        for doc_id in self.docs.keys():
            dataset["ids"].append(doc_id)
            dataset["data"].append(str(self.docs[doc_id]))
            # dataset["data"].append(unicode(self.docs[doc_id]))

        b = Bunch(DESCR=None, ids=dataset["ids"], data=dataset["data"])
        return b

    def keys_sorted_by_attribute(self, attribute="created_time"):
        """
        Return the list of document ids sorted by a document attribute
        """
        d = []
        for doc_id in self.docs.keys():
            if attribute in self.docs[doc_id].document:
                d.append((doc_id, self.docs[doc_id].document[attribute]))
        # sort the list of doc_id, attribute tuples by the attribute
        return [x[0] for x in sorted(d, key=itemgetter(1))]

    def process_pipeline(self, pipeline):
        for doc in self.docs.values():
            res = pipeline.process(doc)
