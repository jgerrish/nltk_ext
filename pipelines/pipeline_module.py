from abc import abstractmethod


class enumModuleType:
    """
    Based on enum example found on stackoverflow:
    http://stackoverflow.com/questions/702834/whats-the-common-practice-for-enums-in-python
    """

    Document = 0
    Sentence = 1
    Word = 2

    def __init__(self, Type):
        self.value = Type

    def __str__(self):
        if self.value == enumModuleType.Document:
            return "Document"
        if self.value == enumModuleType.Sentence:
            return "Sentence"
        if self.value == enumModuleType.Word:
            return "Word"

    def __eq__(self, y):
        return self.value == y.value


class enumModuleProcessingType:
    """
    This enumeration type indicates at what point in the processing pipeline
    the module has data ready.

    Right now there are two options: after each iteration of
    process(), or at the end of processing via post_process()

    Based on enum example found on stackoverflow:
    http://stackoverflow.com/questions/702834/whats-the-common-practice-for-enums-in-python

    """  # :noqa E501

    Process = 0
    PostProcess = 1

    def __init__(self, Type):
        self.value = Type

    def __str__(self):
        if self.value == enumModuleProcessingType.Document:
            return "Document"
        if self.value == enumModuleProcessingType.Sentence:
            return "Sentence"
        if self.value == enumModuleProcessingType.Word:
            return "Word"

    def __eq__(self, y):
        return self.value == y.value


class PipelineModule:
    """
    Abstract base class for pipeline modules
    Concrete classes must implement a process method

    The process method is called for each document, sentence or word
    depending on the module type.
    """

    def __init__(self):
        self.before_process_callbacks = []
        self.after_process_callbacks = []

    @abstractmethod
    def process(self, data, attributes=None):
        for cb in self.before_process_callbacks:
            cb(data, attributes)

        res = self._process(data, attributes)

        for cb in self.after_process_callbacks:
            cb(data, attributes)

        return res

    def add_before_process_callback(self, cb):
        self.before_process_callbacks.append(cb)

    def add_after_process_callback(self, cb):
        self.after_process_callbacks.append(cb)

    def process_all(self, data, attributes=None):
        for d in self.process(data, attributes):
            continue
