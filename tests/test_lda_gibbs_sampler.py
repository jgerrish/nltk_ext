import pytest

from nltk_ext.algorithms.lda_gibbs_sampler import LDAGibbsSampler
from nltk_ext.corpus.corpus import Corpus
from nltk_ext.documents.document import Document


@pytest.fixture
def lda_corpus() -> Corpus:
    d1 = Document(
        {"id": "1", "body": "Birds fly and play."},
    )
    d2 = Document(
        {"id": "2", "body": "Dogs bark and play."},
    )
    d3 = Document(
        {"id": "3", "body": "Trees bud and respire."},
    )
    corpus = Corpus([d1, d2, d3])

    return corpus


def test_ldagibbssampler_init(lda_corpus: Corpus) -> None:
    lda = LDAGibbsSampler(lda_corpus)
    assert type(lda) == LDAGibbsSampler
    assert len(lda.documents) == 3


def test_term_index(lda_corpus: Corpus) -> None:
    lda = LDAGibbsSampler(lda_corpus)
    # Number of terms should be eight
    # "play" should be counted as one term
    # stopword "and" should be removed
    # punctuation "." should be removed
    assert lda.term_index.num_terms == 8
    words = ["dogs", "bark", "bud", "trees", "birds", "play", "fly", "respire"]
    for term in words:
        assert term in lda.term_index.terms

    assert "." not in lda.term_index.terms


def test_initialize(lda_corpus: Corpus) -> None:
    lda = LDAGibbsSampler(lda_corpus)
    assert type(lda) == LDAGibbsSampler
    assert len(lda.documents) == 3

    # 10 topics because it's the default initializer value
    assert lda.thetasum == {
        "1": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "2": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        "3": [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    }
