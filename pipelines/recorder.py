class Recorder(object):
    """
    Recorder pipeline module that records the current state of the
    pipeline data at a stage in the pipeline.
    Useful for testing pipeline processing and pulling out intermediate
    data.
    """
    def __init__(self, data=[]):
        self.data = data

    def get_data(self):
        "Return the recorded data"
        return self.data

    def clear_data(self):
        "Clear the recorded data"
        self.data = []

    def process(self, source, data=None):
        for s in source:
            self.data.append(s)
            yield s
