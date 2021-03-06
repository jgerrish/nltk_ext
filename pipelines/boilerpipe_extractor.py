# HTML to text module for converting HTML documents to text
import copy
from boilerpipe.extract import Extractor

class BoilerpipeExtractor(object):
    def __init__(self, attribute="body", new_attribute="body_text"):
        self.attribute = attribute
        self.new_attribute = new_attribute

    def process_text(self, text):
        if text == "":
            return text
        extractor = Extractor(extractor='ArticleExtractor',
                              html=text)
        new_val = extractor.getText()
        return new_val

    def process(self, documents):
        for document in documents:
            if type(document) == str:
                d = document
                yield self.process_text(d)
                continue
            else:
                d = copy.copy(document)
                if self.attribute in d:
                    text = d[self.attribute]
                    new_val = self.process_text(text)
                    d.set(self.new_attribute, new_val)
                    yield d
                    continue
                else:
                    d.set(self.new_attribute, "")
                    yield d
                    continue
