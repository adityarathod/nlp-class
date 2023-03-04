"""
ngrams.py

Assignment: Homework 4
Class: CS4395
Author: Aditya Rathod (NetID: AGR190000)
Date: 2023-03-04
"""

import logging
import pickle
import nltk

from pathlib import Path
from typing import Dict, List, Tuple, TypedDict
from nltk.util import ngrams

log = logging.getLogger("ngrams")

# Location to persist the ngram distributions
NGRAM_PERSISTENCE_DIR = Path(".") / Path("dists")


# Type aliases
Unigram = Tuple[str]
Bigram = Tuple[str, str]
UnigramDist = Dict[Unigram, int]
BigramDist = Dict[Bigram, int]


class AggregatedDist(TypedDict):
    lang: str
    unigrams: UnigramDist
    bigrams: BigramDist


def create_distributions(text: str) -> Tuple[UnigramDist, BigramDist]:
    """
    Create the unigram and bigram distributions for the given text.
    """
    tokens = nltk.word_tokenize(text)
    unigrams = ngrams(tokens, 1)
    unigrams_freq: UnigramDist = dict(nltk.FreqDist(unigrams))
    log.info(f"Number of unigrams: {len(unigrams_freq)}")
    bigrams = ngrams(tokens, 2)
    bigrams_freq: BigramDist = dict(nltk.FreqDist(bigrams))
    log.info(f"Number of bigrams: {len(bigrams_freq)}")
    return unigrams_freq, bigrams_freq


def compute_probability_single(
    text: str, dists: AggregatedDist, vocab_size: int
) -> float:
    """
    Compute the probability of the text being part of the langauge using Laplace smoothing.
    """
    unigrams = nltk.word_tokenize(text)
    bigrams = ngrams(unigrams, 2)
    p = 1

    # For every bigram, compute the probability of it being part of the language
    for bigram in bigrams:
        b = dists["bigrams"].get(bigram, 0)
        u = dists["unigrams"].get(bigram[0], 0)
        v = vocab_size
        p *= (b + 1) / (u + v)

    return p


def compute_probability_all(text: str, all_dists: List[AggregatedDist]):
    """
    Compute the probability of the text being part of each language using Laplace smoothing.
    """

    # Compute the vocabulary size
    vocab_size = sum([len(dists["unigrams"]) for dists in all_dists])

    # Partially apply the compute_probability_single function
    compute_probability_single_partial = lambda dists: compute_probability_single(
        text, dists, vocab_size
    )

    # Compute the probability for each language
    all_langs = [dists["lang"] for dists in all_dists]
    all_probs = list(map(compute_probability_single_partial, all_dists))

    # Sort the languages by probability, descending
    return list(sorted(zip(all_langs, all_probs), key=lambda x: x[1], reverse=True))


def persist(unigrams: UnigramDist, bigrams: BigramDist, lang: str):
    """
    Persist the unigram and bigram distributions to disk via pickle.
    """
    unigram_loc = NGRAM_PERSISTENCE_DIR / f"dist_{lang}_unigrams.pkl"
    bigram_loc = NGRAM_PERSISTENCE_DIR / f"dist_{lang}_bigrams.pkl"

    log.info(f"Persisting {lang} unigrams to {unigram_loc}")
    with open(unigram_loc, "wb") as f:
        pickle.dump(unigrams, f)

    log.info(f"Persisting {lang} bigrams to {bigram_loc}")
    with open(bigram_loc, "wb") as f:
        pickle.dump(bigrams, f)


def load(
    unigram_path: Path | str, bigram_path: Path | str
) -> Tuple[UnigramDist, BigramDist]:
    """
    Load the unigram and bigram distributions from disk via pickle.
    """
    log.info(f"Loading unigrams from {unigram_path}")
    with open(unigram_path, "rb") as f:
        unigrams = pickle.load(f)

    log.info(f"Loading bigrams from {bigram_path}")
    with open(bigram_path, "rb") as f:
        bigrams = pickle.load(f)
    return unigrams, bigrams
