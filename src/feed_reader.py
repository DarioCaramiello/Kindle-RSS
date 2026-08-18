import logging
from datetime import datetime
from time import mktime

import feedparser


logger = logging.getLogger(__name__)


def parse_entry_date(entry) -> str:
    """
    Extract and normalize the publication date of an RSS entry.

    Args:
        entry: Feedparser entry object.

    Returns:
        Publication date in YYYY-MM-DD format.
        Returns an empty string if no valid date is available.
    """

    date_fields = [
        "published_parsed",
        "updated_parsed",
        "created_parsed",
    ]

    for field in date_fields:
        parsed_date = entry.get(field)

        if parsed_date:
            try:
                date = datetime.fromtimestamp(
                    mktime(parsed_date)
                )

                return date.strftime("%Y-%m-%d")

            except (ValueError, OverflowError, TypeError):
                continue

    return ""


def read_feed(
    feed_name: str,
    feed_url: str,
    category: str,
    max_articles: int = 5,
) -> list[dict]:
    """
    Download and parse a single RSS/Atom feed.

    Args:
        feed_name: Human-readable name of the feed.
        feed_url: RSS or Atom feed URL.
        category: Category assigned to the articles.
        max_articles: Maximum number of articles to return.

    Returns:
        A list of normalized article dictionaries.
    """

    logger.info(
        "Reading feed '%s' from %s",
        feed_name,
        feed_url,
    )

    parsed_feed = feedparser.parse(feed_url)

    if parsed_feed.bozo:
        logger.warning(
            "Feed '%s' may contain parsing errors: %s",
            feed_name,
            parsed_feed.bozo_exception,
        )

    if not parsed_feed.entries:
        logger.warning(
            "No articles found in feed '%s'.",
            feed_name,
        )

        return []

    articles = []

    for entry in parsed_feed.entries[:max_articles]:

        title = entry.get(
            "title",
            "Untitled article",
        ).strip()

        url = entry.get(
            "link",
            "",
        ).strip()

        summary = entry.get(
            "summary",
            "",
        )

        published = parse_entry_date(entry)

        article = {
            "source": feed_name,
            "category": category,
            "title": title,
            "url": url,
            "published": published,
            "summary": summary,
        }

        articles.append(article)

    logger.info(
        "Feed '%s': collected %d articles.",
        feed_name,
        len(articles),
    )

    return articles

def collect_articles(config: dict) -> list[dict]:
    """
    Collect articles from all feeds defined in the configuration.

    Args:
        config: Application configuration dictionary.

    Returns:
        Combined list of articles from all configured feeds.
    """

    feeds = config["feeds"]

    default_max_articles = config["newspaper"].get(
        "max_articles_per_feed",
        5,
    )

    all_articles = []

    for feed in feeds:

        feed_name = feed["name"]
        feed_url = feed["url"]
        category = feed.get(
            "category",
            "General",
        )

        max_articles = feed.get(
            "max_articles",
            default_max_articles,
        )

        try:
            articles = read_feed(
                feed_name=feed_name,
                feed_url=feed_url,
                category=category,
                max_articles=max_articles,
            )

            all_articles.extend(articles)

        except Exception:
            logger.exception(
                "Unexpected error while reading feed '%s'.",
                feed_name,
            )

    logger.info(
        "Collected %d articles in total.",
        len(all_articles),
    )

    return all_articles
