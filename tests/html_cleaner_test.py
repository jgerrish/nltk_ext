import unittest
from nltk_ext.documents.document import Document
from nltk_ext.pipelines.html_cleaner import HtmlCleaner


class HtmlCleanerTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.d1 = Document(
            {
                "id": "1",
                "body": "A test of a html cleaner pipeline.<br/> Another sentence.",  # noqa: E501
            }
        )
        self.docs = [self.d1]

    def test_document(self) -> None:
        words = []
        for word in self.d1.words():
            words.append(word)
        self.assertEqual(len(words), 13)
        self.assertEqual(words[1], "test")

    def test_html_cleaner_docs(self) -> None:
        r = HtmlCleaner()
        docs = list(r.process(self.docs))
        words = list(docs[0].words())
        self.assertEqual(len(words), 11)
        self.assertEqual(words[6], "pipeline")
        self.assertEqual(words[7], ".")
        self.assertEqual(words[8], "another")

    def test_html_cleaner_strings(self) -> None:
        r = HtmlCleaner()
        docs = list(r.process([self.d1["body"]]))
        words = docs[0]
        self.assertEqual(len(words), 53)
        self.assertEqual(words[33], ".")
        self.assertEqual(words[34], "\n")
        self.assertEqual(words[35], " ")


def suite() -> unittest.suite.TestSuite:
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromTestCase(HtmlCleanerTestCase))
    return suite


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite())
