import unittest
from nltk_ext.documents.document import Document
from nltk_ext.documents.html_document import HTMLDocument
from nltk_ext.pipelines.w_shingle import WShingle


class WShingleTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.d1 = HTMLDocument({"id": "1", "body_text": "Derp a derp\nA derp derp"})
        self.d2 = "Derp a derp\nA derp derp"
        self.docs = [self.d1]

    def test_boilerpipe_extractor_with_attribute(self) -> None:
        r = WShingle(2, "w_shingles")
        docs = list(r.process(self.docs))
        doc1 = docs[0]
        if isinstance(doc1, Document):
            shingles = list(doc1.document["w_shingles"])
        else:
            assert "WShingle Process should return a Document"
        # Could write a custom hashing algorithm so this is
        # more stable between Python versions
        ngrams = [("derp", "a"), ("derp", "derp"), ("a", "derp")]
        hashes = [hash(x) for x in ngrams]
        self.assertEqual(len(list(shingles)), 3)
        self.assertEqual(set(shingles), set(hashes))

    def test_boilerpipe_extractor_without_attribute(self) -> None:
        r = WShingle(2)
        docs = list(r.process(self.docs))
        shingles = docs[0]
        ngrams = [("derp", "a"), ("derp", "derp"), ("a", "derp")]
        hashes = [hash(x) for x in ngrams]
        if type(shingles) == list:
            self.assertEqual(len(shingles), 3)
            self.assertSetEqual(set(shingles), set(hashes))
        else:
            self.fail("process should return list of shingles")

    def test_boilerpipe_extractor_str(self) -> None:
        r = WShingle(2)
        docs = list(r.process([self.d2]))
        shingles = docs[0]
        ngrams = [("a", "derp"), ("derp", "a"), ("derp", "derp")]
        hashes = [hash(x) for x in ngrams]
        if type(shingles) == list:
            self.assertEqual(len(shingles), 3)
            self.assertSetEqual(set(shingles), set(hashes))
        else:
            self.fail("process should return list of shingles")


def suite() -> unittest.suite.TestSuite:
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromTestCase(WShingleTestCase))
    return suite


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite())
