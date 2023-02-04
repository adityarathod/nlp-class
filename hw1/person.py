"""
person.py

Assignment: Homework 1
Class: CS4395
Author: Aditya Rathod (NetID: AGR190000)
Date: 2023-02-04
"""

import re
from textwrap import dedent

# matches two letters followed by 4 digits
ID_REGEX = re.compile("^\w{2}\d{4}$")
# matches 3 digits, then 3 digits, then 4 digits with optional separators
PHONE_REGEX = re.compile("^(\d{3})[\s|.|-]*(\d{3})[\s|.|-]*(\d{4})$")


class Person:
    # name fields
    last: str
    first: str
    mi: str

    # id and phone fields
    id: str
    phone: str

    def __init__(self, last: str, first: str, mi: str, id: str, phone: str) -> None:
        """
        Initialize a person from an explicit set of fields.
        """
        self.last = last
        self.first = first
        self.mi = mi
        self.id = id
        self.phone = phone
        self.clean_up()

    def __init__(self, info_dict: dict) -> None:
        """
        Initialize a person from a dictionary of parsed information.
        """
        self.last = info_dict["Last"]
        self.first = info_dict["First"]
        self.mi = info_dict["Middle Initial"]
        self.id = info_dict["ID"]
        self.phone = info_dict["Office phone"]
        self.clean_up()

    def ask_for_correct_id(self):
        """
        Ask the user for a correct ID.
        """
        print(f"ID invalid: {self.id}")
        print("ID is two letters followed by 4 digits")
        raw_id = input("Please enter a valid ID: ").strip()
        self.id = raw_id
        if not ID_REGEX.match(self.id):
            self.ask_for_correct_id()

    def ask_for_correct_phone(self):
        """
        Ask the user for a correct phone number.
        """
        print(f"Phone {self.phone} is invalid")
        print("Enter phone number in form 123-456-7890")
        raw_phone = input("Enter phone number: ").strip()
        self.phone = raw_phone
        if not PHONE_REGEX.match(raw_phone):
            self.ask_for_correct_phone()

    def clean_up(self) -> None:
        """
        Clean up the person's information based on rules set in the assignment.
        """
        # capitalize first and last name
        self.last = self.last.capitalize()
        self.first = self.first.capitalize()
        # capitalize middle initial if it exists, or substitute with X
        if self.mi:
            self.mi = self.mi.upper()
        else:
            self.mi = "X"
        # check if ID is valid
        if not ID_REGEX.match(self.id):
            self.ask_for_correct_id()
        # check if phone number is valid
        phone_match = PHONE_REGEX.match(self.phone)
        if not phone_match:
            self.ask_for_correct_phone()
            phone_match = PHONE_REGEX.match(self.phone)
        # format phone number
        self.phone = (
            f"{phone_match.group(1)}-{phone_match.group(2)}-{phone_match.group(3)}"
        )

    def display(self) -> None:
        """
        Display the person's information to stdout.
        """
        print(str(self))

    def __repr__(self) -> str:
        """
        Return a string representation of the person.
        """
        return str(self)

    def __str__(self) -> str:
        """
        Return a string representation of the person.
        """
        line1 = f"Employee id: {self.id}"
        line2 = f"{self.first} {self.mi} {self.last}"
        line3 = f"{self.phone}"
        return f"""{line1}\n\t{line2}\n\t{line3}\n"""
