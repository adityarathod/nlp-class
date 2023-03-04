"""
prog1.py

Assignment: Homework 4
Class: CS4395
Author: Aditya Rathod (NetID: AGR190000)
Date: 2023-03-04
"""

import argparse
import logging

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("prog1")

import ngrams
from datasets import read_text, determine_train_file_lang


def get_args() -> argparse.Namespace:
    """
    Get the command line arguments via argparse.
    """

    parser = argparse.ArgumentParser(
        prog="hw4_prog1", description="Homework 4 for CS4395"
    )
    parser.add_argument(
        "-f",
        "--file",
        action="append",
        help="The text file(s) to read from.",
        required=True,
    )
    return parser.parse_args()


def main():
    args = get_args()
    files = args.file
    log.info("hi")
    # Generate unigram and bigram distributions for each file and persist them.
    for file in files:
        log.info(f"Generating unigram and bigram distributions for file {file}")
        text = read_text(file)
        lang = determine_train_file_lang(file)
        log.info(f"Training file is of language {lang}")
        unigrams, bigrams = ngrams.create_distributions(text)
        ngrams.persist(unigrams, bigrams, lang)


if __name__ == "__main__":
    main()
