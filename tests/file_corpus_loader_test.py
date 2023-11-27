import unittest
from nltk_ext.documents.document import Document
from nltk_ext.corpus.file_corpus_loader import FileCorpusLoader


class FileCorpusLoaderTest(unittest.TestCase):
    def setUp(self) -> None:
        self.d1 = Document({"id": "1", "body": "A test of a unique filter pipeline."})

    def test_init(self) -> None:
        self.fcl1 = FileCorpusLoader(13)
        self.assertEqual(self.fcl1.max_cnt, 13)


def suite() -> unittest.suite.TestSuite:
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromTestCase(FileCorpusLoaderTest))
    return suite


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite())
