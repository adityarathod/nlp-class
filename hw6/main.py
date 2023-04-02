import argparse
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO)
log = logging.getLogger("prog1")

from scrape import scrape_page
from clean import all_parseable_files, clean_file
from stats import get_term_frequencies, merge_term_frequencies
from util import is_url


def get_args() -> argparse.Namespace:
    """
    Get the command line arguments via argparse.
    """

    parser = argparse.ArgumentParser(prog="hw6", description="Homework 6 for CS4395")
    parser.add_argument(
        "--scrape-folder",
        help="The folder to output scraped webpages to.",
        default="./scraped",
    )
    parser.add_argument(
        "--parse-folder",
        help="The folder to output parsed webpages to.",
        default="./parsed",
    )
    parser.add_argument(
        "--base-url",
        help="The base URL to start scraping from.",
        default="https://en.wikipedia.org/wiki/League_of_Legends",
    )
    parser.add_argument(
        "--scrape-only", action="store_true", help="Only scrape pages.", default=False
    )
    parser.add_argument(
        "--parse-only", action="store_true", help="Only parse pages.", default=False
    )
    return parser.parse_args()


def validate_args(args: argparse.Namespace) -> None:
    """
    Validate the command line arguments.
    """
    scrape_folder = Path(args.scrape_folder)
    scrape_folder_exists = scrape_folder.exists()
    # Create the scrape folder if it doesn't exist.
    if not scrape_folder_exists:
        log.info(f"Creating scrape output folder: {scrape_folder}")
        scrape_folder.mkdir(parents=True)
    elif not scrape_folder.is_dir():
        log.error(f"Output folder is not a directory: {scrape_folder}")
        raise ValueError(f"Output folder is not a directory: {scrape_folder}")
    parse_folder = Path(args.parse_folder)
    parse_folder_exists = parse_folder.exists()
    # Create the parse folder if it doesn't exist.
    if not parse_folder_exists:
        log.info(f"Creating parse output folder: {parse_folder}")
        parse_folder.mkdir(parents=True)
    elif not parse_folder.is_dir():
        log.error(f"Parse folder is not a directory: {parse_folder}")
        raise ValueError(f"Parse folder is not a directory: {parse_folder}")
    # Validate the base URL.
    base_url = args.base_url
    if not is_url(base_url):
        log.error(f"Invalid base URL: {base_url}")
        raise ValueError(f"Invalid base URL: {base_url}")
    # Validate the scrape-only and parse-only flags.
    scrape_only = args.scrape_only
    parse_only = args.parse_only
    if scrape_only and parse_only:
        log.error("Cannot specify both --scrape-only and --parse-only.")
        raise ValueError("Cannot specify both --scrape-only and --parse-only.")
    if not scrape_folder_exists and parse_only:
        log.error("Cannot specify --parse-only when output folder doesn't exist.")
        raise ValueError(
            "Cannot specify --parse-only when output folder doesn't exist."
        )
    return {
        "scrape_folder": scrape_folder,
        "parse_folder": parse_folder,
        "base_url": base_url,
        "scrape_only": scrape_only,
        "parse_only": parse_only,
    }


def execute_scrape(output_folder: Path, base_url: str):
    """
    Execute the scraping process.
    """
    log.info(f"Scrape output folder is {output_folder}")
    log.info(f"Base URL is {base_url}")
    all_links = {base_url}
    scraped_links = set([])
    num_scraped = 0
    # Scrape 300 pages starting from the base URL.
    while num_scraped < 300 or len(all_links) > 0:
        cur_link = all_links.pop()
        if cur_link in scraped_links:
            continue
        _, extracted_links = scrape_page(cur_link, output_folder)
        log.info(f"Found {len(extracted_links)} relevant links.")
        for link in extracted_links:
            if link not in scraped_links:
                all_links.add(link)
        scraped_links.add(cur_link)
        num_scraped += 1
        log.info(f"Scraped {num_scraped+1} pages.")


def execute_parse(scrape_folder: Path, parse_folder: Path):
    """
    Execute the parsing process.
    """
    log.info(f"Parse output folder is {parse_folder}")
    log.info(f"Scrape folder is {scrape_folder}")
    all_files = all_parseable_files(scrape_folder)
    all_term_freqs = get_term_frequencies("")
    for file in all_files:
        log.info(f"Parsing {file}")
        clean_text = clean_file(file, parse_folder)
        all_term_freqs = merge_term_frequencies(
            all_term_freqs, get_term_frequencies(clean_text)
        )
    print(all_term_freqs.most_common(200))


def main():
    args = validate_args(get_args())
    scrape_folder = args["scrape_folder"]
    parse_folder = args["parse_folder"]
    base_url = args["base_url"]
    scrape_only = args["scrape_only"]
    parse_only = args["parse_only"]
    do_both = not scrape_only and not parse_only
    if scrape_only or do_both:
        execute_scrape(scrape_folder, base_url)
    if parse_only or do_both:
        execute_parse(scrape_folder, parse_folder)
    # links = scrape_page(base_url, output_folder)


if __name__ == "__main__":
    main()
