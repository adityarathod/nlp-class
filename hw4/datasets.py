"""
datasets.py

Assignment: Homework 4
Class: CS4395
Author: Aditya Rathod (NetID: AGR190000)
Date: 2023-03-04
"""

import re
from pathlib import Path
from typing import List, Tuple

import ngrams

TRAINING_DATA_FILENAME_REGEX = re.compile(r"^.*LangId.train.(.+)$")
DIST_FILENAME_REGEX = re.compile(r"^.*dist_(.+)_(.*)\.pkl$")


def read_text(filename: str | Path) -> str:
    """
    Read the text from the given file.
    """
    with open(filename, "r") as f:
        return f.read()


def determine_train_file_lang(filename: str | Path) -> str:
    """
    Determine the language of the training file based on the filename.
    """
    results = re.findall(TRAINING_DATA_FILENAME_REGEX, str(filename))
    if len(results) == 0:
        raise ValueError(f"Invalid filename: {filename}")
    else:
        return results[0]


def read_test_files(
    test_data_path: str | Path, test_labels_path: str | Path
) -> List[Tuple[str, str]]:
    """
    Open the test data and labels files and return a list of tuples.
    Each tuple contains the test data and the label, in that order.
    """
    with open(test_data_path, "r") as f:
        test_data = f.readlines()
    with open(test_labels_path, "r") as f:
        test_labels = f.readlines()
    test_labels_clean = map(lambda x: x.split(" ")[1], test_labels)
    strip = lambda x: x.strip()
    return list(zip(map(strip, test_data), map(strip, test_labels_clean)))


def read_dists_folder(folder_path: str | Path) -> List[ngrams.AggregatedDist]:
    """
    Read the ngram distribution files from the given folder using the ngrams module.
    """
    dist_locations = {}
    path = Path(folder_path) if isinstance(folder_path, str) else folder_path

    # Iterate over the files in the folder and determine the language and distribution type
    for file in path.iterdir():
        results = re.findall(DIST_FILENAME_REGEX, str(file))
        if len(results) == 0:
            raise ValueError(f"Invalid filename: {file}")
        else:
            lang, dist_type = results[0]
            if lang not in dist_locations:
                dist_locations[lang] = {}
            dist_locations[lang][dist_type] = file

    # Load the unigrams and bigrams for each language based on the files we found
    all_dists = []
    for lang in dist_locations:
        if (
            "unigrams" not in dist_locations[lang]
            or "bigrams" not in dist_locations[lang]
        ):
            raise ValueError(f"Missing unigrams or bigrams for language: {lang}")
        unigrams, bigrams = ngrams.load(
            dist_locations[lang]["unigrams"], dist_locations[lang]["bigrams"]
        )
        all_dists.append({"lang": lang, "unigrams": unigrams, "bigrams": bigrams})
    return all_dists
