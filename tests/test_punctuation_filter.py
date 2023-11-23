import pytest
from nltk_ext.documents.document import Document
from nltk_ext.filters.punctuation import PunctuationFilter


@pytest.fixture()
def setup_default():
    "Create documents with the default non-alphanumeric punctuation filter"
    punctuation_filter = PunctuationFilter()
    d1 = Document(
        {"id": "1", "body": "First document."},
        [punctuation_filter],
    )
    d2 = Document(
        {"id": "2", "body": "Document 2."},
        [punctuation_filter],
    )
    d3 = Document(
        {"id": "3", "body": "3rd Document."},
        [punctuation_filter],
    )
    d4 = Document(
        {"id": "4", "body": "num4 Document."},
        [punctuation_filter],
    )

    return [d1, d2, d3, d4]


@pytest.fixture()
def setup_alpha():
    "Create documents with an non-alphabetic punctuation filter"
    punctuation_filter = PunctuationFilter(lambda x: x.isalpha())
    d1 = Document(
        {"id": "1", "body": "First document."},
        [punctuation_filter],
    )
    d2 = Document(
        {"id": "2", "body": "Document 2."},
        [punctuation_filter],
    )
    d3 = Document(
        {"id": "3", "body": "3rd Document."},
        [punctuation_filter],
    )
    d4 = Document(
        {"id": "4", "body": "num4 Document."},
        [punctuation_filter],
    )

    return [d1, d2, d3, d4]


def test_words_default_period(setup_default):
    "Test that a period is removed with the default filter"
    docs = setup_default
    words = []
    for word in docs[0].words():
        words.append(word)
    assert len(words) == 2
    assert words[0] == "first"
    assert words[1] == "document"


def test_words_default_number(setup_default):
    "Test that 2 is not removed with an alphanumeric filter"
    docs = setup_default
    words = []
    for word in docs[1].words():
        words.append(word)
    assert len(words) == 2
    assert words[0] == "document"
    assert words[1] == "2"


def test_words_default_number_alpha(setup_default):
    "Test that 3rd is not removed with an alphanumeric filter"
    docs = setup_default
    words = []
    for word in docs[2].words():
        words.append(word)
    assert len(words) == 2
    assert words[0] == "3rd"
    assert words[1] == "document"


def test_words_default_alpha_number(setup_default):
    "Test that num4 is not removed with an alphanumeric filter"
    docs = setup_default
    words = []
    for word in docs[3].words():
        words.append(word)
    assert len(words) == 2
    assert words[0] == "num4"
    assert words[1] == "document"


def test_words_alpha_period(setup_alpha):
    "Test that a period is removed with an alphabetic filter"
    docs = setup_alpha
    words = []
    for word in docs[0].words():
        words.append(word)
    assert len(words) == 2
    assert words[0] == "first"
    assert words[1] == "document"


def test_words_alpha_number(setup_alpha):
    "Test that 2 is removed with an alphabetic filter"
    docs = setup_alpha
    words = []
    for word in docs[1].words():
        words.append(word)
    assert len(words) == 1
    assert words[0] == "document"


def test_words_alpha_number_alpha(setup_alpha):
    "Test that 3rd is removed with an alphabetic filter"
    docs = setup_alpha
    words = []
    for word in docs[2].words():
        words.append(word)
    assert len(words) == 1
    assert words[0] == "document"


def test_words_alpha_alpha_number(setup_alpha):
    "Test that num4 is removed with an alphabetic filter"
    docs = setup_alpha
    words = []
    for word in docs[3].words():
        words.append(word)
    assert len(words) == 1
    assert words[0] == "document"
