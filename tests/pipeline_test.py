import unittest
from nltk_ext.documents.document import Document
from nltk_ext.corpus.corpus import Corpus
from nltk_ext.pipelines.generator_pipeline import GeneratorPipeline
from nltk_ext.filters.stopword import StopwordFilter
from nltk_ext.pipelines.uniq import Uniq
from nltk_ext.pipelines.recorder import Recorder

class PipelineTestCase(unittest.TestCase):
    """
    Test a simple pipeline with several pipeline modules
    """
    def setUp(self):
        self.d1 = Document({"id": "1", "body": "A stopword test."})
        self.d2 = Document({"id": "2", "body": "A stopword test and a unique test."})
        self.corpus = Corpus([self.d1, self.d2])

    def test_pipeline(self):
        recorder = Recorder([])
        pipeline = GeneratorPipeline([Uniq(), recorder, StopwordFilter()])
        words = pipeline.process(self.d2.words())
        word_list = list(words)
        self.assertEqual(len(word_list), 4)
        self.assertEqual(word_list[0], "stopword")
        self.assertEqual(word_list[1], "test")
        self.assertEqual(word_list[2], "unique")
        self.assertEqual(word_list[3], ".")

        word_list = recorder.get_data()
        #print word_list
        self.assertEqual(len(word_list), 6)
        self.assertEqual(word_list[0], "a")
        self.assertEqual(word_list[1], "stopword")
        self.assertEqual(word_list[2], "test")
        self.assertEqual(word_list[3], "and")
        self.assertEqual(word_list[4], "unique")
        self.assertEqual(word_list[5], ".")

def suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromTestCase(PipelineTestCase))
    return suite

if __name__ == '__main__':
    unittest.TextTestRunner(verbosity=2).run(suite())
