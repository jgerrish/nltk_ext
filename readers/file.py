from nltk_ext.documents.document import Document


class FileReader(object):
    def __init__(self, source):
        self.data = None
        if source:
            self.source = source
            self.read()

    # TODO: Make this use the context manager API
    def read(self, source=None):
        # override constructor source if specified
        if source:
            self.source = source
        with open(self.source, "r") as f:
            self.data = f.read().replace("\n", " ")
        return self.data

    # get the next document in the source
    # currently the FileReader only reads a single document
    def next(self):
        if self.cursor_position > 0:
            raise StopIteration
        else:
            self.cursor_position += 1
            return {"id": self.source, "body": self.data}

    def process(self, data):
        doc = Document({"id": self.source, "body": self.data})
        for doc in [doc]:
            yield doc

    def __iter__(self):
        self.cursor_position = 0
        return self
