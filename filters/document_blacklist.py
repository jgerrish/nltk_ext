# A Document blacklist filter to filter out documents
#
# Filters out documents based on a regular expression blacklist
# if the given attribute matches one of the regular expressions, the
# document is rejected
# attribute and one of the blacklist parameters are required arguments
import re

class DocumentBlacklist(object):
    def __init__(self, attribute=None,
                 blacklist=None, blacklist_fn="blacklist.txt"):
        bl = []
        if (blacklist_fn != None) and (blacklist == None):
            with open(blacklist_fn, "r") as f:
                bl = f.read().split('\n')
                # convert list to a set
        elif blacklist != None:
            bl = blacklist
        self.blacklist = set(bl)
        self.attribute = attribute
        self.init_regexes(bl)

    def init_regexes(self, blacklist):
        """
        Right now, use a simple list of regexes and check in sequence
        Use more efficient methods later
        """
        self.regex_blacklist = []
        for bl in blacklist:
            if bl != "":
                self.regex_blacklist.append(re.compile(bl))

    def filter(self, documents):
        for document in documents:
            match = False
            if self.attribute in document:
                for bl in self.regex_blacklist:
                    #print "checking " + document[self.attribute] + " against " + str(bl)
                    if bl.match(document[self.attribute]) != None:
                        match = True
            if not match:
                yield document

    def process(self, documents):
        return self.filter(documents)
