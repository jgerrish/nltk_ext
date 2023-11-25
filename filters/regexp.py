# A regular expression filter to filter out data
#
# Filter out words based on a given regular expression
# For example, using "^.$" would filter out single character words
import re
from nltk_ext.filters.filter import Filter


class RegexpFilter(Filter):
    def __init__(self, regex):
        if regex:
            self.regex = re.compile(regex)

    def filter(self, elements):
        for elem in elements:
            if self.regex.match(elem) is None:
                yield elem
