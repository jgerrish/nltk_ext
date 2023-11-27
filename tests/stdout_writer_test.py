import unittest
from nltk_ext.documents.document import Document


class StdoutWriterTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.d1 = Document({"id": "1", "body": "A test of a unique filter pipeline."})

    def test_document(self) -> None:
        words = []
        for word in self.d1.words():
            words.append(word)
        self.assertEqual(len(words), 8)
        self.assertEqual(words[1], "test")

    # def test_stdout_writer(self) -> None:
    #    r = StdoutWriter()
    #    words = r.process(self.d1.words())
    #    self.assertIsNone(words)


def suite() -> unittest.suite.TestSuite:
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromTestCase(StdoutWriterTestCase))
    return suite


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite())
