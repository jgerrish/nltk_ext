from nltk_ext.parsers.parser import Parser
from nltk_ext.documents.twitter import TwitterDocument


class TwitterParser(Parser):
    def __init__(self):
        pass

    def _parse(self, post):
        return TwitterDocument(post)

    def parse(self, data, attributes=None):
        "Extract messages from twitter status objects"
        doc = None
        if "text" in data:
            doc = self._parse(data)

        return doc
