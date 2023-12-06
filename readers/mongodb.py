import copy
from pymongo import MongoClient
from bson.objectid import ObjectId
from typing import Any, Iterator
from typing_extensions import Self

from nltk_ext.documents.document import Document
from nltk_ext.documents.html_document import HTMLDocument


# TODO: investigate if we need to use the MongoDB cursor functionality instead
# to prevent loading documents into memory
class MongoDBReader:
    def __init__(
        self,
        db: str = "db_name",
        collection: str = "collection_name",
    ) -> None:
        self.mongodb_client = MongoClient()
        self.db = self.mongodb_client[db]
        self.collection = self.db[collection]
        self.count: int = 0

    def read(self, source: Any) -> None:
        return None

    def __next__(self) -> Document:
        if self.cursor_position >= self.collection.count():
            raise StopIteration
        else:
            self.cursor_position += 1
            doc = self.found_docs[self.cursor_position - 1]
            h = copy.copy(doc)
            h["id"] = str(doc["_id"])
            return h

    def __iter__(self) -> Self:
        self.cursor_position = 0
        self.found_docs = self.collection.find()
        return self

    def get(self, doc_id: str) -> HTMLDocument:
        return self.collection.find_one({"_id": ObjectId(doc_id)})

    def remove(self, doc_id: str) -> None:
        self.collection.remove({"_id": ObjectId(doc_id)})

    def process(self, data: Any) -> Iterator[HTMLDocument]:
        for doc in self.collection.find():
            h = doc.copy()
            h["id"] = str(doc["_id"])
            yield h

    def get_doc(self, doc_id: str, doc_class: Any = HTMLDocument) -> Any:
        d = self.get(doc_id)
        h = copy.copy(d)
        h["id"] = str(d["_id"])  # type: ignore[index]
        del h["_id"]  # type: ignore[attr-defined]
        return doc_class(h)
