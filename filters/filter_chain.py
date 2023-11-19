class FilterChain:
    def __init__(self, filters=[]):
        self.filters = filters

    def add(self, f):
        self.filters.append(f)

    def check(self, data):
        for f in self.filters:
            if not f.filter(data):
                return False
        return True
