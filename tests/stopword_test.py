import unittest
from nltk_ext.documents.document import Document
from nltk_ext.filters.stopword import StopwordFilter


class StopwordFilterTestCase(unittest.TestCase):
    def setUp(self):
        self.d1 = Document({"id": "1", "body": "A stopword test."}, [StopwordFilter()])

    def test_document(self):
        words = []
        for word in self.d1.words():
            words.append(word)
        self.assertEqual(len(words), 3)
        self.assertEqual(words[0], "stopword")


def suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromTestCase(StopwordFilterTestCase))
    return suite


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite())
