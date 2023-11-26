# category_to_corpus converts a set of documents tagged with categories
# to a set of corpora, with each corpus corresponding to a single tag/category
import json
import pprint
from typing import Dict, Iterator, List, Optional, Union

from nltk_ext.corpus.corpus import Corpus
from nltk_ext.documents.document import Document
from nltk_ext.pipelines.pipeline_module import (
    enumModuleType,
    enumModuleProcessingType,
    PipelineModule,
)

# TODO Should use a Corpus in corpora instead of a list of documents
# same applies elsewhere
CorporaType = Dict[str, List[Document]]

# TODO In addition, this shouldn't be a union, should use a different
# type.
CombinedCorpusType = Union[Corpus, CorporaType]


class CategoryToCorpus(PipelineModule):
    def __init__(
        self,
        output: str = None,
        corpus: Corpus = None,
        attribute: str = "categories",
        categories: List[str] = None,
        mode: str = "combined",
    ) -> None:
        """
        Create a CategoryToCorpus module, which loads a corpus with tagged
        documents.
        If corpus is passed in, it adds to an existing corpus.
        mode is the corpus loading method to use.  If set to "combined", all
        documents in a category are concatenated to a single document.
        Otherwise each document is loaded separately.
        """
        self.output = output
        self.corpora: CorporaType = {}
        # combined mode has a single corpus
        if corpus is None:
            self.corpus = Corpus()
        else:
            self.corpus = corpus
        self.module_type = enumModuleType.Document
        self.module_processing_type = enumModuleProcessingType.PostProcess
        self.attribute = attribute
        self.categories = categories
        self.mode = mode
        self.pp = pprint.PrettyPrinter(indent=4)

    def add_document(self, category: str, document: Document) -> None:
        if self.mode != "combined":
            if category in self.corpora:
                self.corpora[category].append(document)
            else:
                self.corpora[category] = [document]
        else:
            if category in self.corpus:
                d = self.corpus[category]
                d.update_text("{} {}".format(d, document))
                # d.update_text(unicode(d) + " " + unicode(document))
            else:
                document.set_doc_id(category)
                self.corpus.add(document)

    def process(
        self,
        data: Union[List[str], List[Document]],
        attributes: Optional[List[str]] = None,
    ) -> Iterator[Union[str, Document]]:
        """
        Process the documents.  The code looks at the attribute
        attribute, which should be a list or dictionary,
        and builds a set of corpora from categories in that
        attribute.
        If category is set, it only builds a single corpus containing
        documents with that category.
        """
        for doc in data:
            if type(doc) == str:
                return
            if isinstance(doc, Document) and (self.attribute in doc.document):
                d = doc.document[self.attribute]
                # TODO: Double check by adding a test that the
                # behavior is correct now
                if (type(d) is not list) and (type(d) is not dict):
                    return
                if self.categories is None:
                    for v in d:
                        self.add_category_document(v, doc)
                else:
                    for category in self.categories:
                        if category in d:
                            self.add_category_document(category, doc)
            yield doc

    def add_category_document(
        self,
        category: str,
        doc: Union[str, Document],
    ) -> None:
        if type(doc) == str:
            self.add_document(category, Document(doc))
        elif isinstance(doc, Document):
            self.add_document(category, doc)

    def post_process(self) -> CombinedCorpusType:
        """
        method that gets run after all data has been processed

        TODO: look into optimizing this, seems inefficient, written in
        derp-mode
        """
        if self.mode != "combined":
            return self.corpora
        else:
            return self.corpus

    def as_json(self) -> str:
        # TODO: Refactor this to have a common "root" type
        c: Optional[CombinedCorpusType] = None
        if self.mode != "combined":
            c = self.corpora
        else:
            c = self.corpus
        return json.dumps(c, sort_keys=True, indent=4, separators=(",", ": "))

    def write(self) -> None:
        if self.output is not None:
            f = open(self.output, "w")
            f.write(self.as_json())
            f.close()

    def top_categories(self, n: int = 10) -> None:
        for doc_id in self.categories:
            print(doc_id)
            rt = self.corpus.ranked_terms(doc_id, n)
            print("  {}".format(rt))
