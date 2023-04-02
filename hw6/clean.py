import logging
import re
from pathlib import Path
from typing import List

log = logging.getLogger("clean")

from nltk.corpus import stopwords
from nltk.tokenize import sent_tokenize, word_tokenize


def all_parseable_files(folder: Path) -> List[Path]:
    """
    Get all the parseable files in a folder.
    """
    return list(folder.glob("*"))


def open_file(path: Path) -> str:
    """
    Open a file and return its contents.
    """
    with open(path, "r") as f:
        return f.read()


def clean_file(file: Path, parse_output_path: Path) -> str:
    """
    Clean a file and save it to the parse output path.
    """
    all_text = open_file(file)
    all_text = all_text.replace("\n\n", " ").replace("\t", " ")
    # Parse the text into sentences.
    sentences = sent_tokenize(all_text)
    # Remove stop words, punctuation, and short sentences.
    stop_words = set(stopwords.words("english"))
    stop_words.update(".,!?;:()[]{}|.`*<>")
    # sentences = [sentence for sentence in sentences if len(sentence) > 5]
    for sentence in sentences:
        words = word_tokenize(sentence)
        words = [
            word.lower() for word in words if word not in stop_words and word.isalnum()
        ]
        # print(words)
        sentence = " ".join(words)
        sentence = re.sub(r"[^\w\s]", "", sentence)

    clean_text = " ".join(sentences).lower()
    output_path = parse_output_path / Path(file.stem + ".txt")
    log.info(f"Writing to {output_path}")
    with open(output_path, "w") as f:
        f.write(clean_text)
    return clean_text
