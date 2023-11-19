# Count number of characters in a document


class CharCount(object):
    def __init__(self, new_attribute="char_count"):
        self.new_attribute = new_attribute

    def process_text(self, text):
        if text == "":
            return text
        return len(text)

    def process(self, documents):
        for document in documents:
            if type(document) == str:
                yield self.process_text(document)
            else:
                new_val = self.process_text(document)
                document.set(self.new_attribute, new_val)
                yield document
