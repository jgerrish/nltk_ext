# HTML Cleaner module for cleaning HTML documents before conversion
# TODO: Clean up pipeline interface, separate word/document processing
import copy
import pprint
import re


class HtmlCleaner(object):
    def __init__(self, attribute="body"):
        self.attribute = attribute
        self.regexp = re.compile(r"<[bB][rR]\s*\/?\s*>")
        self.pp = pprint.PrettyPrinter(indent=4)

    def process(self, documents):
        for document in documents:
            if type(document) == str:
                d = document
                if d != "":
                    d = self.regexp.sub("\n", d)
            else:
                d = copy.copy(document)
                if self.attribute in d:
                    new_val = self.regexp.sub("\n", d[self.attribute])
                    d.set(self.attribute, new_val)
            yield d
