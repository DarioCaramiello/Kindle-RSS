from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

import yaml


def load_config(config_path: str) -> dict:
    """
    Load the YAML configuration file.

    Args:
        config_path: Path to the YAML configuration file.

    Returns:
        Parsed configuration as a dictionary.

    Raises:
        FileNotFoundError: If the configuration file does not exist.
        ValueError: If the configuration file is empty or invalid.
    """

    path = Path(config_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Configuration file not found: {path}"
        )

    with path.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    if not config:
        raise ValueError(
            f"Configuration file is empty: {path}"
        )

    if "newspaper" not in config:
        raise ValueError(
            "Missing 'newspaper' section in configuration."
        )

    if "feeds" not in config:
        raise ValueError(
            "Missing 'feeds' section in configuration."
        )

    return config

def normalize_url(url: str) -> str:
    """
    Normalize an URL for duplicate detection.

    Query parameters and fragments are removed.

    Args:
        url: Original URL.

    Returns:
        Normalized URL.
    """

    if not url:
        return ""

    parts = urlsplit(url)

    normalized = urlunsplit(
        (
            parts.scheme.lower(),
            parts.netloc.lower(),
            parts.path.rstrip("/"),
            "",
            "",
        )
    )

    return normalized


def remove_duplicates(
    articles: list[dict],
) -> list[dict]:
    """
    Remove duplicate articles using their normalized URL.

    Args:
        articles: List of article dictionaries.

    Returns:
        List containing unique articles only.
    """

    seen_urls = set()
    unique_articles = []

    for article in articles:

        url = normalize_url(
            article.get(
                "url",
                "",
            )
        )

        if not url:
            unique_articles.append(
                article
            )

            continue

        if url in seen_urls:
            continue

        seen_urls.add(url)

        unique_articles.append(
            article
        )

    return unique_articles
