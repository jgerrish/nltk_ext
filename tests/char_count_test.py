import unittest
from nltk_ext.documents.document import Document
from nltk_ext.documents.html_document import HTMLDocument
from nltk_ext.pipelines.char_count import CharCount


class CharCountTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.d1 = Document({"id": "1", "body": "This this."})
        self.d2 = Document({"id": "2", "body": "This is another test document."})
        self.d3 = HTMLDocument({"id": "1", "body_text": "Derp a derp\nA derp derp"})
        self.d4 = "Derp a derp\nA derp derp"
        self.docs = [self.d1, self.d2, self.d3]

    def test_boilerpipe_extractor_with_attribute(self) -> None:
        r = CharCount("char_count")
        docs = list(r.process(self.docs))
        if isinstance(docs[0], Document):
            self.assertEqual(docs[0].document["char_count"], 10)
        else:
            self.fail("process should return list of documents")
        if isinstance(docs[1], Document):
            self.assertEqual(docs[1].document["char_count"], 30)
        else:
            self.fail("process should return list of documents")
        if isinstance(docs[2], Document):
            self.assertEqual(docs[2].document["char_count"], 23)
        else:
            self.fail("process should return list of documents")

    def test_boilerpipe_extractor_without_attribute(self) -> None:
        r = CharCount()
        docs = list(r.process(self.docs))
        if isinstance(docs[0], Document):
            self.assertEqual(docs[0].document["char_count"], 10)
        else:
            self.fail("process should return list of documents")
        if isinstance(docs[1], Document):
            self.assertEqual(docs[1].document["char_count"], 30)
        else:
            self.fail("process should return list of documents")
        if isinstance(docs[2], Document):
            self.assertEqual(docs[2].document["char_count"], 23)
        else:
            self.fail("process should return list of documents")

    def test_boilerpipe_extractor_str(self) -> None:
        r = CharCount()
        docs = list(r.process([self.d4]))
        self.assertEqual(docs[0], 23)

    def test_char_count_empty_document(self) -> None:
        d1 = Document({"id": "1", "body": ""})
        r = CharCount()
        docs = list(r.process([d1]))
        if isinstance(docs[0], Document):
            self.assertEqual(docs[0].document["char_count"], 0)
        else:
            self.fail("process should return list of documents")

    def test_char_count_empty_string(self) -> None:
        s1 = ""
        r = CharCount()
        lengths = list(r.process([s1]))
        self.assertEqual(lengths[0], 0)


def suite() -> unittest.suite.TestSuite:
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromTestCase(CharCountTestCase))
    return suite


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite())
