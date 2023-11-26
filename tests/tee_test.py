import unittest
from nltk_ext.documents.document import Document
from nltk_ext.pipelines.identity import Identity
from nltk_ext.pipelines.tee import Tee


class TeeTestCase(unittest.TestCase):
    def setUp(self):
        self.d1 = Document({"id": "1", "body": "A test of a unique filter pipeline."})

    def test_document(self):
        words = []
        for word in self.d1.words():
            words.append(word)
        self.assertEqual(len(words), 8)
        self.assertEqual(words[1], "test")

    def document_test(self, words):
        self.assertEqual(len(words), 8)
        self.assertEqual(words[0], "a")
        self.assertEqual(words[1], "test")
        self.assertEqual(words[2], "of")
        self.assertEqual(words[3], "a")

    def test_tee(self):
        identity = Identity()
        t = Tee(identity)
        self.assertEqual(len(self.d1.words()), 8)
        words = list(t.process(self.d1.words()))
        self.document_test(words)
        words2 = list(t.alternate())
        self.document_test(words2)


def suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromTestCase(TeeTestCase))
    return suite


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite())
