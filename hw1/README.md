# Homework 1: Python Basics

## Program Description
The program parses a CSV of employees with the following columns in the CSV:

- Last (name)
- First (name)
- Middle Initial
- (Employee) ID
- Office phone

It then checks each entry for formatting and prompts the user to fix any issues if they are detected.

## Running the Program

`python3 main.py <path_to_data_file>`

## Strengths and Weaknesses of Python for Text Processing
### Strengths
Python has a rich standard library with built-in packages to do everything from parsing CSV files automatically to resolving paths in an OS-agnostic way. And for any functionality not built-in to Python, there is a rich ecosystem of packages that can probably handle your usecase (see spaCy and NLTK).

### Weaknesses
A lot of Python packages that are performance-focused actually end up offloading a lot of work to extensions written in C that can be called from Python. That means that in general, you're largely limited to the functionality of those libraries with C extensions if performance is important to you.

## Takeaways
I got to review the Python standard library and the language's approach to types.