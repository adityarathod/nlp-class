"""
main.py

Assignment: Homework 1
Class: CS4395
Author: Aditya Rathod (NetID: AGR190000)
Date: 2023-02-04
"""

import argparse
import csv
import pickle
from pathlib import Path
from typing import Dict

from person import *


def get_args() -> argparse.Namespace:
    """
    Get the command line arguments via argparse.
    """
    parser = argparse.ArgumentParser(prog="hw1", description="Homework 1 for CS4395")
    parser.add_argument("data_path")
    return parser.parse_args()


def read_csv(path: Path) -> Dict[str, Person]:
    """
    Read a CSV file and return a dictionary of Person objects.
    Throws a ValueError if there are duplicate IDs.
    """
    with open(path, "r", encoding="utf-8-sig") as data_file:
        all_people = {}
        # read every line in the CSV file (besides the header)
        for line in csv.DictReader(data_file):
            person = Person(line)
            # if the ID is already in the dictionary, throw an error
            if person.id in all_people:
                raise ValueError(f"Duplicate ID: {person.id}")
            all_people[person.id] = person
        return all_people


def create_pickle(data: Dict[str, Person], path: Path = Path("./data/people.pkl")):
    """
    Create a pickle file from a dictionary of Person objects.
    """
    with open(path, "wb") as pickle_file:
        pickle.dump(data, pickle_file)


def open_pickle(path: Path = Path("./data/people.pkl")) -> Dict[str, Person]:
    """
    Open a pickle file and return a dictionary of Person objects.
    """
    with open(path, "rb") as pickle_file:
        return pickle.load(pickle_file)


def main():
    """
    Main function. Reads the CSV file and prints the dictionary of Person objects.
    """
    # parse args, read data
    args = get_args()
    data_path = Path(args.data_path)
    all_people = read_csv(data_path)

    # pickling and unpickling demo
    create_pickle(all_people)
    all_people_unpickled = open_pickle()

    # display all employees
    print("\nEmployee list:\n")
    for person in all_people_unpickled.values():
        person.display()


if __name__ == "__main__":
    main()
