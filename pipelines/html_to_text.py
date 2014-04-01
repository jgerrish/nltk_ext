# HTML to text module for converting HTML documents to text
from bs4 import BeautifulSoup

class HtmlToTextPipeline(object):
    def __init__(self):
        self.parser = "lxml"
        return

    def clean(self):
        [s.extract() for s in self.soup('script')]

    def process(self, source, data):
        self.soup = BeautifulSoup(data, self.parser)
        self.clean()
        return self.soup.get_text()#.encode('ascii', 'ignore')
