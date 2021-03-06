# filter a dictionary down to a select list of keys
# useful for processing large sets of documents in memory
from nltk_ext.documents.document import Document

# pipeline module to filter a dictionary by keys
class FilterDict(object):
    def __init__(self, keys=None):
        self.keys = keys

    def process(self, documents):
        for document in documents:
            if self.keys != None:
                d = { key: document[key] for key in self.keys }
                yield d
            else:
                yield document
