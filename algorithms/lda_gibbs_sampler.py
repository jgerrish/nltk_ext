# LDA Gibbs Sampler
# Based on code from the Java implementation by Gregor Heinrich

import copy, json, operator, random, sets
# dictionary with increment or set operation
from collections import defaultdict
from progressbar import Percentage, ProgressBar, Bar, ETA
from nltk_ext.documents.document import Document
from nltk_ext.corpus import Corpus

burn_in_bar_tmpl = ['Burn In: ', Percentage(), ' ',
                    Bar(marker='#', left='[', right=']'), ' ', ETA()]

sample_bar_tmpl = ['Sample: ', Percentage(), ' ',
                   Bar(marker='#', left='[', right=']'), ' ', ETA()]

class LDAGibbsSampler:
    def __init__(self, documents, num_topics=10, alpha=2.0, beta=0.5,
                 num_iterations=1000, burn_in_len=100, thin_interval=100,
                 sample_lag=10):
        self.documents = documents
        # number of words in a document assigned to a topic
        self.document_topic_count = {}
        # number of terms assigned to each topic
        self.topic_term_count = defaultdict(int)
        self.document_topic_sum = {}
        # total number of words assigned to a topic
        self.topic_term_sum = defaultdict(int)
        self.document_topic_sum = defaultdict(int)
        self.doc_word_topic = {}
        self.num_topics = num_topics

        self.alpha = alpha
        self.beta = beta

        self.num_iterations = num_iterations
        self.burn_in_len = burn_in_len
        self.thin_interval = thin_interval
        self.sample_lag = sample_lag

        self.build_term_index()
        self.initialize()

    def build_term_index(self):
        # Build term index
        self.terms = sets.Set()
        for document in self.documents:
            self.document_topic_count[document.doc_id] = defaultdict(int)
            for word in document.words():
                self.terms.add(word)
        self.term_list = list(self.terms)
        self.num_terms = len(self.term_list)
        self.term_index = {}
        for i, term in enumerate(self.term_list):
            self.term_index[term] = i

    def inc_counts(self, document, word, word_idx):
        t_i = self.term_index[word]
        k = random.randint(0, self.num_topics - 1)
        if document.doc_id not in self.doc_word_topic:
            self.doc_word_topic[document.doc_id] = []
        self.doc_word_topic[document.doc_id][word_idx] = k

        self.document_topic_count[document.doc_id][k] += 1
        self.document_topic_sum[document.doc_id] += 1
        if k not in self.topic_term_count:
            self.topic_term_count[k] = defaultdict(int)
        self.topic_term_count[k][t_i] += 1
        self.topic_term_sum[k] += 1

    def dec_counts(self, document, word, word_idx):
        t_i = self.term_index[word]
        k = self.doc_word_topic[document.doc_id][word_idx]
        self.document_topic_count[document.doc_id][k] -= 1
        self.document_topic_sum[document.doc_id] -= 1
        self.topic_term_count[k][t_i] -= 1
        self.topic_term_sum[k] -= 1

    def sample(self, document, word, word_idx):
        m = [None]*self.num_topics
        t_i = self.term_index[word]
        k = self.doc_word_topic[document.doc_id][word_idx]
        for i in range(self.num_topics):
            denom = (self.topic_term_sum[k] + len(self.term_list) * self.beta)
            if denom == 0:
                t1 = float('NaN')
            else:
                t1 = (self.topic_term_count[k][t_i] + self.beta) / denom
            denom = self.document_topic_sum[document.doc_id] + \
                    self.num_topics * self.alpha
            if denom == 0:
                t2 = float('NaN')
            else:
                t2 = (self.document_topic_count[document.doc_id][k] + self.alpha) / \
                     denom
            m[i] = t1 * t2

        for i in range(self.num_topics - 1):
            m[i + 1] += m[i]

        u = random.randint(0, self.num_topics - 1)
        for k in range(self.num_topics):
            if (u < m[k]):
                break

        return k

    def initialize(self):
        self.thetasum = {}
        self.phisum = []
        for document in self.documents:
            self.thetasum[document.doc_id] = [0] * self.num_topics
            self.doc_word_topic[document.doc_id] = [None] * len(document.words())
            for idx, word in enumerate(document.words()):
                self.inc_counts(document, word, idx)

        for k in range(self.num_topics):
            self.phisum.append([0] * self.num_terms)

        self.num_stats = 0


    def update_progress_bar(self, i):
        if i < self.burn_in_len:
            if i == 0:
                self.burn_in_pbar.start()
            self.burn_in_pbar.update(i)
        else:
            if i == self.burn_in_len:
               self.burn_in_pbar.finish()
               self.sample_pbar.start()
            self.sample_pbar.update(i - self.burn_in_len)
            if i == self.num_iterations:
                self.sample_pbar.finish()

    def update_params(self):
        for document in self.documents:
            for k in range(self.num_topics):
                self.thetasum[document.doc_id][k] += \
                    (self.document_topic_count[document.doc_id][k] + self.alpha) / \
                    (self.document_topic_sum[document.doc_id] + self.num_topics * self.alpha)

        for k in range(self.num_topics):
            for w in range(self.num_terms):
                self.phisum[k][w] += (self.topic_term_count[k][w] + self.beta) / \
                                     (self.topic_term_sum[k] + self.num_terms * self.beta)
        self.num_stats += 1

    def get_theta(self):
        theta = {}
        for document in self.documents:
            theta[document.doc_id] = []
            for k in range(self.num_topics):
                a = self.thetasum[document.doc_id][k]
                theta[document.doc_id].append(a / self.num_stats)

        return theta

    def get_phi(self):
        phi = {}
        for k in range(self.num_topics):
            phi[k] = []
            for w in range(self.num_terms):
                phi[k].append(self.phisum[k][w] / self.num_stats)

        return phi

    def print_stats(self):
        theta = self.get_theta()
        phi = self.get_phi()

        tw = {}
        print "topic - words:"
        topic_words = []

        for k in range(self.num_topics):
            print "Topic " + str(k)
            tw[k] = {}
            for w in range(self.num_terms):
                tw[k][self.term_list[w]] = phi[k][w]
            topic_words = sorted(tw[k].iteritems(), key=operator.itemgetter(1))
            topic_words.reverse()
            for t in topic_words[0:10]:
                print "  " + str(t[0]) + ": " + str(t[1])

        print "document - topics:"
        s = []
        for document in self.documents:
            print "document " + str(document.doc_id) + ": "
            d = theta[document.doc_id]
            topic_scores = dict(zip(range(self.num_topics), d))
            s = sorted(topic_scores.iteritems(), key=operator.itemgetter(1))
            s.reverse()
            for t in s:
                print "Topic " + str(t[0]) + ": "+ str(t[1])

        g = { "topic_words": tw, "document_topics": theta }
        f = open('topics.json', 'w')
        f.write(json.dumps(g, sort_keys=True, indent=4, separators=(',', ': ')))
        f.close()


    def sampler(self, progress_bar=True):
        if progress_bar:
            self.burn_in_pbar = ProgressBar(widgets=burn_in_bar_tmpl,
                                            maxval=self.burn_in_len)
            self.sample_pbar = ProgressBar(widgets=sample_bar_tmpl,
                                           maxval=self.num_iterations - self.burn_in_len)

        for i in range(self.num_iterations):
            for document in self.documents:
                for idx, word in enumerate(document.words()):
                    self.dec_counts(document, word, idx)
                    # Sample
                    k = self.sample(document, word, idx)
                    # Update the topic
                    self.doc_word_topic[document.doc_id][idx] = k

            if progress_bar:
                self.update_progress_bar(i)
            if (i > self.burn_in_len) and \
               (self.sample_lag > 0) and ((i % self.sample_lag) == 0):
                self.update_params()

        self.print_stats()
