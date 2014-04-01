# A random filter that drops a random number of documents based on
# simple uniform probability distribution
import random

class RandomFilter(object):
    # Initialize the RandomFilter with a drop probability,
    # probability is the drop probability
    def __init__(self, probability=0.8, randgen=None):
        self.probability = probability
        self.randgen = randgen

    def filter(self, elements):
        for elem in elements:
            if self.randgen:
                rnd = self.randgen()
            else:
                rnd = self.r.random()
            if rnd >= self.probability:
                yield elem

    def process(self, docs):
        return self.filter(docs)

    #def filter(self, elem):
    #    if self.randgen:
    #        rnd = self.randgen()
    #    else:
    #        rnd = self.r.random()
    #    return rnd >= self.probability
