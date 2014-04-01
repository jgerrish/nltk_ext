# Run custom code in the pipeline

class Custom(object):
    def __init__(self, custom_func):
        self.custom_func = custom_func

    def process(self, documents):
        for document in documents:
            yield self.custom_func(document)
