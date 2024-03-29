import unittest
from nltk_ext.documents.document import Document
from nltk_ext.filters.document_blacklist import DocumentBlacklist


class DocumentBlacklistTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.d1 = Document(
            {
                "id": "1",
                "url": "http://www.baddomain.com/test",
                "body": "A URL blacklist test.",
            }
        )
        self.d2 = Document(
            {
                "id": "2",
                "url": "http://www.gooddomain.com/test",
                "body": "A URL blacklist test.",
            }
        )
        self.docs = [self.d1, self.d2]
        self.url_blacklist = ["^http://www.baddomain.com/"]

    def test_document_blacklist(self) -> None:
        blacklist = DocumentBlacklist("url", self.url_blacklist)
        docs = list(blacklist.process(self.docs))
        self.assertEqual(len(docs), 1)
        if isinstance(docs[0], Document):
            self.assertEqual(docs[0].doc_id, "2")
        else:
            self.fail("process should return list of documents")


def suite() -> unittest.suite.TestSuite:
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromTestCase(DocumentBlacklistTestCase))
    return suite


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite())
