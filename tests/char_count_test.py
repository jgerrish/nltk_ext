import unittest
from nltk_ext.documents.document import Document
from nltk_ext.documents.html_document import HTMLDocument
from nltk_ext.pipelines.char_count import CharCount

class CharCountTestCase(unittest.TestCase):
    def setUp(self):
        self.d1 = Document({"id": "1", "body": "This this."})
        self.d2 = Document({"id": "2", "body": "This is another test document."})
        self.d3 = HTMLDocument({"id": "1",
                                "body_text": "Derp a derp\nA derp derp"})
        self.d4 = "Derp a derp\nA derp derp"
        self.docs = [self.d1, self.d2, self.d3]

    def test_boilerpipe_extractor_with_attribute(self):
        r = CharCount("char_count")
        docs = list(r.process(self.docs))
        self.assertEqual(docs[0].document["char_count"], 10)
        self.assertEqual(docs[1].document["char_count"], 30)
        self.assertEqual(docs[2].document["char_count"], 23)

    def test_boilerpipe_extractor_without_attribute(self):
        r = CharCount()
        docs = list(r.process(self.docs))
        self.assertEqual(docs[0].document["char_count"], 10)
        self.assertEqual(docs[1].document["char_count"], 30)
        self.assertEqual(docs[2].document["char_count"], 23)

    def test_boilerpipe_extractor_str(self):
        r = CharCount()
        docs = list(r.process([self.d4]))
        self.assertEqual(docs[0], 23)

def suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromTestCase(CharCountTestCase))
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
