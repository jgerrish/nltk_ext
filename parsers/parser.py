from abc import ABCMeta, abstractmethod

class Parser():
    """
    Abstract base class for parsers
    Parser modules are usually run after reader modules to convert a
    channel-specific format into a Document.
    Examples include extracting messages from Facebook Graph objects
    and body text from HTML pages.
    Concrete classes must implement a parse method
    The process method is called for each document, sentence or word depending on
    the module type.
    TODO: define general mapping from document formats into Document model
    TODO: maybe re-factor this, not necessarily needed with subclassed Documents
    """
    @abstractmethod
    def parse(self, data, attributes=None):
        pass
