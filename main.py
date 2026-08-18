import logging
from datetime import datetime
from pathlib import Path

from src.article_extractor import enrich_articles
from src.epub_builder import create_epub
from src.feed_reader import collect_articles
from src.utils import load_config, remove_duplicates
from src.kindle_sender import send_to_kindle


CONFIG_PATH = "config/feeds.yaml"
CSS_PATH = "templates/article.css"
OUTPUT_DIRECTORY = "output"


def configure_logging() -> None:
    """
    Configure application logging.
    """

    logging.basicConfig(
        level=logging.INFO,
        format=(
            "%(asctime)s | "
            "%(levelname)s | "
            "%(name)s | "
            "%(message)s"
        ),
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def main() -> None:
    """
    Run the personal newspaper generation pipeline.
    """

    configure_logging()

    logger = logging.getLogger(
        __name__
    )

    logger.info(
        "Starting personal newspaper generator."
    )

    # -------------------------------------------------
    # STEP 1
    # Load configuration
    # -------------------------------------------------

    config = load_config(
        CONFIG_PATH
    )

    newspaper_config = config[
        "newspaper"
    ]

    title = newspaper_config.get(
        "title",
        "Personal Daily Digest",
    )

    language = newspaper_config.get(
        "language",
        "it",
    )

    logger.info(
        "Newspaper title: %s",
        title,
    )

    # -------------------------------------------------
    # STEP 2
    # Collect articles from RSS feeds
    # -------------------------------------------------

    articles = collect_articles(
        config
    )

    if not articles:
        logger.error(
            "No articles were collected."
        )

        return

    logger.info(
        "Articles collected: %d",
        len(articles),
    )

    # -------------------------------------------------
    # STEP 3
    # Remove duplicate articles
    # -------------------------------------------------

    original_count = len(
        articles
    )

    articles = remove_duplicates(
        articles
    )

    duplicates_removed = (
        original_count
        - len(articles)
    )

    logger.info(
        "Removed %d duplicate articles.",
        duplicates_removed,
    )

    # -------------------------------------------------
    # STEP 4
    # Download and extract full article content
    # -------------------------------------------------

    articles = enrich_articles(
        articles
    )
    full_articles = sum(
        1
        for article in articles
        if article.get("content_source")
        == "full_article"
    )

    rss_summaries = sum(
        1
        for article in articles
        if article.get("content_source")
        == "rss_summary"
    )

    logger.info(
        "Full articles extracted: %d",
        full_articles,
    )

    logger.info(
        "RSS summary fallbacks: %d",
        rss_summaries,
    )

    # -------------------------------------------------
    # STEP 5
    # Generate output filename
    # -------------------------------------------------

    current_date = datetime.now().strftime(
        "%Y-%m-%d"
    )

    safe_title = (
        title
        .replace(" ", "_")
        .replace("/", "_")
    )

    output_filename = (
        f"{safe_title}_{current_date}.epub"
    )

    output_path = (
        Path(OUTPUT_DIRECTORY)
        / output_filename
    )

    # -------------------------------------------------
    # STEP 6
    # Build EPUB
    # -------------------------------------------------

    create_epub(
        articles=articles,
        output_path=str(output_path),
        title=title,
        language=language,
        css_path=CSS_PATH,
    )

    logger.info(
        "Newspaper successfully generated."
    )

    logger.info(
        "Output: %s",
        output_path,
    )
    # -------------------------------------------------
    # STEP 7
    # Send EPUB to Kindle
    # -------------------------------------------------

    logger.info(
        "Sending newspaper to Kindle."
    )

    send_enabled = newspaper_config.get(
    "send_to_kindle",
    False,
    )

    if send_enabled:

        logger.info(
            "Sending newspaper to Kindle."
        )

        send_to_kindle(
            str(output_path)
        )

        logger.info(
            "Newspaper successfully sent to Kindle."
        )

    else:

        logger.info(
            "Kindle delivery disabled."
        )


if __name__ == "__main__":
    main()
