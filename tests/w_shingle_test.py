import unittest
from nltk_ext.documents.html_document import HTMLDocument
from nltk_ext.pipelines.w_shingle import WShingle

class WShingleTestCase(unittest.TestCase):
    def setUp(self):
        self.d1 = HTMLDocument({"id": "1",
                                "body_text": "Derp a derp\nA derp derp"})
        self.d2 = "Derp a derp\nA derp derp"
        self.docs = [self.d1]

    def test_boilerpipe_extractor_with_attribute(self):
        r = WShingle(2, "w_shingles")
        docs = list(r.process(self.docs))
        shingles = list(docs[0].document["w_shingles"])
        self.assertEqual(len(shingles), 3)
        self.assertItemsEqual(shingles, [4511874163119075276,
                                         586875170268770749,
                                         1339662791857901318])

    def test_boilerpipe_extractor_without_attribute(self):
        r = WShingle(2)
        docs = list(r.process(self.docs))
        shingles = list(docs[0])
        self.assertEqual(len(shingles), 3)
        self.assertItemsEqual(shingles, [4511874163119075276,
                                         586875170268770749,
                                         1339662791857901318])

    def test_boilerpipe_extractor_str(self):
        r = WShingle(2)
        docs = list(r.process([self.d2]))
        shingles = list(docs[0])
        self.assertEqual(len(shingles), 3)
        self.assertItemsEqual(shingles, [4511874163119075276,
                                         586875170268770749,
                                         1339662791857901318])

def suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromTestCase(WShingleTestCase))
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
