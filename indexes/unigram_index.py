from nltk_ext.indexes.index import Index


class UnigramIndex(Index):
    """
    Unigram model index class.  Terms are the unigrams in the document.
    """

    def terms(self):
        """
        Return the unigrams in the document, which is the same as
        what the default words method on Document returns
        """
        return self._document.words()
