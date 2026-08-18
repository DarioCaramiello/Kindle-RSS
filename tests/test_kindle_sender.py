from pathlib import Path

from src.kindle_sender import send_to_kindle


OUTPUT_DIRECTORY = Path("output")


epub_files = list(
    OUTPUT_DIRECTORY.glob("*.epub")
)

if not epub_files:
    raise RuntimeError(
        "No EPUB files found in output directory."
    )


latest_epub = max(
    epub_files,
    key=lambda path: path.stat().st_mtime,
)


print(
    f"Sending EPUB: {latest_epub}"
)


send_to_kindle(
    str(latest_epub)
)


print(
    "EPUB sent successfully."
)