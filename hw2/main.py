"""
main.py

Assignment: Homework 2
Class: CS4395
Author: Aditya Rathod (NetID: AGR190000)
Date: 2023-02-18
"""

import argparse
from collections import Counter
from pathlib import Path
from typing import List, Tuple

from nltk import pos_tag
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

from game import GuessingGame

ALL_STOPWORDS = set(stopwords.words("english"))


def get_args() -> argparse.Namespace:
    """
    Get the command line arguments via argparse.
    """

    parser = argparse.ArgumentParser(prog="hw2", description="Homework 2 for CS4395")
    parser.add_argument("data_path")
    return parser.parse_args()


def preprocess_raw_text(raw_text: str) -> Tuple[List[str], List[str]]:
    """
    Preprocess the raw text data.
    """

    # tokenize the lowercased text
    token_conditions = (
        lambda t: (t not in ALL_STOPWORDS) and t.isalpha() and (len(t) > 5)
    )
    tokens = list(filter(token_conditions, word_tokenize(raw_text.lower())))

    # lemmatize the tokens and create a list of unique lemmas
    lemmatizer = WordNetLemmatizer()
    lemmas = [lemmatizer.lemmatize(t) for t in tokens]
    lemmas_unique = list(set(lemmas))

    # do pos tagging and print the first 20 tagged
    pos_tagged = pos_tag(lemmas_unique)
    print("First 20 tagged tokens:")
    for i, (token, tag) in enumerate(pos_tagged):
        print(f"\t{i + 1}. {token} ({tag})")
        if i >= 19:
            break

    # create a list of only those lemmas that are nouns
    nouns: List[str] = [t for t, tag in pos_tagged if tag.startswith("NN")]

    print(f"Number of tokens: {len(tokens)}, number of nouns: {len(nouns)}")
    return (tokens, nouns)


def main():
    """
    Main function. Reads the CSV file and prints the dictionary of Person objects.
    """

    # read the input file as raw text
    args = get_args()
    data_path = Path(args.data_path)
    with open(data_path, "r") as f:
        data = f.read().replace("\n", " ")
    # calculate the lexical diversity of the tokenized text and output it
    raw_tokens = word_tokenize(data)
    print(
        f"Lexical diversity (raw text): {(len(set(raw_tokens)) / len(raw_tokens)):.2f}"
    )
    tokens, nouns = preprocess_raw_text(data)
    # make a dictionary of the most common nouns and their counts
    counter = dict(Counter(filter(lambda t: t in nouns, tokens)))
    # print out the most common 50 nouns
    most_common_50_all = sorted(counter.items(), key=lambda x: x[1], reverse=True)[:50]
    print("Most 50 common nouns:")
    most_common_50_words: List[str] = []
    for i, (noun, count) in enumerate(most_common_50_all):
        print(f"\t{i + 1}. {noun} ({count})")
        most_common_50_words.append(noun)
    # play a guessing game lol
    game = GuessingGame(most_common_50_words)
    game.play()


if __name__ == "__main__":
    main()
