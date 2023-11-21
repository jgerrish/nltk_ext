import glob
from nltk_ext.corpus.corpus import Corpus
from nltk_ext.documents.document import Document
from progressbar import Percentage, ProgressBar, Bar, ETA


class FileCorpusLoader:
    def __init__(self, max_cnt=200000000):
        self.documents = Corpus()
        self.max_cnt = max_cnt

    def process(self, data, fields=None):
        if fields is not None:
            d = {}
            for field in fields:
                if field in data:
                    d[field] = data[field]
        else:
            d = data.copy()
        doc = Document(d)
        self.documents.add(doc)

        return self.documents

    def load(
        self,
        directory,
        fields=None,
        progress_bar=True,
    ):
        files = glob.glob(directory + "/*.txt")

        num_docs = len(files)
        # num_docs = self.reader.collection.count()
        # count = 0
        if progress_bar:
            progress_bar_tmpl = [
                "Loading: ",
                Percentage(),
                " ",
                Bar(marker="#", left="[", right="]"),
                " ",
                ETA(),
            ]
            pbar = ProgressBar(
                widgets=progress_bar_tmpl, maxval=min(num_docs, self.max_cnt + 1)
            )
            pbar.start()

        for f in files:
            # self.reader = FileReader(f)
            with open(f, "r") as content_file:
                content = content_file.read()
                d = Document(
                    {
                        "id": f,
                        "body_text": content,
                    }
                )
                self.documents.add(d)

        if progress_bar:
            pbar.finish()

        return self.documents
