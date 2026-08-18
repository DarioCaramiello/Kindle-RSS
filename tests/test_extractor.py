from src.article_extractor import (
    extract_article_content,
)


url = "https://blog.python.org/"

content = extract_article_content(url)

if content:
    print(content[:3000])

else:
    print("Article extraction failed.")
