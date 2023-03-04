"""
prog2.py

Assignment: Homework 4
Class: CS4395
Author: Aditya Rathod (NetID: AGR190000)
Date: 2023-03-04
"""

import argparse
import csv
import logging
from pathlib import Path
from typing import List, Tuple

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("prog2")

import ngrams
from datasets import read_dists_folder, read_test_files


def get_args() -> argparse.Namespace:
    """
    Get the command line arguments via argparse.
    """

    parser = argparse.ArgumentParser(
        prog="hw4_prog2", description="Homework 4 for CS4395"
    )
    parser.add_argument(
        "-d",
        "--dist-dir",
        help="The directory to load the ngram distributions from.",
        required=True,
    )
    parser.add_argument(
        "-t",
        "--test-file",
        help="The location of the test data file.",
        required=True,
    )
    parser.add_argument(
        "-l",
        "--test-labels",
        help="The location of the test data labels file.",
        required=True,
    )
    parser.add_argument(
        "-r",
        "--result-path",
        help="The location where to save the results to.",
        default="LangId.prediction_results.csv",
    )
    return parser.parse_args()


def validate_args(args: argparse.Namespace):
    """
    Validate the command line arguments.
    """
    dist_dir = Path(args.dist_dir).resolve()
    if not dist_dir.exists():
        raise ValueError(f"Directory {dist_dir} does not exist.")
    if not dist_dir.is_dir():
        raise ValueError(f"Path {dist_dir} is not a directory.")
    test_file = Path(args.test_file).resolve()
    if not test_file.exists():
        raise ValueError(f"File {test_file} does not exist.")
    if not test_file.is_file():
        raise ValueError(f"Path {test_file} is not a file.")
    test_labels = Path(args.test_labels).resolve()
    if not test_labels.exists():
        raise ValueError(f"File {test_labels} does not exist.")
    if not test_labels.is_file():
        raise ValueError(f"Path {test_labels} is not a file.")
    result_path = Path(args.result_path).resolve()
    if not result_path.parent.exists():
        raise ValueError(f"Directory {result_path.parent} does not exist.")
    if not result_path.parent.is_dir():
        raise ValueError(f"Path {result_path.parent} is not a directory.")

    return {
        "dist_dir": dist_dir,
        "test_file": test_file,
        "test_labels": test_labels,
        "result_path": result_path,
    }


def run_test_single(test_case: Tuple[str, str], all_dists: List[ngrams.AggregatedDist]):
    """
    Run a single test case and return the predicted language,
    the probability of the prediction, and whether the prediction was correct.
    """
    sentence, label = test_case
    # Truncate the sentence if it's too long for the log.
    truncated_sentence = (sentence[:50] + "...") if len(sentence) > 50 else sentence
    # log.info(f'Running test case "{truncated_sentence}" with label "{label}"')
    # Compute the probability of the sentence being of each language. Use only the top result.
    predictions = ngrams.compute_probability_all(sentence, all_dists)
    predicted_lang, predicted_prob = predictions[0]
    is_correct = predicted_lang == label
    if not is_correct:
        log.info(f'Running test case "{truncated_sentence}" with label "{label}"')
        log.info(
            f'[Incorrect] Sentence is predicted to be of language "{predicted_lang}" with probability {predicted_prob}'
        )
    return (predicted_lang, predicted_prob, is_correct)


def write_test_results(
    test_results: List[Tuple[str, float, bool]], file_name: str | Path
):
    """
    Write the test results to a CSV file.
    """
    with open(file_name, "w") as f:
        writer = csv.writer(f)
        writer.writerow(["PredictedLabel", "Probability", "Correct"])
        for result in test_results:
            writer.writerow(list(map(str, result)))


def main():
    args = validate_args(get_args())
    all_dists = read_dists_folder(args["dist_dir"])
    tests = read_test_files(args["test_file"], args["test_labels"])
    # Run the test cases.
    test_results = [run_test_single(test_case, all_dists) for test_case in tests]
    # Compute the number of correct and incorrect test cases.
    correct_test_cases = sum(map(lambda test: test[2], test_results))
    total_test_cases = len(tests)
    incorrect_test_cases = [
        i + 1 for i in range(len(test_results)) if not test_results[i][2]
    ]
    log.info(
        f"Correctly predicted {correct_test_cases} out of {total_test_cases} test cases. ({correct_test_cases / total_test_cases * 100:.2f}%)"
    )
    log.info(
        f"Incorrectly predicted test cases: {' '.join(map(str, incorrect_test_cases))}"
    )
    write_test_results(test_results, args["result_path"])


if __name__ == "__main__":
    main()
