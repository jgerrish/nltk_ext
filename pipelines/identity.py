class Identity(object):
    """
    Identity pipeline module that simply yields the stream
    """

    def process(self, source, data=None):
        for s in source:
            yield s
