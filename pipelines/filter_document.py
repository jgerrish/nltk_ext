# filter a document down to a select list of attributes
# useful for processing large sets of documents in memory
from typing import Iterator, List, Optional, Union

from nltk_ext.documents.document import Document


# Document pipeline module to filter a document by attributes
class FilterDocument(object):
    def __init__(self, attributes: Optional[List[str]] = None):
        self.attributes = attributes

    def process(
        self,
        data: Union[List[str], List[Document]],
        attributes: Optional[List[str]] = None,
    ) -> Iterator[Union[str, Document]]:
        for document in data:
            if (self.attributes is not None) and isinstance(document, Document):
                d = {key: document.document[key] for key in self.attributes}
                yield Document(d)
            else:
                yield document
