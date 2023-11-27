import unittest
from nltk_ext.documents.document import Document
from nltk_ext.util import Util


class UtilTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.d1 = Document({"id": "1", "body": "first test document"})
        self.d2 = Document({"id": "2", "body": "second test document"})
        self.d3 = Document({"id": "3", "body": "short document"})
        self.d4 = Document({"id": "4", "body": "fourth test document"})
        self.docs = [self.d1, self.d2, self.d3, self.d4]

    def test_jaccard(self) -> None:
        s1 = set(["a", "b", "c"])
        s2 = set(["a", "b"])
        r = Util.jaccard(s1, s2)
        self.assertEqual(r, 2.0 / 3.0)
        s1 = set(["a", "b", "c"])
        s2 = set(["a", "b", "c"])
        r = Util.jaccard(s1, s2)
        self.assertEqual(r, 1.0)
        s1 = set(["d", "e", "f"])
        s2 = set(["a", "b", "c"])
        r = Util.jaccard(s1, s2)
        self.assertEqual(r, 0.0)
        s1 = set(["a", "b", "f"])
        s2 = set(["a", "b", "c"])
        r = Util.jaccard(s1, s2)
        self.assertEqual(r, 0.5)


def suite() -> unittest.suite.TestSuite:
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromTestCase(UtilTestCase))
    return suite


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite())
