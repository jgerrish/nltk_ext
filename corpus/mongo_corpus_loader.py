from progressbar import Percentage, ProgressBar, Bar, ETA
from typing import List, Optional

from nltk_ext.corpus.corpus import Corpus
from nltk_ext.documents.document import Document
from nltk_ext.readers.mongodb import MongoDBReader


class MongoCorpusLoader:
    def __init__(self, max_cnt: int = 200000000) -> None:
        self.documents = Corpus()
        self.max_cnt = max_cnt

    def process(self, data: Document, fields: Optional[List[str]] = None) -> Corpus:
        if fields is not None:
            d = {}
            for field in fields:
                if field in data:
                    d[field] = data[field]
            doc = Document(d)
        else:
            # TODO Double check this change, add a test
            doc = data
        self.documents.add(doc)

        return self.documents

    def load(
        self,
        dbname: str = "db_name",
        collection: str = "collection_name",
        fields: Optional[List[str]] = None,
        progress_bar: bool = True,
    ) -> Corpus:
        self.reader = MongoDBReader(dbname, collection)

        num_docs = self.reader.collection.count()
        count = 0
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
        i = 0
        for data in self.reader:
            if i > self.max_cnt:
                break
            i += 1
            if data is not None:
                self.process(data, fields)
                count += 1
                if progress_bar:
                    pbar.update(count)

        if progress_bar:
            pbar.finish()

        return self.documents
