# w-shingling generator
from typing import Iterator, List, Optional, Union

from nltk_ext.documents.document import Document


# Document pipeline module to generate w-shingles for a document
# The w-shingles for a document are the set of hashed unique n-grams
# in that document
# If a document attribute is given in the constructor, assign the
# hashes to that attribute and yield the document.  Otherwise yield
# the hashes themselves.
class WShingle(object):
    def __init__(self, ngram_size: int = 10, attribute: Optional[str] = None) -> None:
        self.ngram_size = ngram_size
        self.attribute = attribute

    def process(
        self, documents: List[Union[Document, str]]
    ) -> Iterator[Union[Document, List[int]]]:
        for document in documents:
            if isinstance(document, Document):
                ngrams = document.to_ngrams(self.ngram_size)
            elif type(document) == str:
                doc = Document(document)
                ngrams = doc.to_ngrams(self.ngram_size)
            uniq = set(ngrams)
            # Instead of using the Python hash function, we could
            # include a language-agnostic hash so hashes don't
            # possibly change between Python versions.
            # If your use cases involve long-term storage, this is
            # probably a good addition.
            hashes = [hash(ng) for ng in uniq]
            if isinstance(document, Document) and self.attribute:
                document.set(self.attribute, hashes)
                yield document
            else:
                yield hashes
