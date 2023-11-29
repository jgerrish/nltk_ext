# LDA Gibbs Sampler
# Based on code from the Java implementation by Gregor Heinrich

from dataclasses import dataclass, field, InitVar
import json
import operator
import random

# dictionary with increment or set operation
from collections import defaultdict
from typing import Any, Dict, List, Set, Union

from progressbar import Percentage, ProgressBar, Bar, ETA

from nltk_ext.corpus.corpus import Corpus
from nltk_ext.documents.document import Document
from nltk_ext.filters.punctuation import PunctuationFilter
from nltk_ext.filters.stopword import StopwordFilter


burn_in_bar_tmpl = [
    "Burn In: ",
    Percentage(),
    " ",
    Bar(marker="#", left="[", right="]"),
    " ",
    ETA(),
]

sample_bar_tmpl = [
    "Sample: ",
    Percentage(),
    " ",
    Bar(marker="#", left="[", right="]"),
    " ",
    ETA(),
]


@dataclass
class TermIndex:
    """
    An index of terms in the corpus.
    """

    terms: Set[str] = field(default_factory=set, init=False)
    "A set of the unique terms in the index"

    term_list: List[str] = field(default_factory=list, init=False)
    "A list of the unique terms in the index"

    num_terms: int = field(init=False)
    "The number of terms in the index"

    term_index: Dict[str, int] = field(default_factory=dict, init=False)
    """
    An index of terms from the term string to an index into the
    term_list
    """

    documents: InitVar[Corpus | None] = None
    "The Corpus to initialize this index with"

    def __post_init__(self, documents: Corpus) -> None:
        "Build the term index"
        self.terms = set()
        if documents is not None:
            for document in documents:
                for word in document.words():
                    self.terms.add(word)
        self.term_list = list(self.terms)
        self.num_terms = len(self.term_list)
        self.term_index = {}
        for i, term in enumerate(self.term_list):
            self.term_index[term] = i


@dataclass
class TopicIndex:
    document_topic_count: Dict[str, Dict[Union[int, str], int]] = field(
        default_factory=dict, init=False
    )
    "number of words in a document assigned to a topic"

    topic_term_count: Dict[Any, Any] = field(
        default_factory=lambda: defaultdict(int), init=False
    )
    "number of terms assigned to each topic"

    document_topic_sum: Dict[Any, Any] = field(
        default_factory=lambda: defaultdict(int), init=False
    )
    "sum of topics for each document"

    topic_term_sum: Dict[Any, Any] = field(
        default_factory=lambda: defaultdict(int), init=False
    )

    doc_word_topic: Dict[str, List[int]] = field(default_factory=dict, init=False)

    documents: InitVar[Corpus | None] = None
    "The Corpus to initialize this index with"

    def __post_init__(self, documents: Corpus) -> None:
        for document in documents:
            self.document_topic_count[document.doc_id] = defaultdict(int)


@dataclass
class BetaModelParameters:
    alpha: float = 2.0
    beta: float = 0.5


@dataclass
class TrainingParameters:
    num_iterations: int = 1000
    burn_in_len: int = 100
    sample_lag: int = 10


