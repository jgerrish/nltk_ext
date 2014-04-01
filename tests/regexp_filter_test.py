import unittest
from nltk_ext.documents.document import Document
from nltk_ext.filters.regexp import RegexpFilter

class RegexpFilterTestCase(unittest.TestCase):
    def setUp(self):
        self.d1 = Document({"id": "1", "body": "A stopword test."},
                           [RegexpFilter("^.$")])

    def test_document(self):
        words = []
        for word in self.d1.words():
            words.append(word)
        self.assertEqual(len(words), 2)
        self.assertEqual(words[0], "stopword")
        self.assertEqual(words[1], "test")

def suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromTestCase(RegexpFilterTestCase))
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
