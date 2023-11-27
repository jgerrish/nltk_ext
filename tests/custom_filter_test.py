import unittest
from nltk_ext.documents.document import Document
from nltk_ext.filters.custom_filter import CustomFilter


class CustomFilterTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.d1 = Document({"id": "1", "body": "first test document"})
        self.d2 = Document({"id": "2", "body": "second test document"})
        self.d3 = Document({"id": "3", "body": "short document"})
        self.d4 = Document({"id": "4", "body": "fourth test document"})
        self.docs = [self.d1, self.d2, self.d3, self.d4]

    def test_custom_filter_docs(self) -> None:
        r = CustomFilter(lambda x: len(x) >= 15)
        docs = list(r.process(self.docs))
        self.assertEqual(len(docs), 3)
        if isinstance(docs[0], Document):
            self.assertEqual(docs[0].doc_id, "1")
        else:
            self.fail("process should return list of documents")
        if isinstance(docs[1], Document):
            self.assertEqual(docs[1].doc_id, "2")
        else:
            self.fail("process should return list of documents")
        if isinstance(docs[2], Document):
            self.assertEqual(docs[2].doc_id, "4")
        else:
            self.fail("process should return list of documents")


def suite() -> unittest.suite.TestSuite:
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromTestCase(CustomFilterTestCase))
    return suite


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite())