@dataclass
class LDAGibbsSampler:
    documents: Corpus = field(default_factory=lambda: Corpus())
    num_topics: int = 10
    model_parameters: BetaModelParameters = field(
        default_factory=lambda: BetaModelParameters(), init=False
    )
    training_parameters: TrainingParameters = field(
        default_factory=lambda: TrainingParameters(), init=False
    )

    def __post_init__(self) -> None:
        # First, add a stopword and punctation filter to each document
        # if they're not already added.
        self.add_filters()

        self.topic_index = TopicIndex(self.documents)
        self.term_index = TermIndex(self.documents)

        self.initialize()

    def add_filters(self) -> None:
        """
        Add a stopword and punctation filter to each document if they're
        not already added.
        """
        stopword_filter = StopwordFilter()
        punctuation_filter = PunctuationFilter()
        for doc in self.documents:
            stopword_filter_found = False
            punctuation_filter_found = False
            for f in doc.word_filters:
                # Search for a general stopword filter
                # This won't catch all custom stopword filters
                if type(f) == StopwordFilter:
                    stopword_filter_found = True
                # Search for a general punctuation filter
                # This won't catch all custom punctuation filters
                if type(f) == PunctuationFilter:
                    punctuation_filter_found = True
            if not stopword_filter_found:
                doc.word_filters.append(stopword_filter)
            if not punctuation_filter_found:
                doc.word_filters.append(punctuation_filter)

    def inc_counts(self, document: Document, word: str, word_idx: int) -> None:
        t_i = self.term_index.term_index[word]
        k = random.randint(0, self.num_topics - 1)
        if document.doc_id not in self.topic_index.doc_word_topic:
            self.topic_index.doc_word_topic[document.doc_id] = []
        self.topic_index.doc_word_topic[document.doc_id][word_idx] = k

        self.topic_index.document_topic_count[document.doc_id][k] += 1
        self.topic_index.document_topic_sum[document.doc_id] += 1
        if k not in self.topic_index.topic_term_count:
            self.topic_index.topic_term_count[k] = defaultdict(int)
        self.topic_index.topic_term_count[k][t_i] += 1
        self.topic_index.topic_term_sum[k] += 1

    def dec_counts(self, document: Document, word: str, word_idx: int) -> None:
        t_i = self.term_index.term_index[word]
        k = self.topic_index.doc_word_topic[document.doc_id][word_idx]
        self.topic_index.document_topic_count[document.doc_id][k] -= 1
        self.topic_index.document_topic_sum[document.doc_id] -= 1
        # TODO Review logic here
        if k not in self.topic_index.topic_term_count:
            self.topic_index.topic_term_count[k] = defaultdict(int)
        else:
            self.topic_index.topic_term_count[k][t_i] -= 1
        self.topic_index.topic_term_sum[k] -= 1

    def sample(self, document: Document, word: str, word_idx: int) -> int:
        m = [None] * self.num_topics
        t_i = self.term_index.term_index[word]
        k = self.topic_index.doc_word_topic[document.doc_id][word_idx]
        for i in range(self.num_topics):
            denom = self.topic_index.topic_term_sum[k]
            +len(self.term_index.term_list) * self.model_parameters.beta
            if denom == 0:
                t1 = float("NaN")
            else:
                t1 = (
                    self.topic_index.topic_term_count[k][t_i]
                    + self.model_parameters.beta
                ) / denom
            denom = (
                self.topic_index.document_topic_sum[document.doc_id]
                + self.num_topics * self.model_parameters.alpha
            )
            if denom == 0:
                t2 = float("NaN")
            else:
                t2 = (
                    self.topic_index.document_topic_count[document.doc_id][k]
                    + self.model_parameters.alpha
                ) / denom
            m[i] = t1 * t2  # type: ignore[call-overload]

        for i in range(self.num_topics - 1):
            m[i + 1] += m[i]  # type: ignore[operator]

        u = random.randint(0, self.num_topics - 1)
        for k in range(self.num_topics):
            if u < m[k]:
                break

        return k

    def initialize(self) -> None:
        self.thetasum = {}
        self.phisum = []
        for document in self.documents:
            self.thetasum[document.doc_id] = [0] * self.num_topics
            self.topic_index.doc_word_topic[document.doc_id] = [None] * len(
                document.words()
            )
            for idx, word in enumerate(document.words()):
                self.inc_counts(document, word, idx)

        for k in range(self.num_topics):
            self.phisum.append([0] * self.term_index.num_terms)

        self.num_stats = 0

    def update_progress_bar(self, i: int) -> None:
        if i < self.training_parameters.burn_in_len:
            if i == 0:
                self.burn_in_pbar.start()
            self.burn_in_pbar.update(i)
        else:
            if i == self.training_parameters.burn_in_len:
                self.burn_in_pbar.finish()
                self.sample_pbar.start()
            self.sample_pbar.update(i - self.training_parameters.burn_in_len)
            if i == self.training_parameters.num_iterations:
                self.sample_pbar.finish()

    def update_params(self) -> None:
        for document in self.documents:
            for k in range(self.num_topics):
                self.thetasum[document.doc_id][k] += (
                    self.topic_index.document_topic_count[document.doc_id][k]
                    + self.model_parameters.alpha
                ) / (
                    self.topic_index.document_topic_sum[document.doc_id]
                    + self.num_topics * self.model_parameters.alpha
                )

        for k in range(self.num_topics):
            # TODO Review logic here
            denom = (
                self.topic_index.topic_term_sum[k]
                + self.term_index.num_terms * self.model_parameters.beta
            )
            if denom != 0.0:
                for w in range(self.term_index.num_terms):
                    self.phisum[k][w] += (
                        self.topic_index.topic_term_count[k][w]
                        + self.model_parameters.beta
                    ) / denom

        self.num_stats += 1

    def get_theta(self) -> Dict[Any, List[Any]]:
        theta: Dict[Any, List[Any]] = {}
        for document in self.documents:
            theta[document.doc_id] = []
            for k in range(self.num_topics):
                a = self.thetasum[document.doc_id][k]
                theta[document.doc_id].append(a / self.num_stats)

        return theta

    def get_phi(self) -> Dict[Any, List[Any]]:
        phi: Dict[Any, List[Any]] = {}
        for k in range(self.num_topics):
            phi[k] = []
            for w in range(self.term_index.num_terms):
                phi[k].append(self.phisum[k][w] / self.num_stats)

        return phi

    # TODO Add a test for the below
    def print_stats(self) -> None:
        theta = self.get_theta()
        phi = self.get_phi()

        tw: Dict[Any, Any] = {}
        # TODO Add a test for the below
        print("topic - words:")
        topic_words = []

        for k in range(self.num_topics):
            print("Topic: {} ".format(str(k)))
            tw[k] = {}
            for w in range(self.term_index.num_terms):
                tw[k][self.term_index.term_list[w]] = phi[k][w]
            # TODO Review logic here
            # topic_words = sorted(tw[k].iteritems(), key=operator.itemgetter(1))
            topic_words = sorted(tw[k].items(), key=operator.itemgetter(1))
            topic_words.reverse()
            for t in topic_words[0:10]:
                print("  {}: {}".format(str(t[0]), str(t[1])))

        print("document - topics:")
        s = []
        for document in self.documents:
            print("document {}: ".format(str(document.doc_id)))
            d = theta[document.doc_id]
            topic_scores = dict(zip(range(self.num_topics), d))
            # s = sorted(topic_scores.iteritems(), key=operator.itemgetter(1))  # type: ignore[attr-defined]
            s = sorted(topic_scores.items(), key=operator.itemgetter(1))
            s.reverse()
            for t in s:
                print("Topic {}: {}".format(str(t[0]), str(t[1])))

        g = {"topic_words": tw, "document_topics": theta}
        f = open("topics.json", "w")
        f.write(json.dumps(g, sort_keys=True, indent=4, separators=(",", ": ")))
        f.close()

    def sampler(self, progress_bar: bool = True) -> None:
        if progress_bar:
            self.burn_in_pbar = ProgressBar(
                widgets=burn_in_bar_tmpl, maxval=self.training_parameters.burn_in_len
            )
            self.sample_pbar = ProgressBar(
                widgets=sample_bar_tmpl,
                maxval=self.training_parameters.num_iterations
                - self.training_parameters.burn_in_len,
            )

        for i in range(self.training_parameters.num_iterations):
            for document in self.documents:
                for idx, word in enumerate(document.words()):
                    self.dec_counts(document, word, idx)
                    # Sample
                    k = self.sample(document, word, idx)
                    # Update the topic
                    self.topic_index.doc_word_topic[document.doc_id][idx] = k

            if progress_bar:
                self.update_progress_bar(i)
            if (
                (i > self.training_parameters.burn_in_len)
                and (self.training_parameters.sample_lag > 0)
                and ((i % self.training_parameters.sample_lag) == 0)
            ):
                self.update_params()

        self.print_stats()
