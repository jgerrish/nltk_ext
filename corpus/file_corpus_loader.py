import json
import pprint
from nltk_ext.corpus import Corpus
from nltk_ext.document import Document
from progressbar import Percentage, ProgressBar, Bar, ETA


class FileCorpusLoader:
    def __init__(self, max_cnt=200000000):
        self.documents = Corpus()
        self.max_cnt = max_cnt

    def process(self, data, fields=None):
        if fields != None:
            d = {}
            for field in fields:
                if field in data:
                    d[field] = data[field]
        else:
            d = data.copy()
        doc = Document(d)
        self.documents.add(doc)

        return self.documents

    def load(self, dbname="spout_test", collection="good_documents", fields=None,
             progress_bar=True):
        self.reader = MongoDBReader(dbname, collection)

        num_docs = self.reader.collection.count()
        count = 0
        if progress_bar:
            progress_bar_tmpl = ['Loading: ', Percentage(), ' ',
                                 Bar(marker='#', left='[', right=']'), ' ', ETA()]
            pbar = ProgressBar(widgets=progress_bar_tmpl,
                               maxval=min(num_docs, self.max_cnt + 1))
            pbar.start()
        i = 0

        files = glob.glob(d + "/*.txt")
        for f in files:
            with open(f, 'r') as content_file:
                content = content_file.read()
                d = Document({
                    'id': f,
                    'body_text': content,
                })
                documents.add(d)

        if progress_bar:
            pbar.finish()

        return self.documents
