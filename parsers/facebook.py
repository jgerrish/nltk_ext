from nltk_ext.parsers.parser import Parser
from nltk_ext.documents.facebook import FacebookDocument

class FacebookParser(Parser):
    def __init__(self):
        pass

    def _parse(self, post):
        return FacebookDocument(post)

    def parse(self, data, attributes=None):
        "Extract messages from facebook Graph API objects"
        doc = None
        if "message" in data:
            doc = self._parse(data)

        return doc
