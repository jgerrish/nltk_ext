# HTML Cleaner module for cleaning HTML documents before conversion
# TODO: Clean up pipeline interface, separate word/document processing
import copy
from nltk_ext.documents.html_document import HTMLDocument

class CreateDocument(object):
    def __init__(self, document_class=HTMLDocument, attribute="body"):
        self.document_class = document_class
        self.attribute = attribute

    def process(self, documents):
        for document in documents:
            if type(document) == str:
                d = {self.attribute: document}
            else:
                d = copy.copy(document)
            doc = self.document_class(d)
            yield doc
