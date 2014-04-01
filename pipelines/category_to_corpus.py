# category_to_corpus converts a set of documents tagged with categories
# to a set of corpora, with each corpus corresponding to a single tag/category
import pprint
from nltk_ext.graph import Graph
from nltk_ext.documents.document import Document
from nltk_ext.corpus.corpus import Corpus
from nltk_ext.pipelines.pipeline_module import enumModuleType, enumModuleProcessingType, PipelineModule

class CategoryToCorpus(PipelineModule):
    def __init__(self, output=None, corpus=None,
                 attribute="categories",
                 categories=None, mode="combined"):
        """
        Create a CategoryToCorpus module, which loads a corpus with tagged
        documents.
        If corpus is passed in, it adds to an existing corpus.
        mode is the corpus loading method to use.  If set to "combined", all
        documents in a category are concatenated to a single document.
        Otherwise each document is loaded separately.
        """
        self.output = output
        self.corpora = {}
        # combined mode has a single corpus
        if corpus == None:
            self.corpus = Corpus()
        else:
            self.corpus = corpus
        self.module_type = enumModuleType(enumModuleType.Document)
        self.module_processing_type = \
            enumModuleProcessingType(enumModuleProcessingType.PostProcess)
        self.attribute = attribute
        self.categories = categories
        self.mode = mode
        self.pp = pprint.PrettyPrinter(indent=4)

    def add_document(self, category, document):
        if self.mode != "combined":
            if category in self.corpora:
                self.corpora[category].append(document)
            else:
                self.corpora[category] = [document]
        else:
            if category in self.corpus:
                d = self.corpus[category]
                d.update_text(unicode(d) + " " + unicode(document))
            else:
                document.set_doc_id(category)
                self.corpus.add(document)

    def process(self, data):
        """
        Process the documents.  The code looks at the attribute
        attribute, which should be a list or dictionary,
        and builds a set of corpora from categories in that
        attribute.
        If category is set, it only builds a single corpus containing
        documents with that category.
        """
        for doc in data:
            if self.attribute in doc.document:
                d = doc.document[self.attribute]
                if type(d) is list:
                    if self.categories == None:
                        for v in d:
                            self.add_document(v, doc)
                    else:
                        for category in self.categories:
                            if category in d:
                                self.add_document(category, doc)
            yield doc

    def post_process(self):
        """
        method that gets run after all data has been processed
        TODO: look into optimizing this, seems inefficient, written in derp-mode
        """
        if self.mode != "combined":
            return self.corpora
        else:
            return self.corpus

    def as_json(self):
        if self.mode != "combined":
            c = self.corpora
        else:
            c = self.corpus
        json.dumps(c, sort_keys=True, indent=4, separators=(',', ': '))

    def write(self):
        if self.output != None:
            f = open(self.output, 'w')
            f.write(self.as_json())
            f.close()

    def top_categories(self, n=10):
        for doc_id in self.categories:
            print str(doc_id)
            rt = self.corpus.ranked_terms(doc_id, n)
            print "  " + str(rt)
