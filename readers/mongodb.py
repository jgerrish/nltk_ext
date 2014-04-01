from pymongo import MongoClient
from bson.objectid import ObjectId
from nltk_ext.documents.html_document import HTMLDocument

# TODO: investigate if we need to use the MongoDB cursor functionality instead
# to prevent loading documents into memory
class MongoDBReader(object):
    def __init__(self, db="spout_test", collection="documents"):
        self.mongodb_client = MongoClient()
        self.db = self.mongodb_client[db]
        self.collection = self.db[collection]
        self.count = 0

    def read(self, source):
        return None

    def next(self):
        if self.cursor_position >= self.collection.count():
            raise StopIteration
        else:
            self.cursor_position += 1
            doc = self.found_docs[self.cursor_position - 1]
            h = doc.copy()
            h['id'] = str(doc['_id'])
            return h

    def __iter__(self):
        self.cursor_position = 0
        self.found_docs = self.collection.find()
        return self

    def get(self, doc_id):
        return self.collection.find_one({"_id": ObjectId(doc_id)})

    def remove(self, doc_id):
        self.collection.remove({"_id":ObjectId(doc_id)})

    def process(self, data):
        i = iter(self)
        for doc in self.collection.find():
            h = doc.copy()
            h['id'] = str(doc['_id'])
            yield h

    def get_doc(self, doc_id, doc_class=HTMLDocument):
        d = self.get(doc_id)
        h = d.copy()
        h['id'] = str(d['_id'])
        del h['_id']
        return doc_class(h)
