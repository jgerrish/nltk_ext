import unittest
from nltk_ext.documents.html_document import HTMLDocument


class HTMLDocumentTestCase(unittest.TestCase):
    def setUp(self) -> None:
        self.d1 = HTMLDocument(
            {"id": "1", "body_text": "This this.", "title": "test document 1"}
        )
        self.d2 = HTMLDocument(
            {
                "id": "2",
                "body_text": "This is another test document.",
                "title": "test document 2",
            }
        )
        self.d3 = HTMLDocument(
            {"id": "3", "body_text": "Two words.", "title": "test document 3"}
        )
        self.d4 = HTMLDocument({"id": "3", "body_text": "Derp a derp.\nA derp derp."})

    def test_html_document_init(self) -> None:
        d1 = HTMLDocument({"id": "1", "body_text": "This this."})
        self.assertEqual(d1.doc_id, "1")
        self.assertEqual(str(d1), "This this.")
        d2 = HTMLDocument("This that.")
        self.assertEqual(str(d2), "This that.")

    def test_html_document_title(self) -> None:
        # title attributes here are defined with the set method on
        # Document
        self.assertEqual(self.d1.title, "test document 1")  # type: ignore[attr-defined]
        self.assertEqual(self.d2.title, "test document 2")  # type: ignore[attr-defined]
        self.assertEqual(self.d3.title, "test document 3")  # type: ignore[attr-defined]
        self.assertRaises(AttributeError, lambda: self.d4.title)  # type: ignore[attr-defined]


def suite() -> unittest.suite.TestSuite:
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    suite.addTest(loader.loadTestsFromTestCase(HTMLDocumentTestCase))
    return suite


if __name__ == "__main__":
    unittest.TextTestRunner(verbosity=2).run(suite())
