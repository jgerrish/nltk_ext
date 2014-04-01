import unittest
from nltk_ext.documents.document import Document

class DocumentTestCase(unittest.TestCase):
    def setUp(self):
        self.d1 = Document({"id": "1", "body": "This this."})
        self.d2 = Document({"id": "2", "body": "This is another test document."})
        self.d3 = Document({"id": "3", "body": "Two words."})
        self.d4 = Document({"id": "3", "body": "Derp a derp.\nA derp derp."})

    def test_init(self):
        d1 = Document({"id": "1", "body": "This this."})
        self.assertEqual(d1.doc_id, "1")
        self.assertEqual(str(d1), "This this.")
        d2 = Document("This this.")
        self.assertEqual(str(d1), "This this.")

    def test_index(self):
        self.assertEqual(self.d1._freq_dist, None)
        self.assertEqual(self.d2._freq_dist, None)
        self.assertEqual(self.d3._freq_dist, None)
        self.d1.index()
        self.d2.index()
        self.d3.index()
        self.assertNotEqual(self.d1._freq_dist, None)
        self.assertNotEqual(self.d2._freq_dist, None)
        self.assertNotEqual(self.d3._freq_dist, None)

        # periods are considered words by default in NLTK
        self.assertEqual(len(self.d1._freq_dist), 2)
        self.assertEqual(self.d1._freq_dist["this"], 2)
        self.assertEqual(self.d1._freq_dist["."], 1)

        self.assertEqual(len(self.d2._freq_dist), 6)
        self.assertEqual(self.d2._freq_dist["this"], 1)
        self.assertEqual(self.d2._freq_dist["is"], 1)
        self.assertEqual(self.d2._freq_dist["another"], 1)
        self.assertEqual(self.d2._freq_dist["test"], 1)
        self.assertEqual(self.d2._freq_dist["document"], 1)
        self.assertEqual(self.d2._freq_dist["."], 1)

        self.assertEqual(len(self.d3._freq_dist), 3)
        self.assertEqual(self.d3._freq_dist["two"], 1)
        self.assertEqual(self.d3._freq_dist["words"], 1)
        self.assertEqual(self.d3._freq_dist["."], 1)

    def test___str__(self):
        self.assertEqual(str(self.d1), "This this.")
        self.assertEqual(str(self.d2), "This is another test document.")
        self.assertEqual(str(self.d3), "Two words.")

    def test_update_text(self):
        self.assertEqual(str(self.d1), "This this.")
        self.d1.update_text("more words")
        self.assertEqual(str(self.d1), "more words")

    def test_words(self):
        words = list(self.d4.words())
        self.assertEqual(len(words), 8)
        self.assertEqual(words[0], "derp")
        self.assertEqual(words[1], "a")
        self.assertEqual(words[2], "derp")
        self.assertEqual(words[3], ".")
        self.assertEqual(words[4], "a")
        self.assertEqual(words[5], "derp")
        self.assertEqual(words[6], "derp")
        self.assertEqual(words[7], ".")

    def test_to_ngrams(self):
        ngrams = self.d4.to_ngrams(2)
        self.assertEqual(ngrams, [("derp", "a"), ("a", "derp"), ("derp", "."),
                                  (".", "a"), ("a", "derp"), ("derp", "derp"),
                                  ("derp", ".")])

def suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromTestCase(DocumentTestCase))
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
