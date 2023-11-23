from nltk_ext.filters.custom_filter import CustomFilter


class PunctuationFilter(CustomFilter):
    """
    Filter punctuation from a document.

    This filter class removes punctuation from a document.  The
    default implementation uses isalnum to filter out punctuation.

    isalpha was recommended for punctuation removal in the NLTK book
    Chapter 1 Section 6.

    But isalpha filters out certain words that may need to be indexed.
    Is 69 a valid word? 911? 21?  Before using this class these are
    questions to ask.
    """

    def __init__(self, func=None):
        """
        Initialize the PunctucationFilter with an appropriate string
        function.

        isalpha was recommended for punctuation removal is shown in the NLTK
        book Chapter 1 Section 6.

        Is 69 a topic? 911? 21?  Before using this class these are
        questions to ask.

        If isalpha is used, topics around 911 may be removed.  For
        now, the default uses isalnum.  For academic articles, this
        may increase topic noise.
        """
        self.func = None
        if func is None:
            self.func = lambda w: w.isalnum()
        else:
            self.func = func
        return super().__init__(self.func)
