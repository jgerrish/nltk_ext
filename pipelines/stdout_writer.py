import pprint


class StdoutWriter(object):
    """
    Pipeline module to print out items
    """

    def __init__(self, formatter=None):
        if formatter:
            self.formatter = formatter
        else:
            self.pp = pprint.PrettyPrinter(indent=4)
            self.formatter = self.pp_formatter

    def pp_formatter(self, data):
        return self.pp.pformat(data)

    def process(self, source, data=None):
        for s in source:
            print("data")
            print(str(s))  # self.formatter(s)
            yield self.formatter(s)
