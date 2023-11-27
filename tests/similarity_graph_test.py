import unittest
from nltk_ext.documents.document import Document
from nltk_ext.pipelines.similarity_graph import SimilarityGraph


class SimilarityGraphTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.d1 = Document({"id": "1", "body": "This this."})
        self.d2 = Document({"id": "2", "body": "This is another test document."})
        self.d3 = Document({"id": "3", "body": "Two words."})
        self.d4 = Document({"id": "4", "body": "Three words."})

    def test_process(self) -> None:
        sim = SimilarityGraph(lambda x: x < 3)
        data = [self.d1, self.d2, self.d3, self.d4]
        sim.process(data)
        # self.assertEqual(len(add_to_corpus_module.corpus), 4)


def suite() -> unittest.suite.TestSuite:
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromTestCase(SimilarityGraphTestCase))
    return suite


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite())
