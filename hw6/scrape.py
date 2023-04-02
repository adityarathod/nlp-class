import logging
from pathlib import Path
from typing import List, Tuple

log = logging.getLogger("scrape")

import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from readabilipy import simple_json_from_html_string

RELEVANT_TERMS = {"lol", "league"}


def get_page(url: str) -> str:
    """
    Get the HTML content of a page.
    """
    log.debug(f"Getting page: {url}")
    response = requests.get(url)
    return response.text


def get_relevant_links(
    page: str, base_url: str, relevant_terms=RELEVANT_TERMS
) -> List[str]:
    """
    Get all the relevant links from a page.
    """
    soup = BeautifulSoup(page, "html.parser")
    try:
        all_links = soup.html.find_all("a")
    except:
        log.error(f"Page may be malformed: {base_url}")
        return []
    has_real_link = lambda link: link.has_attr("href") and not link["href"].startswith(
        "#"
    )
    clean_links = {link["href"] for link in filter(has_real_link, all_links)}
    log.debug(f"Found {len(clean_links)} links.")
    if len(clean_links) == 0:
        log.error(f"No links found on page: {base_url}")
        log.debug(f"Page content: {page}")
    resolved_links = {urljoin(base_url, path) for path in clean_links}
    relevant_links = {
        link for link in resolved_links if any(term in link for term in relevant_terms)
    }
    log.debug(f"Found {len(relevant_links)} relevant links.")
    return list(relevant_links)


def scrape_page(url: str, save_folder: Path) -> Tuple[str, List[str]]:
    """
    Scrape a page and return all the relevant links.
    """
    log.info(f"Scraping: {url}")
    try:
        page = get_page(url)
    except:
        log.error(f"Could not get page: {url}")
        return "", []
    clean_url = url.replace("/", "_")
    if len(clean_url) > 100:
        clean_url = clean_url[:100]
    save_path = save_folder / Path(clean_url + ".txt")
    try:
        parsed_article = simple_json_from_html_string(page)
        plain_text = "\n\n".join(
            [chunk["text"] for chunk in parsed_article["plain_text"]]
        )
    except:
        plain_text = page
    relevant_links = get_relevant_links(page, url)
    if len(plain_text) > 0:
        log.debug(f"Saving page to: {save_path}")
        with open(save_path, "w") as f:
            f.write(plain_text)
    else:
        log.warning(f"Page is empty: {url}. Skipping save.")
    return page, relevant_links
