# Module to return uniq elements given a list of elements
# Stores every item seen in the stream, for large collections,
# use the RedisUniq Redis-backed uniq module
import itertools

class Uniq(object):
    def __init__(self):
        self.items = set()

    def process(self, data):
        for s in data:
            if s not in self.items:
                self.items.add(s)
                yield s
