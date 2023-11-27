from typing import Any, Dict

from nltk_ext.parsers.parser import Parser
from nltk_ext.documents.facebook import FacebookDocument


class FacebookParser(Parser):
    def __init__(self) -> None:
        pass

    def _parse(self, post: Dict[str, Any]) -> FacebookDocument:
        return FacebookDocument(post)

    def parse(self, data: Dict[str, Any], attributes: Any = None) -> FacebookDocument:
        "Extract messages from facebook Graph API objects"
        doc = None
        if "message" in data:
            doc = self._parse(data)

        return doc
