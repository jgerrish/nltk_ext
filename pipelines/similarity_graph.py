# similarity graph generator
import itertools, sets
from nltk_ext.documents.document import Document
from nltk_ext.graph import Graph
from nltk.util import ngrams

# Document pipeline module to generate a similarity graph for a document
class SimilarityGraph(object):
    def __init__(self, dist_func, distance=100):
        self.dist_func = dist_func
        self.distance = distance
        self.graph = Graph()
        self.corpus = Corpus()

    def process(self, documents):
        for document in documents:
            if (isinstance(document, Document)):
                self.corpus.add(document)
                doc1_id = document.doc_id
                neighbors = self.corpus.neighbors(doc1_id, self.distance)

        yield document
