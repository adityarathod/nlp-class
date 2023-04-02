from collections import Counter

from nltk import word_tokenize


def get_term_frequencies(text: str) -> Counter:
    """
    Get the term frequencies of a text.
    """
    return Counter(word_tokenize(text))


def merge_term_frequencies(*term_frequencies: Counter) -> Counter:
    """
    Merge multiple term frequencies into one.
    """
    return Counter(sum(term_frequencies, Counter()))
