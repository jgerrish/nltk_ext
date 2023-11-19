# filter a document down to a select list of attributes
# useful for processing large sets of documents in memory
from nltk_ext.documents.document import Document


# Document pipeline module to filter a document by attributes
class FilterDocument(object):
    def __init__(self, attributes=None):
        self.attributes = attributes

    def process(self, documents):
        for document in documents:
            if self.attributes is not None:
                d = {key: document.document[key] for key in self.attributes}
                yield Document(d)
            else:
                yield document
