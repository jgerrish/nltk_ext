import unittest
from nltk_ext.corpus.corpus import Corpus
from nltk_ext.documents.document import Document
from nltk_ext.pipelines.generator_pipeline import GeneratorPipeline
from nltk_ext.pipelines.category_to_corpus import CategoryToCorpus


class CategoryToCorpusTestCase(unittest.TestCase):
    """
    Test a simple pipeline with several pipeline modules
    """

    def setUp(self) -> None:
        self.d1 = Document({"id": "1", "body": "A stopword test."})
        self.d1.set("categories", ["stopwords"])
        self.d2 = Document({"id": "2", "body": "A stopword test and a unique test."})
        self.d2.set("categories", ["stopwords"])
        self.d3 = Document({"id": "3", "body": "A parsing test."})
        self.d3.set("categories", ["parsing"])
        self.docs = [self.d1, self.d2, self.d3]

    def test_category_to_corpus_combined(self) -> None:
        # Test combined mode, which concatenates documents in the same category
        # into a single document
        category_to_corpus = CategoryToCorpus()
        pipeline = GeneratorPipeline([category_to_corpus])
        docs = pipeline.process(self.docs)
        # TODO: add a sink module or something similar to thread all docs/words
        # through a pipeline
        for doc in docs:
            continue
        # Get the generated corpus
        corpus = category_to_corpus.post_process()
        if isinstance(corpus, Corpus):
            self.assertEqual(len(corpus.categories()), 2)
        else:
            self.fail("category_to_corpus.post_process Should return Corpus")
        stopwords_docs = corpus["stopwords"]
        parsing_docs = corpus["parsing"]

        if isinstance(stopwords_docs, Document):
            word_list = list(stopwords_docs.words())
            self.assertEqual(len(word_list), 12)
            self.assertEqual(word_list[0], "a")
            self.assertEqual(word_list[1], "stopword")
            self.assertEqual(word_list[2], "test")
            self.assertEqual(word_list[3], ".")
            self.assertEqual(word_list[4], "a")
            self.assertEqual(word_list[5], "stopword")
            self.assertEqual(word_list[6], "test")
            self.assertEqual(word_list[7], "and")
            self.assertEqual(word_list[8], "a")
            self.assertEqual(word_list[9], "unique")
            self.assertEqual(word_list[10], "test")
            self.assertEqual(word_list[11], ".")
        else:
            self.fail("Corpus getitem should return Document")

        if isinstance(parsing_docs, Document):
            word_list = list(parsing_docs.words())
            self.assertEqual(len(word_list), 4)
            self.assertEqual(word_list[0], "a")
            self.assertEqual(word_list[1], "parsing")
            self.assertEqual(word_list[2], "test")
            self.assertEqual(word_list[3], ".")
        else:
            self.fail("Corpus getitem should return Document")

    def test_category_to_corpus_combined_two(self) -> None:
        """
        Test combined mode, which concatenates documents in the same category
        into a single document
        """
        category_to_corpus = CategoryToCorpus()
        pipeline = GeneratorPipeline([category_to_corpus])
        docs = pipeline.process(self.docs)
        # TODO: add a sink module or something similar to thread all docs/words
        # through a pipeline
        for doc in docs:
            continue
        # Get the generated corpus
        corpus = category_to_corpus.post_process()
        if isinstance(corpus, Corpus):
            self.assertEqual(len(corpus.categories()), 2)
        else:
            self.fail("category_to_corpus.post_process Should return Corpus")
        stopwords_docs = corpus["stopwords"]
        parsing_docs = corpus["parsing"]

        word_list = list(stopwords_docs.words())
        if isinstance(stopwords_docs, Document):
            self.assertEqual(len(word_list), 12)
            self.assertEqual(word_list[0], "a")
            self.assertEqual(word_list[1], "stopword")
            self.assertEqual(word_list[2], "test")
            self.assertEqual(word_list[3], ".")
            self.assertEqual(word_list[4], "a")
            self.assertEqual(word_list[5], "stopword")
            self.assertEqual(word_list[6], "test")
            self.assertEqual(word_list[7], "and")
            self.assertEqual(word_list[8], "a")
            self.assertEqual(word_list[9], "unique")
            self.assertEqual(word_list[10], "test")
            self.assertEqual(word_list[11], ".")
        else:
            self.fail("Corpus getitem should return Document")

        word_list = list(parsing_docs.words())
        if isinstance(parsing_docs, Document):
            self.assertEqual(len(word_list), 4)
            self.assertEqual(word_list[0], "a")
            self.assertEqual(word_list[1], "parsing")
            self.assertEqual(word_list[2], "test")
            self.assertEqual(word_list[3], ".")
        else:
            self.fail("Corpus getitem should return Document")

    def test_category_to_corpus_separated(self) -> None:
        """
        Test separated mode, which puts documents in the same category
        into different corpora.
        """
        category_to_corpus = CategoryToCorpus(
            None, None, "categories", None, "separated"
        )
        pipeline = GeneratorPipeline([category_to_corpus])
        docs = pipeline.process(self.docs)
        # TODO: add a sink module or something similar to thread all docs/words
        # through a pipeline
        for doc in docs:
            continue
        # Get the generated corpus
        corpora = category_to_corpus.post_process()
        self.assertEqual(len(corpora), 2)
        self.assertEqual(len(corpora["stopwords"]), 2)
        self.assertEqual(len(corpora["parsing"]), 1)


def suite() -> unittest.suite.TestSuite:
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromTestCase(CategoryToCorpusTestCase))
    return suite


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite())
