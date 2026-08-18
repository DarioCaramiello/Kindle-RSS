from src.article_extractor import enrich_articles
from src.feed_reader import collect_articles
from src.utils import load_config


config = load_config(
    "config/feeds.yaml"
)

articles = collect_articles(
    config
)

articles = enrich_articles(
    articles
)

for article in articles:

    print("=" * 80)

    print(
        f"TITLE: {article['title']}"
    )

    print(
        f"SOURCE: {article['source']}"
    )

    print(
        f"DATE: {article['published']}"
    )

    print(
        f"CONTENT SOURCE: "
        f"{article['content_source']}"
    )

    print()

    print(
        article["content"][:500]
    )

    print()
