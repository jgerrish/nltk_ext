# w-shingling generator
import itertools, sets
from nltk_ext.documents.document import Document
from nltk.util import ngrams

# Document pipeline module to generate w-shingles for a document
# The w-shingles for a document are the set of hashed unique n-grams
# in that document
# If a document attribute is given in the constructor, assign the
# hashes to that attribute and yield the document.  Otherwise yield
# the hashes themselves.
class WShingle(object):
    def __init__(self, ngram_size=10, attribute=None):
        self.ngram_size = ngram_size
        self.attribute = attribute

    def process(self, documents):
        for document in documents:
            if (isinstance(document, Document)):
                ngrams = document.to_ngrams(self.ngram_size)
            elif type(document) == str:
                doc = Document(document)
                ngrams = doc.to_ngrams(self.ngram_size)
            uniq = sets.ImmutableSet(ngrams)
            hashes = [hash(ng) for ng in uniq]
            if self.attribute:
                document.set(self.attribute, hashes)
                yield document
            else:
                yield hashes
