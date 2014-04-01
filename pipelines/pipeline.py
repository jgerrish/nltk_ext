from nltk_ext.filters.filter_chain import FilterChain

# TODO: Make this class iterable
class Pipeline():
    def __init__(self, modules=[], filter_chain=None):
        self.modules = modules
        self.filter_chain = filter_chain if filter_chain else FilterChain()

    def add_filter(self, f):
        self.filter_chain.add(f)

    def add_module(self, m):
        self.modules.append(m)

    def process(self, document):
        if self.filter_chain.check(document):
            res = document
            for p in self.modules:
                res = p.process(document.doc_id, res)
            return res
        else:
            return None

    def process_corpus(self, corpus):
        """
        provide methods on Pipeline in addition to Corpus to process collections
        of documents.
        """
        for doc in corpus:
            res = self.process(doc)
