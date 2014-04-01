from nltk_ext.filters.filter_chain import FilterChain

class GeneratorPipeline():
    """
    New interface to pipeline processing system that doesn't rely on documents
    """
    def __init__(self, modules=[], filter_chain=None):
        self.modules = modules
        self.filter_chain = filter_chain if filter_chain else FilterChain()

    def add_filter(self, f):
        self.filter_chain.add(f)

    def add_module(self, m):
        self.modules.append(m)

    def process(self, data):
        if self.filter_chain.check(data):
            res = data
            for p in self.modules:
                res = p.process(res)
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
