# Simple document class
import copy, itertools, json, operator, random
import nltk
from nltk.text import Text
from nltk_ext.indexes.unigram_index import UnigramIndex
import pprint

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

    def __init__(self, data, word_filters=[]):
        self.nltk_text = None
        self.body_attribute = Document.BodyAttribute
        self._index = None
        if (type(data) == str) or (type(data) == unicode):
            self.document = { }
            self.document[Document.BodyAttribute] = data
        else:
            self.__dict__.update((t, i) for (i,t) in enumerate(data))
            keys = data.keys()
            self.__dict__.update(zip(keys, [data[key] for key in keys]))
            self.document = data.copy()
        if "id" in self.document:
            self.set_doc_id(self.document["id"])
        self.word_filters = word_filters

    def __len__(self):
        "length of the document in characters"
        if self.body_attribute in self.document:
            return len(self.document[self.body_attribute])
        else:
            return 0

    def num_words(self):
        "length of the document in words"
        return sum(1 for _ in self.words())

    def __str__(self):
        if self.body_attribute in self.document:
            return self.document[self.body_attribute]
        else:
            return ""

    def __getitem__(self, k):
        return self.document[k]

    def __contains__(self, k):
        return k in self.document

    def as_json(self):
        return json.dumps(self.document, sort_keys=True, indent=4, separators=(',', ': '))

    def set_doc_id(self, doc_id):
        self.doc_id = doc_id

    def set_collection(self, collection):
        self.collection = collection

    def set(self, attribute, value):
        "set an attribute on the document"
        self.document[attribute] = value

    def neighbors(self):
        return self.collection.neighbors(self)

    def lowercase_words(self, words):
        for word in words:
            yield word.lower()

    def words(self, use_unicode=True, filtered=True, lowercase=True):
        all_words = []
        text = unicode(self).encode('ascii', 'ignore')
        for sentence in nltk.tokenize.sent_tokenize(text):
            words = nltk.tokenize.word_tokenize(sentence)
            if lowercase:
                words = self.lowercase_words(words)
            if filtered:
                for f in self.word_filters:
                    words = f.filter(words)
            all_words += words
        return all_words

    def to_ngrams(self, n=5):
        self.ngrams = nltk.util.ngrams(self.words(), n)
        return self.ngrams

    def to_nltk_text(self):
        if self.nltk_text:
            return self.nltk_text
        elif self.body_attribute in self.document:
            self.nltk_text = Text(self.words())
            return self.nltk_text
        return None

    def index(self, index_class=UnigramIndex):
        """
        index the document, building a word frequency table and other indexes
        stopwords are currently indexed
        """
        self._index = index_class()
        self._index.index(self)

    # returns the term frequency of a term
    def tf(self, term):
        if self._index:
            return self._index.tf(term)
        else:
            self.index()
            return self._index.tf(term)

    def freq_dist(self):
        if self._index:
            return self._index.freq_dist()
        else:
            self.index()
            return self._index.freq_dist()

    def update_text(self, text):
        if self.body_attribute in self.document:
            self.document[self.body_attribute] = text
        self.nltk_text = None
        if self._index:
            self._index.reset()
