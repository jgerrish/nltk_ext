from nltk import FreqDist

class Index:
    """
    The Index class stores an index for a document.
    """
    def __init__(self):
        self._freq_dist = None
        self._document = None

    def index(self, document):
        self._document = document
        if self._freq_dist == None:
            self._freq_dist = FreqDist()
            for term in self.terms():
                self._freq_dist[term] += 1

    def reset(self):
        "Reset the index"
        self._freq_dist = None

    def freq_dist(self):
        if self._freq_dist == None:
            self.index()
        return self._freq_dist

    # return the number of times a term appears in this document
    def freq(self, term):
        if not self._freq_dist:
            self.index()
        return self._freq_dist[term]

    def tf(self, term):
        if not self._freq_dist:
            self.index()
        return float(self._freq_dist[term]) / float(self._freq_dist.N())
