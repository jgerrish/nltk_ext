class Util(object):
    @staticmethod
    def jaccard(s1, s2):
        """Static method for Jaccard distance"""
        union = len(s1.union(s2))
        inter = len(s1.intersection(s2))
        if union == 0:
            return 0.0
        else:
            return float(inter) / float(union)
