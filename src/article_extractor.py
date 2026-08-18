import logging

import trafilatura
from bs4 import BeautifulSoup


logger = logging.getLogger(__name__)


def clean_html(html: str) -> str:
    """
    Clean extracted HTML before inserting it into the EPUB.

    Args:
        html: Raw or extracted HTML content.

    Returns:
        Simplified HTML suitable for an EPUB document.
    """

    if not html:
        return ""

    soup = BeautifulSoup(
        html,
        "html.parser",
    )

    unwanted_tags = [
        "script",
        "style",
        "iframe",
        "video",
        "audio",
        "form",
        "button",
        "noscript",
    ]

    for tag_name in unwanted_tags:
        for tag in soup.find_all(tag_name):
            tag.decompose()

    # Remove most attributes that could interfere
    # with the Kindle layout.
    for element in soup.find_all(True):

        allowed_attributes = {}

        if element.name == "a":
            href = element.get("href")

            if href:
                allowed_attributes["href"] = href

        if element.name == "img":
            src = element.get("src")
            alt = element.get("alt")

            if src:
                allowed_attributes["src"] = src

            if alt:
                allowed_attributes["alt"] = alt

        element.attrs = allowed_attributes

    return str(soup)

def extract_article_content(url: str) -> str | None:
    """
    Download a web page and extract its main article content.

    Args:
        url: Article URL.

    Returns:
        Clean HTML containing the main article content,
        or None if extraction fails.
    """

    if not url:
        logger.warning(
            "Cannot extract article without URL."
        )

        return None

    logger.info(
        "Extracting article: %s",
        url,
    )

    try:

        downloaded = trafilatura.fetch_url(url)

        if not downloaded:
            logger.warning(
                "Unable to download article: %s",
                url,
            )

            return None

        extracted = trafilatura.extract(
            downloaded,
            output_format="html",
            include_links=True,
            include_tables=True,
            include_images=False,
            include_comments=False,
            favor_precision=True,
        )

        if not extracted:
            logger.warning(
                "Unable to extract main content: %s",
                url,
            )

            return None

        cleaned = clean_html(extracted)

        return cleaned

    except Exception:
        logger.exception(
            "Error extracting article: %s",
            url,
        )

        return None

def enrich_article(article: dict) -> dict:
    """
    Add full article content to an article dictionary.

    If full content extraction fails, the RSS summary is used
    as a fallback.

    Args:
        article: Normalized article dictionary.

    Returns:
        Article dictionary including a 'content' field.
    """

    content = extract_article_content(
        article["url"]
    )

    if content:
        article["content"] = content
        article["content_source"] = "full_article"

        return article

    logger.info(
        "Using RSS summary for article '%s'.",
        article["title"],
    )

    summary = article.get(
        "summary",
        "",
    )

    article["content"] = clean_html(summary)
    article["content_source"] = "rss_summary"

    return article

def enrich_articles(
    articles: list[dict],
) -> list[dict]:
    """
    Extract full content for all collected articles.

    Args:
        articles: List of normalized article dictionaries.

    Returns:
        List of enriched article dictionaries.
    """

    enriched_articles = []

    total = len(articles)

    for index, article in enumerate(
        articles,
        start=1,
    ):

        logger.info(
            "Processing article %d/%d: %s",
            index,
            total,
            article["title"],
        )

        enriched_article = enrich_article(
            article
        )

        enriched_articles.append(
            enriched_article
        )

    return enriched_articles
