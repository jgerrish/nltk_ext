from typing import Any, List, Optional

from nltk_ext.corpus.corpus import Corpus
from nltk_ext.filters.filter_chain import FilterChain
from nltk_ext.pipelines.pipeline_module import PipelineModule


# TODO: Make this class iterable
class Pipeline:
    def __init__(
        self,
        modules: List[PipelineModule] = [],
        filter_chain: Optional[FilterChain] = None,
    ) -> None:
        self.modules = modules
        self.filter_chain = filter_chain if filter_chain else FilterChain()

    def add_filter(self, f: Any) -> None:
        self.filter_chain.add(f)

    def add_module(self, m: Any) -> None:
        self.modules.append(m)

    def process(self, document: Any) -> Optional[Any]:
        if self.filter_chain.check(document):
            res = document
            for p in self.modules:
                res = p.process(document.doc_id, res)
            return res
        else:
            return None

    def process_corpus(self, corpus: Corpus) -> None:
        """
        provide methods on Pipeline in addition to Corpus to process
        collections of documents.
        """
        for doc in corpus:
            self.process(doc)
