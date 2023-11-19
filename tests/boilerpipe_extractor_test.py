import unittest
from nltk_ext.documents.html_document import HTMLDocument
from nltk_ext.pipelines.boilerpipe_extractor import BoilerpipeExtractor


class BoilerpipeExtractorTestCase(unittest.TestCase):
    def setUp(self):
        self.d1 = HTMLDocument(
            {
                "id": "1",
                "body": "<html><head><title>test title</title></head><body><p>A test of a boilerpipe extractor.</p>\n<p>Another sentence.</p>",  # noqa: E501
            }
        )
        self.docs = [self.d1]

    def test_boilerpipe_extractor_docs(self):
        r = BoilerpipeExtractor()
        docs = list(r.process(self.docs))
        words = list(docs[0].words())
        self.assertEqual(len(words), 10)
        self.assertEqual(words[5], "extractor")
        self.assertEqual(words[6], ".")
        self.assertEqual(words[7], "another")

    def test_boilerpipe_extractor_strings(self):
        r = BoilerpipeExtractor()
        docs = list(r.process([self.d1["body"]]))
        words = docs[0]
        self.assertEqual(len(words), 52)
        self.assertEqual(words[32], ".")
        self.assertEqual(words[33], "\n")
        self.assertEqual(words[34], "A")


def suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromTestCase(BoilerpipeExtractorTestCase))
    return suite


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite())
