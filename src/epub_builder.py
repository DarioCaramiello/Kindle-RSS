import html
import logging
from pathlib import Path

from ebooklib import epub


logger = logging.getLogger(__name__)

def load_css(
    css_path: str,
) -> str:
    """
    Load CSS used by the EPUB.

    Args:
        css_path: Path to the CSS file.

    Returns:
        CSS content as string.
    """

    path = Path(css_path)

    if not path.exists():
        raise FileNotFoundError(
            f"CSS file not found: {path}"
        )

    return path.read_text(
        encoding="utf-8"
    )

def create_article_chapter(
    article: dict,
    index: int,
    language: str,
    stylesheet,
):
    """
    Create an EPUB chapter for a single article.

    Args:
        article: Article dictionary.
        index: Sequential article number.
        language: EPUB language.
        stylesheet: EbookLib CSS item.

    Returns:
        EpubHtml chapter.
    """

    safe_title = html.escape(
        article["title"]
    )

    safe_source = html.escape(
        article["source"]
    )

    safe_category = html.escape(
        article.get(
            "category",
            "General",
        )
    )

    published = html.escape(
        article.get(
            "published",
            "",
        )
    )

    original_url = html.escape(
        article.get(
            "url",
            "",
        ),
        quote=True,
    )

    content = article.get(
        "content",
        "",
    )

    content_source = article.get(
        "content_source",
        "",
    )

    chapter = epub.EpubHtml(
        title=article["title"],
        file_name=(
            f"article_{index:03d}.xhtml"
        ),
        lang=language,
    )

    chapter.content = f"""
    <html>
        <head>
            <title>{safe_title}</title>
        </head>

           <body>

               <div class="article-header">

                   <p class="article-category">
                    {safe_category}
                </p>

                   <h1>{safe_title}</h1>

                   <div class="article-metadata">

                       <p>
                        {safe_source}
                        ·
                        {published or "Data non disponibile"}
                    </p>

                   </div>

               </div>

               {content}

               <div class="article-source">

                   <p>
                    Contenuto:
                    {html.escape(content_source)}
                </p>

                   <p>
                    <a href="{original_url}">
                        Leggi l'articolo originale
                    </a>
                </p>

               </div>

           </body>
    </html>
    """

    chapter.add_item(
        stylesheet
    )

    return chapter

def create_intro_chapter(
    title: str,
    article_count: int,
    language: str,
    stylesheet,
):
    """
    Create the newspaper introduction page.
    """

    chapter = epub.EpubHtml(
        title="Today's Edition",
        file_name="intro.xhtml",
        lang=language,
    )

    safe_title = html.escape(
        title
    )

    chapter.content = f"""
    <html>

           <head>
            <title>{safe_title}</title>
        </head>

           <body>

               <div class="newspaper-header">

                   <h1>{safe_title}</h1>

                   <p class="newspaper-subtitle">
                    La tua selezione quotidiana di notizie
                </p>

                   <hr/>

                   <p class="edition-info">
                    Articoli in questa edizione:
                    <strong>{article_count}</strong>
                </p>

               </div>

           </body>

       </html>
    """

    chapter.add_item(
        stylesheet
    )

    return chapter

def create_epub(
    articles: list[dict],
    output_path: str,
    title: str,
    language: str = "it",
    css_path: str = "templates/article.css",
) -> None:
    """
    Build the complete EPUB newspaper.

    Args:
        articles: Articles to include.
        output_path: Destination EPUB file.
        title: Newspaper title.
        language: EPUB language.
        css_path: CSS stylesheet path.
    """

    if not articles:
        raise ValueError(
            "Cannot create an EPUB without articles."
        )

    output = Path(
        output_path
    )

    output.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    logger.info(
        "Creating EPUB: %s",
        output,
    )

    book = epub.EpubBook()

    book.set_identifier(
        output.stem
    )

    book.set_title(
        title
    )

    book.set_language(
        language
    )

    book.add_author(
        "Personal Newspaper Generator"
    )

    css_content = load_css(
        css_path
    )

    stylesheet = epub.EpubItem(
        uid="style",
        file_name="styles/article.css",
        media_type="text/css",
        content=css_content,
    )

    book.add_item(
        stylesheet
    )

    intro = create_intro_chapter(
        title=title,
        article_count=len(articles),
        language=language,
        stylesheet=stylesheet,
    )

    book.add_item(
        intro
    )

    chapters = []

    for index, article in enumerate(
        articles,
        start=1,
    ):

        chapter = create_article_chapter(
            article=article,
            index=index,
            language=language,
            stylesheet=stylesheet,
        )

        book.add_item(
            chapter
        )

        chapters.append(
            chapter
        )

    book.toc = chapters

    book.add_item(
        epub.EpubNcx()
    )

    book.add_item(
        epub.EpubNav()
    )

    book.spine = [
        "nav",
        intro,
        *chapters,
    ]

    epub.write_epub(
        str(output),
        book,
    )

    logger.info(
        "EPUB successfully created: %s",
        output,
    )
