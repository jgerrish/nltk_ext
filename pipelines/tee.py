import itertools

class Tee(object):
    """
    The tee module lets you split a pipeline into two separate paths
    The first path is the normal pipeline path, acting as an identity
    map.  The second path should be passed into the constructor.
    The iterators should be consumed roughly at the same rate or
    more memory will be used.
    """
    def __init__(self, module):
        self.module = module

    def alternate(self):
        "get the alternate path"
        return self.module.process(self.alt_stream)

    def process(self, source, data=None):
        paths = itertools.tee(source)
        self.alt_stream = paths[1]
        return paths[0]
