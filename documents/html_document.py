from typing import Any, List, Optional

from nltk_ext.documents.document import Document
from nltk_ext.filters.filter import Filter


class HTMLDocument(Document):
    BodyAttribute = "body_text"
    # BodyAttribute = "title"

    def __init__(self, data: Any, word_filters: Optional[List[Filter]] = None) -> None:
        if type(data) == str:
            self.document = {}
            self.document[Document.BodyAttribute] = data
            self.body_attribute = Document.BodyAttribute
        else:
            keys = data.keys()
            self.__dict__.update(zip(keys, [data[key] for key in keys]))
            self.document = data.copy()
            self.body_attribute = HTMLDocument.BodyAttribute
        if "id" in data:
            self.set_doc_id(self.document["id"])
        if "doc_char_count" in data:
            self.doc_char_count = self.document["doc_char_count"]
        if "sorted_hashed_ngrams" in data:
            self.sorted_hashed_ngrams = self.document["sorted_hashed_ngrams"]
        # if Document.BodyAttribute in data:
        #    self.nltk_text = Text(unicode(self.document["body_text"]))
        self.nltk_text = None
        # document or domain specific metadata that is currently un-mapped
        if "metadata" in data:
            self.metadata = self.document["metadata"]

        self._freq_dist = None
        if word_filters is not None:
            self.word_filters = word_filters
        else:
            self.word_filters = []
        # super(HTMLDocument, self).__init__(data)
        # super(self.__class__, self).__init__(data)
        # Document.__init__(self, data)
