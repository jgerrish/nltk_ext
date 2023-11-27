from typing import Any, Dict

from nltk_ext.parsers.parser import Parser
from nltk_ext.documents.twitter import TwitterDocument


class TwitterParser(Parser):
    def __init__(self) -> None:
        pass

    def _parse(self, post: Dict[str, Any]) -> TwitterDocument:
        return TwitterDocument(post)

    def parse(self, data: Dict[str, Any], attributes: Any = None) -> TwitterDocument:
        "Extract messages from twitter status objects"
        doc = None
        if "text" in data:
            doc = self._parse(data)

        return doc
