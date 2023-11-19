# MongoDB Writer module
from pymongo import MongoClient
from bson.objectid import ObjectId
from nltk_ext.pipelines.pipeline_module import PipelineModule


# Item pipeline to write the item to a MongoDB store
class MongoWriter(PipelineModule):
    """
    Initialize a MongoWriter object for a pipeline

    If the operation is of type insert, you can specify the keys to
    update in the constructor.
    """

    def __init__(
        self,
        db="spout_test",
        collection="documents",
        operation="insert",
        keys=[],
    ):
        self.mongodb_client = MongoClient()
        self.db = self.mongodb_client[db]
        self.collection = self.db[collection]
        self.operation = operation
        self.keys = keys

    def process(self, documents, keys=None):
        if (keys is None) and (self.keys is not None):
            keys = self.keys
        for d in documents:
            doc_id = d.doc_id
            if self.operation == "insert":
                self.collection.insert(d.document)
            elif self.operation == "update":
                if keys is None:
                    self.collection.update({"_id": ObjectId(doc_id)}, d.document)
                else:
                    filtered_dict = {key: d.document[key] for key in keys}
                    self.collection.update(
                        {"_id": ObjectId(doc_id)}, {"$set": filtered_dict}
                    )
                    # doc = self.collection.find_one({'_id': ObjectId(doc_id)})
            yield d
