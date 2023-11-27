import unittest
from nltk_ext.pipelines.create_document import CreateDocument


class CreateDocumentTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.d1 = {"body": "a document test"}
        self.d2 = "a second document test"

    def test_create_document_from_dict(self) -> None:
        r = CreateDocument()
        docs = list(r.process([self.d1]))
        self.assertEqual(len(docs), 1)
        doc = docs[0]
        self.assertEqual(doc.document["body"], "a document test")

    def test_create_document_from_str(self) -> None:
        r = CreateDocument()
        docs = list(r.process([self.d2]))
        self.assertEqual(len(docs), 1)
        doc = docs[0]
        self.assertEqual(doc.document["body"], "a second document test")


def suite() -> unittest.suite.TestSuite:
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromTestCase(CreateDocumentTestCase))
    return suite


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite())
