import unittest
from nltk_ext.documents.document import Document

class UnigramIndexTestCase(unittest.TestCase):
    def setUp(self):
        self.d1 = Document({"id": "1", "body": "This this."})
        self.d2 = Document({"id": "2", "body": "This is another test document."})
        self.d3 = Document({"id": "3", "body": "Two words."})
        self.d4 = Document({"id": "3", "body": "Derp a derp.\nA derp derp."})

    def test_index(self):
        self.assertEqual(self.d1._index, None)
        self.assertEqual(self.d2._index, None)
        self.assertEqual(self.d3._index, None)
        self.d1.index()
        self.d2.index()
        self.d3.index()
        d1_index = self.d1._index
        d2_index = self.d2._index
        d3_index = self.d3._index
        self.assertNotEqual(d1_index._freq_dist, None)
        self.assertNotEqual(d2_index._freq_dist, None)
        self.assertNotEqual(d3_index._freq_dist, None)

        # periods are considered words by default in NLTK
        self.assertEqual(len(d1_index._freq_dist), 2)
        self.assertEqual(d1_index._freq_dist["this"], 2)
        self.assertEqual(d1_index._freq_dist["."], 1)

        self.assertEqual(len(d2_index._freq_dist), 6)
        self.assertEqual(d2_index._freq_dist["this"], 1)
        self.assertEqual(d2_index._freq_dist["is"], 1)
        self.assertEqual(d2_index._freq_dist["another"], 1)
        self.assertEqual(d2_index._freq_dist["test"], 1)
        self.assertEqual(d2_index._freq_dist["document"], 1)
        self.assertEqual(d2_index._freq_dist["."], 1)

        self.assertEqual(len(d3_index._freq_dist), 3)
        self.assertEqual(d3_index._freq_dist["two"], 1)
        self.assertEqual(d3_index._freq_dist["words"], 1)
        self.assertEqual(d3_index._freq_dist["."], 1)


def suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromTestCase(UnigramIndexTestCase))
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
