import unittest
import math
from nltk_ext.documents.document import Document
from nltk_ext.corpus.corpus import ScikitLearnNotInstalledException, Corpus


class CorpusTestCase(unittest.TestCase):
    def setUp(self):
        self.d1 = Document({"id": "1", "body": "This this."})
        self.d2 = Document({"id": "2", "body": "This is another test document."})
        self.d3 = Document({"id": "3", "body": "Two words."})
        self.d4 = Document({"id": "4", "body": "Three words."})
        self.corpus = Corpus([self.d1, self.d2, self.d3])

    def test_df(self):
        self.assertEqual(self.corpus.df("this"), 2)
        self.assertEqual(self.corpus.df("is"), 1)
        self.assertEqual(self.corpus.df("two"), 1)
        self.assertEqual(self.corpus.df("."), 3)

    def test_idf(self):
        # assume math.log is good
        self.assertEqual(self.corpus.idf("this"), math.log(3.0 / 2.0))
        self.assertEqual(self.corpus.idf("is"), math.log(3.0 / 1.0))
        self.assertEqual(self.corpus.idf("."), math.log(3.0 / 3.0))

    def test_tf(self):
        self.assertEqual(self.corpus.tf("1", "this"), 2.0 / 3.0)
        self.assertEqual(self.corpus.tf("2", "this"), 1.0 / 6.0)
        self.assertEqual(self.corpus.tf("2", "is"), 1.0 / 6.0)
        self.assertEqual(self.corpus.tf("3", "."), 1.0 / 3.0)

    def test_tf_idf(self):
        self.assertEqual(
            self.corpus.tf_idf("1", "this"), (2.0 / 3.0) * math.log(3.0 / 2.0)
        )
        self.assertEqual(
            self.corpus.tf_idf("2", "this"), (1.0 / 6.0) * math.log(3.0 / 2.0)
        )
        self.assertEqual(
            self.corpus.tf_idf("2", "is"), (1.0 / 6.0) * math.log(3.0 / 1.0)
        )
        self.assertEqual(
            self.corpus.tf_idf("3", "."), (1.0 / 3.0) * math.log(3.0 / 3.0)
        )

    def test_vocabulary(self):
        v = self.corpus.vocabulary()
        self.assertEqual(v["."], 3)
        self.assertEqual(v["this"], 3)
        self.assertEqual(v["another"], 1)

    def test_generate_doc_lens(self):
        self.corpus.generate_doc_lens()
        result = {"1": 10, "2": 30, "3": 10}
        self.assertEqual(self.corpus.doc_lens, result)

    def test_generate_neighbor_list(self):
        corpus = Corpus([self.d1, self.d2, self.d3, self.d4])
        length = corpus.generate_neighbor_list(self.d1)
        self.assertTrue(
            ((length[0] == ("1", 0)) and (length[1] == ("3", 0)))
            or ((length[0] == ("3", 0)) and (length[1] == ("1", 0)))
        )
        self.assertEqual(length[2], ("4", 2))
        self.assertEqual(length[3], ("2", 20))

    def test_neighbors(self):
        corpus = Corpus([self.d1, self.d2, self.d3, self.d4])
        neighbors = corpus.neighbors(self.d1, 10)
        n = [doc.doc_id for doc in neighbors]
        self.assertEqual(set(["1", "3", "4"]), set(n))
        neighbors = corpus.neighbors(self.d1, 20)
        n = [doc.doc_id for doc in neighbors]
        self.assertEqual(set(["1", "2", "3", "4"]), set(n))
        neighbors = corpus.neighbors(self.d1, 0)
        n = [doc.doc_id for doc in neighbors]
        self.assertEqual(set(["1", "3"]), set(n))

    def test_to_scikit_learn_dataset(self):
        corpus = Corpus([self.d1, self.d2, self.d3, self.d4])

        import importlib.util

        package_name = "sklearn.utils"
        spec = importlib.util.find_spec(package_name)
        ex = False
        try:
            dataset = corpus.to_scikit_learn_dataset()
            # TODO Test dataset
            self.assertTrue(dataset is not None)
        except ScikitLearnNotInstalledException:
            ex = True
        self.assertEqual(ex, spec is None)


def suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromTestCase(CorpusTestCase))
    return suite


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite())
