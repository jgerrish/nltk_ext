import unittest
from nltk_ext.documents.document import Document
from nltk_ext.pipelines.redis_uniq import RedisUniq
from redis.exceptions import ConnectionError


class RedisUniqTestCase(unittest.TestCase):
    def setUp(self):
        self.d1 = Document({"id": "1", "body": "A test of a unique filter pipeline."})

    def test_document(self):
        words = []
        for word in self.d1.words():
            words.append(word)
        self.assertEqual(len(words), 8)
        self.assertEqual(words[1], "test")

    def test_redis_uniq(self):
        try:
            r = RedisUniq()
            words = list(r.process(self.d1.words()))
            self.assertEqual(len(words), 7)
            self.assertEqual(words[0], "a")
            self.assertEqual(words[1], "test")
            self.assertEqual(words[2], "of")
            self.assertEqual(words[3], "unique")
        except ConnectionError:
            # TODO Add mocks for the Redis code.
            # We could install redis-server on the runners, but even if
            # Github firewalls redis installs on runners, I don't want to
            # forget setting all that up if I ever run a custom CI
            # This gets most tests up and running for now
            pass


def suite():
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromTestCase(RedisUniqTestCase))
    return suite


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite())
