"""
game.py

Assignment: Homework 2
Class: CS4395
Author: Aditya Rathod (NetID: AGR190000)
Date: 2023-02-18
"""

import random
from typing import List


class GuessingGame:
    def __init__(self, word_list: List[str]):
        """
        Initialize the game with a list of words to guess and 5 points.
        """

        print("Let's play a word guessing game!")
        self.word_list = word_list
        self.points = 5
        self._setup_game()

    def _setup_game(self):
        """
        Setup the game by choosing a random word from the list and resetting
        the letters guessed and last input.
        """

        self.letters_guessed = set([])
        self.word_to_guess = random.choice(self.word_list)
        self.last_input = ""

    def play(self):
        """
        Play the game until the user runs out of points or quits.
        """

        # check for exit condition
        while self.points >= 0 and self.last_input != "!":
            self._play_round()
            # check for win condition
            if set(self.word_to_guess) == self.letters_guessed:
                print("You solved it!\n")
                print(f"Current score: {self.points}\n")
                print("Guess another word")
                self._setup_game()
                self.play()
        # print feedback and exit
        if self.last_input == "!":
            print("You quit the game.")
            return
        print(f"Game over! You ended with a score of {self.points}.")

    def _play_round(self):
        """
        Play a single round of the game.
        Check if the letter is in the word and update the points accordingly.
        """

        # print the current state of the word
        print(
            " ".join(
                [c if c in self.letters_guessed else "_" for c in self.word_to_guess]
            )
        )
        self.last_input = input("Guess a letter: ").strip()

        # handle exit condition
        if self.last_input == "!":
            return

        # check if letter is in word, otherwise deduct points
        if self.last_input in self.word_to_guess:
            # check if letter has already been guessed
            if self.last_input in self.letters_guessed:
                print("You already guessed that letter!")
                return
            self.letters_guessed.add(self.last_input)
            self.points += 1
            print(f"Right! Score is {self.points}")
        else:
            self.points -= 1
            print(f"Sorry, guess again. Score is {self.points}")
